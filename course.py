class Course:

    def __init__(self, name, id, exams):
        self.name = name
        self.id = id
        self.exams = exams

class Exam:
    def __init__(self, name, score):
        self.name = name
        self.score = score
