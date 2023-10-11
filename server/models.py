from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4


db = SQLAlchemy()


def get_uuid():
    return uuid4().hex

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    #name = db.Column(db.String(120), nullable=False)

class Enrollment(db.Model):

    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    contact = db.Column(db.String(20))
    course = db.Column(db.String(255))
    course_id = db.Column(db.String(10))
    date = db.Column(db.String(10))

    def __init__(self, full_name, contact, course, course_id, date):
        self.full_name = full_name
        self.contact = contact
        self.course = course
        self.course_id = course_id
        self.date = date

if __name__ == '__main__':
    db.create_all()