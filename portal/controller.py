from portal import get_courses
from sqlalchemy.orm import sessionmaker
from course import Base, Course, Exam
import sys, sched, time, notifier

def get_courses_db(session):
    """Returns all the courses from the database"""
    return session.query(Course).all()

def get_course_by_id(session, id):
    """Searches the course with the corresponding id in the database and returns it"""
    return session.query(Course).filter_by(id = id).first()

def connect_to_db():
    """Connects to the mysql database and returns the session"""
    from sqlalchemy import create_engine
    engine = create_engine('mysql+pymysql://user:password@localhost:1234/portal_db')

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker()
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    
    return Session()

def contains_exam(exams, newExam):
    """Checks if the newExam is contained in the exams list.
    Returns True and the exam contained in the list if it founds a match.
    Returns False and None if it is not contained
    """
    for exam in exams:
        if(exam.order == newExam.order): 
            return (True, exam)
    return (False, None)

def add_new(entity, session):
    """Adds a new course or exam to the database"""
    session.add(entity)
    session.commit()

def update_exam(id, score, session):
    """Updates the exam in the database"""
    exam = session.query(Exam).filter_by(id = id).first()
    exam.score = score
    session.commit()

def compare_courses(new_courses, session):
    """Compares the exams from the new courses with ones in the database.
    If the exams don't exist or their score is outdated, they are updated in the database.
    
    Returns the exams updated.
    """
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
    """Prints courses or exams"""
    print(reduce((lambda x,y: x + "\n\n" + y), map((lambda x: x.__str__()), courses)) if len(courses) > 0 else "\U0001F55C searching")

def schedule_task(scheduler, time, session):
    """Get the new exams and sends them to the notifier. 
    
    It executes every x seconds.
    """
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
