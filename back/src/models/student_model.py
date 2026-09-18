from src.models import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.column(db.Integer, primary_key=True, autoincremente = True)
    name = db.column(db.String(50),nullable=False)
    age = db.column(db.Interger,nullable=True)

    def __repr__(self):
        return f"<Student {self.name}>"