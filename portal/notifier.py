import requests

session = requests.Session()
url = "http://localhost"
method = "/notify"

def send_notification(exam, port = 5000):
    session.post(url + ":" + str(port) + method, json={'title': "New Exam!", 'description': exam.name + " " + exam.score})

def send_notifications(exams, port = 5000): 
    session.post(url + ":" + str(port) + method, json={'title': "New exams", 'description': "You have " + str(len(exams)) + " new exams!"})