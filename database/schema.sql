-- =============================================
-- Skill Track - Training Institute Management
-- MySQL Database Schema
-- =============================================

CREATE DATABASE IF NOT EXISTS skill_track;
USE skill_track;

-- ROLES
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USERS
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- STUDENTS
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    user_id INT UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    dob DATE,
    gender ENUM('Male','Female','Other'),
    qualification VARCHAR(150),
    enrolled_date DATE,
    status ENUM('Active','Inactive','Completed','Dropped') DEFAULT 'Active',
    documents_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- TRAINERS
CREATE TABLE trainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(200),
    experience_years INT DEFAULT 0,
    status ENUM('Active','Inactive') DEFAULT 'Active',
    joined_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- MARKETERS
CREATE TABLE marketers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    status ENUM('Active','Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- COURSES
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    duration_weeks INT,
    fee DECIMAL(10,2),
    syllabus_json JSON,
    status ENUM('Active','Archived') DEFAULT 'Active',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- BATCHES
CREATE TABLE batches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_code VARCHAR(30) UNIQUE NOT NULL,
    course_id INT NOT NULL,
    trainer_id INT,
    batch_name VARCHAR(150) NOT NULL,
    start_date DATE,
    end_date DATE,
    schedule_json JSON,
    meeting_link VARCHAR(500),
    max_students INT DEFAULT 30,
    status ENUM('Upcoming','Ongoing','Completed') DEFAULT 'Upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (trainer_id) REFERENCES trainers(id)
);

-- BATCH STUDENTS (mapping)
CREATE TABLE batch_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    student_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_batch_student (batch_id, student_id),
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- FEES
CREATE TABLE fees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    batch_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    due_date DATE,
    paid_date DATE,
    receipt_number VARCHAR(50) UNIQUE,
    payment_mode ENUM('Cash','Card','UPI','Bank Transfer') DEFAULT 'Cash',
    status ENUM('Pending','Partial','Paid','Overdue') DEFAULT 'Pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (batch_id) REFERENCES batches(id)
);

-- ATTENDANCE
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present','Absent','Late','Leave') DEFAULT 'Absent',
    in_time TIME,
    out_time TIME,
    session_duration_minutes INT,
    marked_by INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_attendance (batch_id, student_id, date),
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (marked_by) REFERENCES users(id)
);

-- LEAVE REQUESTS
CREATE TABLE leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    batch_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    reason TEXT,
    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    reviewed_by INT,
    reviewed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id)
);

-- PROJECTS
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    batch_id INT,
    assigned_by INT,
    deadline DATE,
    status ENUM('Active','Completed','Archived') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id)
);

-- TASKS
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    student_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    deadline DATETIME,
    priority ENUM('Low','Medium','High','Critical') DEFAULT 'Medium',
    status ENUM('Assigned','In Progress','Completed','Overdue') DEFAULT 'Assigned',
    completed_at TIMESTAMP NULL,
    violation_flag BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- COURSE MATERIALS
CREATE TABLE course_materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    material_type ENUM('Document','Video','Link','Assignment') DEFAULT 'Document',
    file_path VARCHAR(500),
    url VARCHAR(1000),
    video_duration_minutes INT,
    order_index INT DEFAULT 0,
    uploaded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- VIDEO TRACKING
CREATE TABLE video_tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    student_id INT NOT NULL,
    watched_minutes INT DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    last_watched_at TIMESTAMP NULL,
    UNIQUE KEY uq_video_track (material_id, student_id),
    FOREIGN KEY (material_id) REFERENCES course_materials(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- FEEDBACK
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    student_id INT NOT NULL,
    week_number INT NOT NULL,
    trainer_rating INT CHECK (trainer_rating BETWEEN 1 AND 5),
    content_rating INT CHECK (content_rating BETWEEN 1 AND 5),
    overall_rating INT CHECK (overall_rating BETWEEN 1 AND 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_feedback (batch_id, student_id, week_number),
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- JOBS
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(200),
    location VARCHAR(200),
    description TEXT,
    requirements TEXT,
    salary_range VARCHAR(100),
    job_type ENUM('Full-time','Part-time','Internship','Contract') DEFAULT 'Full-time',
    posted_by INT,
    deadline DATE,
    status ENUM('Active','Closed') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

-- JOB APPLICATIONS
CREATE TABLE job_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    student_id INT NOT NULL,
    resume_path VARCHAR(500),
    cover_letter TEXT,
    status ENUM('Applied','Shortlisted','Interviewed','Selected','Rejected') DEFAULT 'Applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_job_application (job_id, student_id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ASSESSMENTS
CREATE TABLE assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    assessment_type ENUM('Coding','Aptitude','Mock Interview','Communication') DEFAULT 'Aptitude',
    batch_id INT,
    description TEXT,
    total_marks INT DEFAULT 100,
    pass_marks INT DEFAULT 40,
    duration_minutes INT DEFAULT 60,
    scheduled_at DATETIME,
    status ENUM('Scheduled','Active','Completed') DEFAULT 'Scheduled',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- ASSESSMENT RESULTS
CREATE TABLE assessment_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL,
    student_id INT NOT NULL,
    score DECIMAL(5,2),
    status ENUM('Pass','Fail','Absent') DEFAULT 'Absent',
    submitted_at TIMESTAMP NULL,
    remarks TEXT,
    UNIQUE KEY uq_assessment_result (assessment_id, student_id),
    FOREIGN KEY (assessment_id) REFERENCES assessments(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- MOCK INTERVIEWS
CREATE TABLE mock_interviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    interviewer_id INT,
    scheduled_at DATETIME,
    duration_minutes INT DEFAULT 30,
    feedback TEXT,
    communication_score INT CHECK (communication_score BETWEEN 1 AND 10),
    technical_score INT CHECK (technical_score BETWEEN 1 AND 10),
    overall_score INT CHECK (overall_score BETWEEN 1 AND 10),
    status ENUM('Scheduled','Completed','Cancelled','No Show') DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (interviewer_id) REFERENCES users(id)
);

-- LEADS (Marketing)
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(20),
    source ENUM('Website','WhatsApp','Referral','Social Media','Walk-in','Email','Phone') DEFAULT 'Website',
    interested_course VARCHAR(200),
    status ENUM('New','Contacted','Interested','Follow-up','Converted','Lost') DEFAULT 'New',
    assigned_to INT,
    notes TEXT,
    next_followup_date DATE,
    converted_student_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (converted_student_id) REFERENCES students(id)
);

-- LEAD COMMUNICATIONS
CREATE TABLE lead_communications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lead_id INT NOT NULL,
    comm_type ENUM('WhatsApp','Email','Call','SMS') DEFAULT 'Call',
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_by INT,
    response TEXT,
    responded_at TIMESTAMP NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (sent_by) REFERENCES users(id)
);

