from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, ForeignKey, func, Float, Integer
from sqlalchemy.orm import relationship, backref
from functools import reduce

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    id = Column(String(255), primary_key = True) # The length of the id could be shorter
    name = Column(String(255))
    exams = relationship("Exam", backref="course", cascade="all,delete")

    def __init__(self, name, id, exams = list()):
        self.name = name
        self.id = id
        self.exams = exams
        super(Course, self).__init__()

    def __str__(self):
        return self.name + " [" + self.id + "]\n" + (reduce((lambda x, y: x + '\n' + y), map((lambda x: '\t' + x.__str__()), self.exams)) if len(self.exams) > 0 else "")

class Exam(Base):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(255))
    score = Column(String(255))
    course_id = Column(String(255), ForeignKey('course.id'))
    
    def __init__(self, name, score):
        self.name = name
        self.score = score
        super(Exam, self).__init__()
    
    def __str__(self):
        return self.name + " " + self.score



# # Only for testing purposes
# e = Exam("Final", 3)
# e2 = Exam("Parcial", 10)
# c = Course("Analisis", "AL1", [e,e2])

# s = Session()
# course = s.query(Course).filter_by(id = "AL1").first()
# if(course is not None):
#     # deletes all the exams
#     s.delete(course) 

# # Add all the exams
# s.add(c)
# s.commit()
# courses = s.query(Course).all()
# print(len(courses[0].exams))

