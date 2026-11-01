# CampusFix API Documentation

All requests and responses use JSON. All authenticated routes require a session cookie (credentials: "same-origin").

## Authentication Routes

### 1. Student Login
* **URL:** `/api/student/login`
* **Method:** `POST`
* **Body:** `{ "username": "student1", "password": "1234" }`
* **Success Response:** `{ "ok": true }`
* **Error Response:** `{ "ok": false, "error": "Invalid student credentials" }` (401)

### 2. Admin Login
* **URL:** `/api/admin/login`
* **Method:** `POST`
* **Body:** `{ "username": "admin", "password": "1234" }`
* **Success Response:** `{ "ok": true }`
* **Error Response:** `{ "ok": false, "error": "Invalid admin credentials" }` (401)

### 3. Logout (Student or Admin)
* **URL:** `/api/student/logout` OR `/api/admin/logout`
* **Method:** `POST`
* **Success Response:** `{ "ok": true }`

---

## Complaint Routes

### 4. Submit a Complaint (Student Only)
* **URL:** `/api/complaints`
* **Method:** `POST`
* **Headers:** Must be logged in as a Student.
* **Body:** `{ "room_number": "A-302", "description": "Fan is broken" }`
* **Success Response:** `{ "ok": true, "id": 15 }` (201)
* **Error Response:** `{ "ok": false, "error": "Room and description are required" }` (400)

### 5. Get Complaints
* **URL:** `/api/complaints`
* **Method:** `GET`
* **Behavior:** 
  * If **Admin** is logged in: Returns **all** complaints (Open first, then Fixed).
  * If **Student** is logged in: Returns **only** their own complaints.
* **Success Response (Student):** 
  ```json
  {
    "ok": true,
    "student_name": "student1",
    "complaints": [
      { "id": 1, "student_name": "student1", "room_number": "A-1", "description": "Fan", "status": "open", "created_at": "2026-11-01T10:00:00", "fixed_at": null }
    ]
  }