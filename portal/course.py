from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, ForeignKey, func, Float, Integer
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    id = Column(String(255), primary_key = True) # The length of the id could be shorter
    name = Column(String(255))
    exams = relationship("Exam", backref="course", cascade="all,delete")

    def __init__(self, name, id, exams):
        self.name = name
        self.id = id
        self.exams = exams
        super(Course, self).__init__()

class Exam(Base):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(255))
    score = Column(Float)
    course_id = Column(String(255), ForeignKey('course.id'))
    def __init__(self, name, score):
        self.name = name
        self.score = score
        super(Exam, self).__init__()


# Should be moved to another file
from sqlalchemy import create_engine
engine = create_engine('mysql://user:password@localhost:1234/portal_db')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

# Only for testing purposes
e = Exam("Final", 3)
e2 = Exam("Parcial", 10)
c = Course("Analisis", "AL1", [e,e2])

s = Session()
course = s.query(Course).filter_by(id = "AL1").first()
if(course is not None):
    # deletes all the exams
    s.delete(course) 

# Add all the exams
s.add(c)
s.commit()
courses = s.query(Course).all()
print(len(courses[0].exams))

