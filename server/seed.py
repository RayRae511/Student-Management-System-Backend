from faker import Faker
from app import app, db
from models import Enrollment, User

fake = Faker()

def seed_data():
    with app.app_context():
        db.create_all()
        if not db.session.query(Enrollment).first():
            for _ in range(1, 11):  # Generate data for 10 enrollments
                enrollment = Enrollment(
                    student_id=fake.random_int(min=1, max=10),  # Assuming 10 students
                    student_name=fake.name(),
                    student_contact=fake.email(),
                    course_id=fake.random_int(min=1, max=5),  # Assuming 5 courses
                    course_name=fake.unique.job(),
                    enrollment_date=fake.date_time_between(start_date="-2y", end_date="now")
                )
                db.session.add(enrollment)
        
        if not db.session.query(User).first():
            for _ in range(1, 11):  # Generate data for 10 users
                user = User(
                    email=fake.email(),
                    password=fake.password()
                )
                db.session.add(user)

        db.session.commit()
if __name__== 'main':
    seed_data()