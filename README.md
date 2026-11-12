# CampusFix - Hostel Complaint Intelligence System

CampusFix is a full-stack web application designed to streamline the process of reporting and resolving hostel maintenance issues. It provides separate portals for Students and Administrators.

## 🏗️ System Architecture

```mermaid
flowchart TD
    %% Define Styles
    classDef frontend fill:#3b82f6,stroke:#1e3a8a,stroke-width:2px,color:#fff;
    classDef backend fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff;
    classDef database fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff;
    classDef user fill:#8b5cf6,stroke:#5b21b6,stroke-width:2px,color:#fff;

    %% Entities
    Student([👨‍🎓 Student]):::user
    Admin([🛡️ Admin]):::user
    
    subgraph Frontend [Frontend - Browser]
        UI[HTML/CSS/JS Dashboard]:::frontend
        JS[JavaScript Fetch API]:::frontend
    end

    subgraph Backend [Backend - Python Flask Server]
        API[Flask REST API routes]:::backend
        Auth[Session & Auth Logic]:::backend
        ORM[SQLAlchemy ORM]:::backend
    end

    subgraph Cloud [Cloud Database - Aiven]
        DB[(MySQL Database)]:::database
    end

    %% Connections
    Student -->|1. Enters Username/Password| UI
    Admin -->|1. Enters Admin ID/Password| UI
    
    UI -->|2. Sends JSON Request| JS
    JS -->|3. HTTP POST/GET Request| API
    
    API --> Auth
    Auth -->|4. Checks Session Cookie| ORM
    
    ORM -->|5. Translates Python to SQL| DB
    DB -->|6. Returns Data Rows| ORM
    ORM -->|7. Returns JSON Data| JS
    JS -->|8. Updates the DOM| UI

#  Features
* **Student Portal:** Students can log in securely to submit new complaints (room number & description) and track the real-time status of their previous complaints.
* **Admin Portal:** Admins can log in to view all registered complaints. When an issue is resolved, the admin can mark it as "Fixed".
* **Smart Sorting:** Open complaints appear at the top. Once marked as fixed, the complaint is struck through, greyed out, and automatically moves to the bottom of the list.
* **Secure Authentication:** Passwords are securely hashed using `werkzeug.security`. Role-based session management ensures students cannot access admin routes or view other students' complaints.

#  Technology Stack
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Backend:** Python, Flask Framework
* **Database:** MySQL (Hosted on Aiven Cloud)
* **ORM:** Flask-SQLAlchemy

# Project Structure
* `app.py` - The main Flask application and API routes.
* `models.py` - Database models (Admin, Student, Complaint).
* `config.py` - Configuration and database connection URI.
* `seed_admin.py` - A setup script to create the initial admin and a test student.
* `templates/` - Contains the HTML files for the UI.
* `static/` - Contains the CSS and JavaScript files.

# How to Run Locally

**1. Install Dependencies:**
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
