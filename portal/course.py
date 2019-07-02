from functools import reduce

class Course:

    def __init__(self, name, id, exams = list()):
        self.name = name
        self.id = id
        self.exams = exams

    def to_string(self):
        return self.name + " [" + self.id + "]\n" + (reduce((lambda x, y: x + '\n' + y), map((lambda x: '\t' + x.to_string()), self.exams)) if len(self.exams) > 0 else "")

class Exam:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def to_string(self):
        return self.name + " " + self.score
