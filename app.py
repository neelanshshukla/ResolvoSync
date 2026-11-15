import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, jsonify, render_template, request, session
from config import Config
from models import db, Complaint, Admin, Student
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# --- NEW CODE FOR SSL CERTIFICATE ---
db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
if db_url and "mysql" in db_url:
    if "?ssl-mode=REQUIRED" in db_url:
        db_url = db_url.replace("?ssl-mode=REQUIRED", "")
    
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            "ssl": {
                "ca": "ca.pem"
            }
        }
    }

db.init_app(app)
# ------------------------------------

# ==========================================
# PAGE ROUTES
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/student")
def student_page():
    return render_template("student.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")


# ==========================================
# API ROUTES: AUTHENTICATION
# ==========================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and check_password_hash(admin.password_hash, password):
        session.clear()
        session["admin"] = admin.username 
        return jsonify({"ok": True})
    
    return jsonify({"ok": False, "error": "Invalid admin credentials"}), 401

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/student/login", methods=["POST"])
def student_login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    
    student = Student.query.filter_by(username=username).first()
    
    if student and check_password_hash(student.password_hash, password):
        session.clear()
        # SAVE BOTH ID AND NAME IN SESSION
        session["student_id"] = student.id 
        session["student_name"] = student.username 
        return jsonify({"ok": True})
        
    return jsonify({"ok": False, "error": "Invalid student credentials"}), 401

@app.route("/api/student/logout", methods=["POST"])
def student_logout():
    session.clear()
    return jsonify({"ok": True})


# ==========================================
# API ROUTES: COMPLAINTS
# ==========================================

@app.route("/api/complaints", methods=["POST"])
def add_complaint():
    if not session.get("student_id"):
        return jsonify({"ok": False, "error": "You must be logged in to submit"}), 401

    data = request.json
    room = data.get("room_number", "").strip()
    desc = data.get("description", "").strip()
    
    # Get ID and Name from session
    student_id = session.get("student_id")
    student_name = session.get("student_name")

    if not room or not desc:
        return jsonify({"ok": False, "error": "Room and description are required"}), 400

    new_complaint = Complaint(
        student_id=student_id, 
        student_name=student_name, 
        room_number=room, 
        description=desc
    )
    db.session.add(new_complaint)
    db.session.commit()
    
    return jsonify({"ok": True, "id": new_complaint.id}), 201

@app.route("/api/complaints", methods=["GET"])
def get_complaints():
    # 1. Admin sees all
    if session.get("admin"):
        open_complaints = Complaint.query.filter_by(status="open").order_by(Complaint.created_at.desc()).all()
        fixed_complaints = Complaint.query.filter_by(status="fixed").order_by(Complaint.fixed_at.desc()).all()
        all_complaints = open_complaints + fixed_complaints
        response = jsonify({
            "ok": True, 
            "admin_name": session.get("admin"), 
            "complaints": [c.to_dict() for c in all_complaints]
        })
        
    # 2. Student sees ONLY their own (Filtered by ID)
    elif session.get("student_id"):
        student_id = session.get("student_id")
        my_complaints = Complaint.query.filter_by(student_id=student_id).order_by(Complaint.created_at.desc()).all()
        response = jsonify({
            "ok": True, 
            "student_name": session.get("student_name"), 
            "complaints": [c.to_dict() for c in my_complaints]
        })
        
    else:
        response = jsonify({"ok": False, "error": "Unauthorized"}), 401

    # Force no cache
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/api/complaints/<int:id>/fix", methods=["PATCH"])
def fix_complaint(id):
    if not session.get("admin"):
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    complaint = Complaint.query.get(id)
    if not complaint:
        return jsonify({"ok": False, "error": "Complaint not found"}), 404

    if complaint.status != "fixed":
        complaint.status = "fixed"
        complaint.fixed_at = datetime.utcnow()
        db.session.commit()

    return jsonify({"ok": True})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)