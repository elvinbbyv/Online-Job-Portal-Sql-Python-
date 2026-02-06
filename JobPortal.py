import oracledb


# ******************* DATABASE CONNECTION *******************
def get_db_connection():
    """Joining to the Oracle Database"""
    try:
        connection = oracledb.connect(
            user="your user name for example:'jobportal'",
            password="your password",
            dsn="your dsn address for example:'localhost'",
        )
        return connection
    except oracledb.Error as e:
        print(f":( Database connection error: {e}")
        return None


# ******************* AUTHENTICATION *******************
current_user_id = None
current_user_role = None


def login():
    """User Login"""
    global current_user_id, current_user_role

    print("\n" + "=" * 40)
    print("LOGIN")
    print("=" * 40)

    email = input("Email: ")
    password = input("Password: ")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, name, role FROM Users 
            WHERE email = :1 AND password = :2
        """, (email, password))

        user = cursor.fetchone()

        if user:
            current_user_id = user[0]
            current_user_role = user[2]
            print(f":) Welcome, {user[1]}! (Role: {user[2]})")
        else:
            print(":( Invalid email or password!")
            current_user_id = None
            current_user_role = None

        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Login error: {e}")

    input("\nPress Enter to continue...")


def register():
    """New Person Register"""
    print("\n" + "=" * 40)
    print("REGISTER")
    print("=" * 40)

    name = input("Full Name: ")
    email = input("Email: ")
    password = input("Password: ")

    role = ""
    while role not in ['jobseeker', 'employer']:
        role = input("Role (jobseeker/employer): ").lower()
        if role not in ['jobseeker', 'employer']:
            print(":( Please enter only 'jobseeker' or 'employer'")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Finding new user id
        cursor.execute("SELECT MAX(user_id) FROM Users")
        result = cursor.fetchone()
        new_user_id = (result[0] or 0) + 1  # If Null 0+1=1

        # Add user
        cursor.execute("""
            INSERT INTO Users (user_id, name, email, password, role, created_at)
            VALUES (:1, :2, :3, :4, :5, SYSDATE)
        """, (new_user_id, name, email, password, role))

        conn.commit()

        print(f":) Registration successful! Your User ID: {new_user_id}")

        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Registration failed: {e}")

    input("\nPress Enter to continue...")


# ******************* PROFILE COMPLETION *******************
def complete_profile():
    """Completing New User Profile"""
    if not current_user_id:
        print(":( Please login first!")
        input("\nPress Enter to continue...")
        return

    print("\n" + "=" * 40)
    print("COMPLETE YOUR PROFILE")
    print("=" * 40)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if current_user_role == 'jobseeker':
            # FInding New Seeker ID
            cursor.execute("SELECT MAX(seeker_id) FROM JobSeekers")
            result = cursor.fetchone()
            new_seeker_id = (result[0] or 0) + 1

            # Ask users about their information
            print("\nPlease enter your information:")
            skills = input("Your skills (e.g., Python, SQL): ")

            experience = input("Years of experience (enter number): ")
            try:
                experience_years = int(experience)
            except:
                experience_years = 0

            # Add to JobSeeker schedule
            cursor.execute("""
                INSERT INTO JobSeekers (seeker_id, user_id, skills, experience_years)
                VALUES (:1, :2, :3, :4)
            """, (new_seeker_id, current_user_id, skills, experience_years))

            print(":) Profile created successfully!")

        elif current_user_role == 'employer':
            # Find New Employer ID
            cursor.execute("SELECT MAX(employer_id) FROM Employers")
            result = cursor.fetchone()
            new_employer_id = (result[0] or 0) + 1

            # Ask user about their info
            print("\nPlease enter company information:")
            company_name = input("Company Name: ")
            location = input("Company Location: ")

            # Add to Employers schedule
            cursor.execute("""
                INSERT INTO Employers (employer_id, user_id, company_name, location)
                VALUES (:1, :2, :3, :4)
            """, (new_employer_id, current_user_id, company_name, location))

            print(":) Company profile created successfully!")

        conn.commit()
        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Profile error: {e}")

    input("\nPress Enter to continue...")


# ******************* JOB OPERATIONS *******************
def search_jobs():
    """Search Vacancies"""
    print("\n" + "=" * 40)
    print("SEARCH JOBS")
    print("=" * 40)

    keyword = input("Search keyword (press Enter for all): ")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if keyword.strip():
            query = """
                SELECT j.job_id, j.job_title, e.company_name, j.location
                FROM Jobs j
                JOIN Employers e ON j.employer_id = e.employer_id
                WHERE j.job_title LIKE :1
                ORDER BY j.posted_date DESC
            """
            cursor.execute(query, (f'%{keyword}%',))
        else:
            cursor.execute("""
                SELECT j.job_id, j.job_title, e.company_name, j.location
                FROM Jobs j
                JOIN Employers e ON j.employer_id = e.employer_id
                ORDER BY j.posted_date DESC
            """)

        jobs = cursor.fetchall()

        print(f"\n-----> Found {len(jobs)} jobs:")
        print("-" * 60)

        for job in jobs:
            print(f"ID: {job[0]} | {job[1]} at {job[2]} ({job[3]})")

        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Search error: {e}")

    input("\nPress Enter to continue...")


def apply_job():
    """Apply For Job"""
    if not current_user_id:
        print(":( Please login first!")
        input("\nPress Enter to continue...")
        return

    if current_user_role != 'jobseeker':
        print(":( Only job seekers can apply for jobs!")
        input("\nPress Enter to continue...")
        return

    print("\n" + "=" * 40)
    print("APPLY FOR JOB")
    print("=" * 40)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Find JobSeeker ID
        cursor.execute("SELECT seeker_id FROM JobSeekers WHERE user_id = :1", (current_user_id,))
        seeker = cursor.fetchone()

        if not seeker:
            print(":( Please complete your job seeker profile first!")
            print("Choose option 5 from main menu.")
            input("\nPress Enter to continue...")
            return

        seeker_id = seeker[0]

        # Show all open vacancies first
        print("\n-----> AVAILABLE JOBS:")
        print("-" * 60)
        cursor.execute("""
            SELECT j.job_id, j.job_title, e.company_name, j.location
            FROM Jobs j
            JOIN Employers e ON j.employer_id = e.employer_id
            WHERE j.job_id NOT IN (
                SELECT job_id FROM Applications WHERE seeker_id = :1
            )
            ORDER BY j.posted_date DESC
        """, (seeker_id,))

        available_jobs = cursor.fetchall()

        if not available_jobs:
            print("Empty: No new jobs available to apply!")
            input("\nPress Enter to continue...")
            return

        for job in available_jobs:
            print(f"ID: {job[0]} | {job[1]} at {job[2]} ({job[3]})")
        print("-" * 60)

        # Now ask about job id
        job_id = input("\nEnter Job ID to apply: ")

        if not job_id.isdigit():
            print(":( Please enter a valid Job ID!")
            input("\nPress Enter to continue...")
            return

        # Find new application id
        cursor.execute("SELECT MAX(application_id) FROM Applications")
        result = cursor.fetchone()
        new_app_id = (result[0] or 0) + 1

        # Add application
        cursor.execute("""
            INSERT INTO Applications (application_id, job_id, seeker_id, apply_date, status)
            VALUES (:1, :2, :3, SYSDATE, 'Pending')
        """, (new_app_id, int(job_id), seeker_id))

        conn.commit()

        print(f":) Application submitted successfully!")

        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Application error: {e}")

    input("\nPress Enter to continue...")


def post_job():
    """Add new vacancies"""
    if not current_user_id:
        print(":( Please login first!")
        input("\nPress Enter to continue...")
        return

    if current_user_role != 'employer':
        print(":( Only employers can post jobs!")
        input("\nPress Enter to continue...")
        return

    print("\n" + "=" * 40)
    print("POST NEW JOB")
    print("=" * 40)

    job_title = input("Job Title: ")
    description = input("Description: ")
    location = input("Location: ")

    job_type = ""
    while job_type not in ['full-time', 'part-time', 'remote', 'internship']:
        job_type = input("Job Type (full-time/part-time/remote/internship): ").lower()
        if job_type not in ['full-time', 'part-time', 'remote', 'internship']:
            print(":( Invalid job type!")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Find employer id
        cursor.execute("SELECT employer_id FROM Employers WHERE user_id = :1", (current_user_id,))
        employer = cursor.fetchone()

        if not employer:
            print(":( Please complete your employer profile first!")
            print("Choose option 5 from main menu.")
            input("\nPress Enter to continue...")
            return

        employer_id = employer[0]

        # Find new job id
        cursor.execute("SELECT MAX(job_id) FROM Jobs")
        result = cursor.fetchone()
        new_job_id = (result[0] or 0) + 1

        # Add Vacancy
        cursor.execute("""
            INSERT INTO Jobs (job_id, employer_id, job_title, description, 
                            location, job_type, posted_date)
            VALUES (:1, :2, :3, :4, :5, :6, SYSDATE)
        """, (new_job_id, employer_id, job_title, description, location, job_type))

        conn.commit()

        print(f":) Job posted successfully! Job ID: {new_job_id}")

        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Job posting error: {e}")

    input("\nPress Enter to continue...")


def view_profile():
    """Show User Profile"""
    if not current_user_id:
        print(":( Please login first!")
        input("\nPress Enter to continue...")
        return

    print("\n" + "=" * 40)
    print("YOUR PROFILE")
    print("=" * 40)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # User Infos
        cursor.execute("""
            SELECT user_id, name, email, role, created_at 
            FROM Users WHERE user_id = :1
        """, (current_user_id,))

        user = cursor.fetchone()

        if user:
            print(f"User ID: {user[0]}")
            print(f"Name: {user[1]}")
            print(f"Email: {user[2]}")
            print(f"Role: {user[3]}")
            print(f"Member since: {user[4]}")
            print()

        # Additional Infos
        if current_user_role == 'jobseeker':
            cursor.execute("""
                SELECT skills, experience_years 
                FROM JobSeekers WHERE user_id = :1
            """, (current_user_id,))

            seeker = cursor.fetchone()
            if seeker:
                print(f"Skills: {seeker[0]}")
                print(f"Experience: {seeker[1]} years")
            else:
                print(f"Warning!  Profile not completed! Please complete your profile.")

            # My Applications
            cursor.execute("""
                SELECT a.application_id, j.job_title, a.apply_date, a.status
                FROM Applications a
                JOIN Jobs j ON a.job_id = j.job_id
                JOIN JobSeekers js ON a.seeker_id = js.seeker_id
                WHERE js.user_id = :1
                ORDER BY a.apply_date DESC
            """, (current_user_id,))

            applications = cursor.fetchall()
            print(f"\nYour Applications ({len(applications)}):")
            for app in applications:
                print(f"  - {app[1]} ({app[3]}) - Applied: {app[2]}")

        elif current_user_role == 'employer':
            cursor.execute("""
                SELECT company_name, location 
                FROM Employers WHERE user_id = :1
            """, (current_user_id,))

            employer = cursor.fetchone()
            if employer:
                print(f"Company: {employer[0]}")
                print(f"Location: {employer[1]}")
            else:
                print(f"Warning!  Company profile not completed! Please complete your profile.")

            # My Vacancies
            cursor.execute("""
                SELECT job_id, job_title, location, posted_date
                FROM Jobs WHERE employer_id = (
                    SELECT employer_id FROM Employers WHERE user_id = :1
                )
                ORDER BY posted_date DESC
            """, (current_user_id,))

            my_jobs = cursor.fetchall()
            print(f"\nYour Jobs ({len(my_jobs)}):")
            for job in my_jobs:
                print(f"  - {job[1]} (ID: {job[0]}) - {job[2]}")

        cursor.close()
        conn.close()

    except oracledb.Error as e:
        print(f":( Profile error: {e}")

    input("\nPress Enter to continue...")


def logout():
    """Log out"""
    global current_user_id, current_user_role

    if current_user_id:
        print(f"\n:) Goodbye! Logging out...")
    else:
        print("\nYou are not logged in.")

    current_user_id = None
    current_user_role = None

    input("Press Enter to continue...")


# ******************* MAIN MENU *******************
def display_menu():
    """Main Menu"""
    while True:
        print("\n" + "=" * 50)
        print("ONLINE JOB PORTAL SYSTEM")
        print("=" * 50)

        if current_user_id:
            print(f"👤 Logged in as: User ID {current_user_id} ({current_user_role})")
            print("-" * 50)

        print("1. Register")
        print("2. Login")
        print("3. Search Jobs")

        if current_user_id:
            if current_user_role == 'jobseeker':
                print("4. Apply for Job")
                print("5. Complete Profile")
                print("6. View My Profile")
            elif current_user_role == 'employer':
                print("4. Post New Job")
                print("5. Complete Profile")
                print("6. View My Profile")
            print("7. Logout")
        else:
            print("4. Apply for Job (Login required)")
            print("5. View My Profile (Login required)")
            print("6. Logout (Login required)")

        print("8. Exit")
        print("=" * 50)

        choice = input("Select an option (1-8): ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            search_jobs()
        elif choice == "4":
            if current_user_id:
                if current_user_role == 'jobseeker':
                    apply_job()
                elif current_user_role == 'employer':
                    post_job()
            else:
                print(":( Please login first!")
                input("Press Enter to continue...")
        elif choice == "5":
            if current_user_id:
                complete_profile()
            else:
                print(":( Please login first!")
                input("Press Enter to continue...")
        elif choice == "6":
            if current_user_id:
                view_profile()
            else:
                print(":( Please login first!")
                input("Press Enter to continue...")
        elif choice == "7":
            if current_user_id:
                logout()
            else:
                print(":( You are not logged in!")
                input("Press Enter to continue...")
        elif choice == "8":
            print("\n:) Thank you for using Job Portal System!")
            print("Exiting program...")
            break
        else:
            print(":( Invalid option, please try again.")


# ******************* START PROGRAM *******************
if __name__ == "__main__":
    print("Loading: Connecting to database...")
    # Test connection
    try:
        conn = get_db_connection()
        if conn:
            print(":) Database connection successful!")
            conn.close()
        else:
            print(":( Database connection failed!")
            print("Please check your Oracle credentials and try again.")
            exit()
    except Exception as e:
        print(f":( Error: {e}")
        exit()

    display_menu()