-- RESUMES
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNIQUE NOT NULL,
    content_json JSON,
    template VARCHAR(50) DEFAULT 'default',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- =============================================
-- SEED DATA
-- =============================================

INSERT INTO roles (name, description, permissions) VALUES
('super_admin', 'Full system access', '{"all": true}'),
('admin', 'Institute administration', '{"students": true, "trainers": true, "courses": true, "batches": true, "fees": true, "reports": true}'),
('trainer', 'Training management', '{"attendance": true, "projects": true, "assessments": true, "feedback": true}'),
('student', 'Student portal', '{"profile": true, "attendance_view": true, "tasks": true, "jobs": true}'),
('marketer', 'Marketing operations', '{"leads": true, "communications": true, "reports": true}');

INSERT INTO users (username, email, password_hash, role_id) VALUES
('superadmin', 'superadmin@skilltrack.com', 'pbkdf2:sha256:dummy_hash_super', 1),
('admin1', 'admin@skilltrack.com', 'pbkdf2:sha256:dummy_hash_admin', 2),
('trainer1', 'trainer@skilltrack.com', 'pbkdf2:sha256:dummy_hash_trainer', 3),
('student1', 'student@skilltrack.com', 'pbkdf2:sha256:dummy_hash_student', 4),
('marketer1', 'marketer@skilltrack.com', 'pbkdf2:sha256:dummy_hash_marketer', 5);

INSERT INTO trainers (user_id, full_name, email, phone, specialization, experience_years, joined_date) VALUES
(3, 'Arjun Sharma', 'trainer@skilltrack.com', '9876543210', 'Python, Django, Data Science', 5, '2022-01-15');

INSERT INTO students (student_id, user_id, full_name, email, phone, qualification, enrolled_date) VALUES
('ST001', 4, 'Priya Patel', 'student@skilltrack.com', '9123456780', 'B.Tech', '2024-01-10');

INSERT INTO courses (course_code, title, description, duration_weeks, fee) VALUES
('PY101', 'Python Full Stack Development', 'Comprehensive Python web development course', 16, 35000.00),
('DS201', 'Data Science & ML', 'Data analysis, visualization and machine learning', 20, 45000.00),
('WD301', 'Full Stack Web Development', 'HTML, CSS, JS, Node.js and React', 12, 30000.00);

INSERT INTO batches (batch_code, course_id, trainer_id, batch_name, start_date, end_date, status) VALUES
('PY101-B1', 1, 1, 'Python Batch Jan 2024', '2024-01-15', '2024-05-15', 'Completed'),
('DS201-B1', 2, 1, 'Data Science Batch Mar 2024', '2024-03-01', '2024-08-01', 'Ongoing');

INSERT INTO leads (full_name, email, phone, source, interested_course, status) VALUES
('Rahul Kumar', 'rahul@email.com', '9000000001', 'Website', 'Python Full Stack', 'Interested'),
('Meena Iyer', 'meena@email.com', '9000000002', 'WhatsApp', 'Data Science', 'Follow-up'),
('Karan Singh', 'karan@email.com', '9000000003', 'Referral', 'Full Stack Web', 'New'),
('Divya Reddy', 'divya@email.com', '9000000004', 'Social Media', 'Python Full Stack', 'Contacted');

INSERT INTO jobs (title, company, location, description, salary_range, job_type, deadline) VALUES
('Junior Python Developer', 'TechCorp Solutions', 'Chennai', 'Develop Flask APIs and Python scripts', '3-5 LPA', 'Full-time', '2024-12-31'),
('Data Analyst Intern', 'Analytics Hub', 'Bangalore (Remote)', 'Analyze datasets and build dashboards', '15000/month', 'Internship', '2024-11-30');
