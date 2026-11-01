# CampusFix Database Schema

We are using a Cloud MySQL Database (via Aiven) connected through SQLAlchemy. The database consists of three main tables:

## 1. `admin`
Stores the credentials for the system administrators.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-increment | Unique ID for the admin |
| `username` | String(50) | Unique, Not Null | Admin's login ID |
| `password_hash` | String(255) | Not Null | Securely hashed password |

## 2. `student`
Stores the credentials for the students.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-increment | Unique ID for the student |
| `username` | String(50) | Unique, Not Null | Student's login ID |
| `password_hash` | String(255) | Not Null | Securely hashed password |

## 3. `complaint`
Stores the actual complaints submitted by the students.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-increment | Unique tracking number |
| `student_name` | String(100) | Not Null | Username of the student who submitted it |
| `room_number` | String(20) | Not Null | The room where the issue is |
| `description` | Text | Not Null | Details of the problem |
| `status` | String(10) | Default: "open" | Status: "open" or "fixed" |
| `created_at` | DateTime | Default: UTC Now | Exact time the complaint was made |
| `fixed_at` | DateTime | Nullable | Exact time the admin resolved it |