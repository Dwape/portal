from portal import get_courses
from sqlalchemy.orm import sessionmaker
from course import Base, Course, Exam
import sys, sched, time, notifier

def get_courses_db(session):
    return session.query(Course).all()

def get_course_by_id(session, id):
    return session.query(Course).filter_by(id = id).first()

def connect_to_db():
    # Should be moved to another file
    from sqlalchemy import create_engine
    engine = create_engine('mysql+pymysql://user:password@localhost:1234/portal_db')

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker()
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    
    return Session()

def contains_course(courses, id):
    for course in courses:
        if(course.id == id): 
            return (True, course)
    return False

def contains_exam(exams, newExam):
    for exam in exams:
        if(exam.order == newExam.order): 
            return (True, exam)
    return (False, None)

def add_new(entity, session):
    session.add(entity)
    session.commit()

def update_exam(id, score, session):
    exam = session.query(Exam).filter_by(id = id).first()
    exam.score = score
    session.commit()

def compare_courses(new_courses, session):
    new_exams = list()
    for course in new_courses:
        old_course = get_course_by_id(session, course.id)
        if(old_course == None):
            add_new(course, session)
            for exam in course.exams:
                new_exams.append(exam)
            continue
        for exam in course.exams:
            (result, old_exam) = contains_exam(old_course.exams, exam)
            if result and (exam.score != old_exam.score):
                new_exams.append(exam)
                update_exam(old_exam.id, exam.score, session)
            elif(not result):
                new_exams.append(exam)
                add_new(exam, session)
    return new_exams

def print_courses(courses):
    print(reduce((lambda x,y: x + "\n\n" + y), map((lambda x: x.__str__()), courses)) if len(courses) > 0 else "\U0001F55C searching")

def schedule_task(scheduler, time, session):
    new_courses = get_courses(sys.argv[1], sys.argv[2])
    new_exams = compare_courses(new_courses, session)
    if (len(new_exams) > 1):
        notifier.send_notifications(new_exams)
    elif (len(new_exams) > 0):
        notifier.send_notification(new_exams[0])
    print_courses(new_exams)
    scheduler.enter(time, 1, schedule_task, (scheduler, time, session))

def main():
    session = connect_to_db()
    s = sched.scheduler(time.time, time.sleep)
    schedule_task(s, 10, session)
    s.run()


main()
