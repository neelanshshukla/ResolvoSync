from app import app
from models import db, Admin, Student
from werkzeug.security import generate_password_hash

with app.app_context():

    if not Admin.query.filter_by(username = "admin").first():
        hashed_pw = generate_password_hash("1234")
        new_admin = Admin(username = "admin" , password_hash = hashed_pw)
        db.session.add(new_admin)
        print("✅ Admin created username: admin, password: 1234")
    else:
        print("ℹ️ Admin already exists.")    

    if not Student.query.filter_by(username = "student1").first():
        hashed_pw = generate_password_hash("1234")
        new_student = Student(username = "student1", password_hash = hashed_pw)
        db.session.add(new_student)
        print("✅ student created username: student1, password: 1234")
    else:
        print("ℹ️ student already exists.")    

    db.session.commit()