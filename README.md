# Online-Job-Portal-Sql-Python-
**********************************
This project is a console-based Online Job Portal System developed using Oracle SQL and Python. It simulates a real-world job portal where job seekers can search and apply for jobs, and employers can post and manage job vacancies.
**********************************
The system focuses on database design, relational integrity, and backend logic, making it suitable as a portfolio project for data, SQL, or backend-focused roles.
**********************************
Technologies Used:
Oracle Database (SQL / PL-SQL)
Python
Oracledb (Python Oracle DB driver)
**********************************
Database Design
The system is built on a normalized relational database with 5 core tables:
Users – Stores authentication and role-based user data
JobSeekers – Stores skills and experience for job seekers
Employers – Stores company details
Jobs – Stores job vacancies posted by employers
Applications – Tracks job applications and their status
----------------------------------
Foreign keys with ON DELETE CASCADE
Data validation using CHECK constraints
Unique constraints to prevent duplicate applications
**********************************
Key Features
User Management
User registration and login
Role-based access (jobseeker / employer)
Profile completion after registration
----------------------------------
Job Search
View all available jobs
Keyword-based job search
Sorted by posting date
----------------------------------
Job Seeker Features
Complete job seeker profile (skills & experience)
Apply to jobs
View application history and statuses (Pending / Accepted / Rejected)
----------------------------------
Employer Features
Complete company profile
Post new job vacancies
View all posted jobs
