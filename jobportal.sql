--Creating Tables
/* I have 5 tables(Users, Job Seekers, Employers, Jobs and Applications)*/
-- Creating Users table
CREATE TABLE Users (
    user_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(120) NOT NULL UNIQUE,
    password VARCHAR2(255) NOT NULL,
    role VARCHAR2(20) NOT NULL,
    created_at DATE DEFAULT SYSDATE,
    
    CONSTRAINT chk_user_role CHECK (role IN ('jobseeker','employer'))
);
--Creating Job Seekers table
CREATE TABLE JobSeekers (
    seeker_id NUMBER PRIMARY KEY,
    user_id NUMBER NOT NULL UNIQUE,
    skills CLOB,--for extra large data values
    experience_years NUMBER DEFAULT 0,

    CONSTRAINT fk_jobseeker_user 
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE,--for preventing deleted user crash, because if u can delete 1 user it will not work because of it include in other tables.

    CONSTRAINT chk_experience CHECK (experience_years >= 0)
);
--Creating Employers table
CREATE TABLE Employers (
    employer_id NUMBER PRIMARY KEY,
    user_id NUMBER NOT NULL UNIQUE,
    company_name VARCHAR2(150) NOT NULL,
    location VARCHAR2(120),

    CONSTRAINT fk_employer_user 
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
);
--Creating Jobs table
CREATE TABLE Jobs (
    job_id NUMBER PRIMARY KEY,
    employer_id NUMBER NOT NULL,
    job_title VARCHAR2(120) NOT NULL,
    description CLOB,
    location VARCHAR2(120),
    salary_min NUMBER,
    salary_max NUMBER,
    job_type VARCHAR2(20) NOT NULL,
    posted_date DATE DEFAULT SYSDATE,

    CONSTRAINT fk_job_employer
        FOREIGN KEY (employer_id)
        REFERENCES Employers(employer_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_job_type CHECK (job_type IN ('full-time','part-time','remote','internship')),
    CONSTRAINT chk_salary CHECK (
        salary_min IS NULL 
        OR salary_max IS NULL 
        OR salary_max >= salary_min
    )
);
--Creating Applications Table
CREATE TABLE Applications (
    application_id NUMBER PRIMARY KEY,
    job_id NUMBER NOT NULL,
    seeker_id NUMBER NOT NULL,
    apply_date DATE DEFAULT SYSDATE,
    status VARCHAR2(20) DEFAULT 'Pending',

    CONSTRAINT fk_application_job
        FOREIGN KEY (job_id)
        REFERENCES Jobs(job_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_application_seeker
        FOREIGN KEY (seeker_id)
        REFERENCES JobSeekers(seeker_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_status CHECK (status IN ('Pending','Accepted','Rejected')),
    CONSTRAINT unique_application UNIQUE (job_id, seeker_id)
);
--Now we can insert our values to the table.
--İnserting into Users table
--Normal Users
INSERT INTO Users VALUES (1, 'Elvin Babayev', 'elvin@mail.com', 'pass1', 'jobseeker', SYSDATE);
INSERT INTO Users VALUES (2, 'Aysel Aliyeva', 'aysel@mail.com', 'pass2', 'jobseeker', SYSDATE);
INSERT INTO Users VALUES (3, 'Murad Hasan', 'murad@mail.com', 'pass3', 'jobseeker', SYSDATE);
INSERT INTO Users VALUES (4, 'Lale Karim', 'lale@mail.com', 'pass4', 'jobseeker', SYSDATE);
INSERT INTO Users VALUES (5, 'Rashad Mammad', 'rashad@mail.com', 'pass5', 'jobseeker', SYSDATE);
--Companies
INSERT INTO Users VALUES (6, 'TechSoft HR', 'techsoft@mail.com', 'pass6', 'employer', SYSDATE);
INSERT INTO Users VALUES (7, 'GlobalBank HR', 'gbank@mail.com', 'pass7', 'employer', SYSDATE);
INSERT INTO Users VALUES (8, 'AzerIT Solutions', 'azerit@mail.com', 'pass8', 'employer', SYSDATE);
INSERT INTO Users VALUES (9, 'NextGen Company', 'nextgen@mail.com', 'pass9', 'employer', SYSDATE);
INSERT INTO Users VALUES (10, 'FutureCorp HR', 'future@mail.com', 'pass10', 'employer', SYSDATE);
--Inserting into Job Seekers table
INSERT INTO JobSeekers VALUES (1, 1, 'Python, SQL, Data Analysis', 2);
INSERT INTO JobSeekers VALUES (2, 2, 'Java, Spring Boot, APIs', 3);
INSERT INTO JobSeekers VALUES (3, 3, 'HTML, CSS, JavaScript, React', 1);
INSERT INTO JobSeekers VALUES (4, 4, 'Data Science, Machine Learning', 4);
INSERT INTO JobSeekers VALUES (5, 5, 'Accountant, Excel, PowerBI', 5);
--Inserting into Employers table
INSERT INTO Employers VALUES (1, 6, 'TechSoft', 'Baku');
INSERT INTO Employers VALUES (2, 7, 'GlobalBank', 'Baku');
INSERT INTO Employers VALUES (3, 8, 'AzerIT Solutions', 'Ganja');
INSERT INTO Employers VALUES (4, 9, 'NextGen', 'Baku');
INSERT INTO Employers VALUES (5, 10, 'FutureCorp', 'Sumqayit');
--Inserting into Jobs table
INSERT INTO Jobs VALUES (1, 1, 'Junior Python Developer', 'Work with data analytics projects', 'Baku', 800, 1500, 'full-time', SYSDATE);
INSERT INTO Jobs VALUES (2, 1, 'SQL Database Specialist', 'SQL tuning and database support', 'Remote', 900, 1700, 'remote', SYSDATE);

INSERT INTO Jobs VALUES (3, 2, 'Bank Data Analyst', 'Analyze customer financial data', 'Baku', 1200, 2500, 'full-time', SYSDATE);
INSERT INTO Jobs VALUES (4, 2, 'IT Support Specialist', 'Provide technical support', 'Baku', 700, 1200, 'full-time', SYSDATE);

INSERT INTO Jobs VALUES (5, 3, 'Frontend Developer', 'React developer for web apps', 'Ganja', 900, 1800, 'full-time', SYSDATE);
INSERT INTO Jobs VALUES (6, 3, 'Intern Web Developer', 'Training internship', 'Remote', 0, 500, 'internship', SYSDATE);

INSERT INTO Jobs VALUES (7, 4, 'Machine Learning Engineer', 'Work on AI models', 'Baku', 2000, 4000, 'full-time', SYSDATE);
INSERT INTO Jobs VALUES (8, 4, 'Part-Time Research Assistant', 'Assist in data projects', 'Remote', 300, 800, 'part-time', SYSDATE);

INSERT INTO Jobs VALUES (9, 5, 'Accountant', 'Manage financial reports', 'Sumqayit', 1000, 2000, 'full-time', SYSDATE);
INSERT INTO Jobs VALUES (10, 5, 'Business Analyst', 'Analyze business processes', 'Baku', 1500, 2800, 'full-time', SYSDATE);
--Inserting into Applications table
INSERT INTO Applications VALUES (1, 1, 1, SYSDATE, 'Pending');
INSERT INTO Applications VALUES (2, 1, 2, SYSDATE, 'Rejected');
INSERT INTO Applications VALUES (3, 2, 1, SYSDATE, 'Accepted');
INSERT INTO Applications VALUES (4, 3, 4, SYSDATE, 'Pending');
INSERT INTO Applications VALUES (5, 4, 1, SYSDATE, 'Pending');
INSERT INTO Applications VALUES (6, 5, 3, SYSDATE, 'Accepted');
INSERT INTO Applications VALUES (7, 6, 2, SYSDATE, 'Pending');
INSERT INTO Applications VALUES (8, 7, 4, SYSDATE, 'Rejected');
INSERT INTO Applications VALUES (9, 9, 5, SYSDATE, 'Pending');
INSERT INTO Applications VALUES (10, 10, 1, SYSDATE, 'Pending');
--Select for overview
SELECT
    a.application_id,
    u_seeker.name AS seeker_name,
    js.experience_years,
    
    j.job_id,
    j.job_title,
    j.location AS job_location,

    e.company_name,
    u_employer.name AS employer_user_name,

    a.apply_date,
    a.status
FROM Applications a
JOIN JobSeekers js 
    ON a.seeker_id = js.seeker_id
JOIN Users u_seeker 
    ON js.user_id = u_seeker.user_id
JOIN Jobs j 
    ON a.job_id = j.job_id
JOIN Employers e 
    ON j.employer_id = e.employer_id
JOIN Users u_employer 
    ON e.user_id = u_employer.user_id
ORDER BY a.application_id;
--describe of all tables
desc Applications;
desc JobSeekers;
desc Users;
desc Employers;
desc Applications;
--Commit changes
commit;








