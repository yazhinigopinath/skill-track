# ⬡ Skill Track — Training Institute Management System

Full-stack web app: HTML/CSS/JS frontend · Python Flask backend · MySQL database

---

## Quick Start

### 1. Database
```bash
mysql -u root -p < database/schema.sql
```

### 2. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # edit with your MySQL password
python app.py               # http://localhost:5000
```

### 3. Frontend
Open `frontend/html/login.html` with VS Code Live Server (port 5500)  
or: `cd frontend && python -m http.server 5500`

---

## Demo Credentials

| Role     | Email                    | Password     |
|----------|--------------------------|--------------|
| Admin    | admin@skilltrack.com     | Admin@123    |
| Trainer  | trainer@skilltrack.com   | Trainer@123  |
| Student  | student@skilltrack.com   | Student@123  |
| Marketer | marketer@skilltrack.com  | Marketer@123 |

---

## API Routes

| Endpoint | Description |
|----------|-------------|
| POST /api/auth/login | JWT login |
| POST /api/auth/register | Register user |
| GET/POST /api/students/ | Students CRUD |
| GET/POST /api/trainers/ | Trainers CRUD |
| GET/POST /api/courses/ | Courses CRUD |
| GET/POST /api/batches/ | Batches CRUD |
| GET/POST /api/attendance/ | Attendance |
| GET/POST /api/projects/ | Projects & tasks |
| GET/POST /api/jobs/ | Job postings |
| GET/POST /api/assessments/ | Assessments |
| GET/POST /api/leads/ | Lead management |
| GET/POST /api/fees/ | Fee management |
| GET /api/reports/* | Reports & violations |

All endpoints require: `Authorization: Bearer <jwt_token>`

---

## Modules

- **Marketing** — Leads, pipeline, follow-ups, communication logs
- **Admin** — Students, trainers, courses, batches, fees, receipts
- **Training** — Attendance, projects, tasks, assessments, feedback
- **Placement** — Job postings, applications, mock interviews

## Tech Stack
- Frontend: HTML5 · CSS3 · Vanilla JS (Fetch API)
- Backend: Python Flask · Flask-JWT-Extended · Flask-CORS
- Database: MySQL 8.0 · mysql-connector-python
