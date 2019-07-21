import sys
import requests
import urllib
from pyquery import PyQuery as pq
from requests.models import Response
from course import Course, Exam
from functools import reduce

global session # Try to remove this global variable
session = requests.Session()

def login(user, password):
	"""Logs the user and returns the response"""
	token = get_verification_token()
	payload = {'__RequestVerificationToken': token, 'TipoDeDocId': 'D', 'NroDoc': user, 'Clave': password, 'Recordarme':False}
	cookies = session.cookies # We need to send the cookies
	r = session.post('http://www.austral.edu.ar/portal/Cuenta/IniciarSesion', data=payload, cookies=cookies) # Do the cookies need to be added manually here?
	
	d = pq(r.text)
	message = d('#status-message').find('span').text()
	if(message != ""):
		print(message)
		raise ValueError('Error while trying to login')
	
	return r

def get_verification_token():
	"""Returns the verification token required for the login request"""
	URL = 'http://www.austral.edu.ar/portal/'
	r = session.get(url = URL)
	d = pq(r.text)
	# Is this token acutally needed?
	return d('[name=__RequestVerificationToken]').attr['value'] # This token is sent in the form

def get_average(page):
	"""Finds the user's grade point average"""
	d = pq(page.text)
	return d('#lblPromedio').find('span').text()

def get_course_content(degree, unit, plan, courseId):
	"""Returns the content for the specified subject.
	This data must be somehow parsed so that it becomes useful."""
	payload = {'carreraId': degree, 'unidadId': unit, 'planId': plan, 'materiaId': courseId}
	r = session.get(url = 'http://www.austral.edu.ar/portal/materias/notasmateria', params=payload)
	return r

def get_course_exams(course, content):
	"""Returns a new course with exams assigned"""
	text = pq(content.text)
	
	exams = list()
	
	rows = text.find('tr')
	i = 0
	for row in rows:
		cells = pq(row).find('td')
		if(cells.length > 3):
			name = urllib.unquote(pq(cells[0]).text())
			score = pq(cells[cells.length - 1]).text()
			exams.append(Exam(name, score, i))
			i += 1

	# tables = text.find('table')
	# for table in tables:
	# 	query_table = pq(table)
	# 	group = query_table.find('th')[0].text
	# 	rows = query_table.find('tr')
	# 	for row in rows:
	# 		cells = pq(row).find('td')
	# 		if(cells.length > 3):
	# 			name = urllib.unquote(pq(cells[0]).text())
	# 			score = pq(cells[cells.length - 1]).text()
	# 			exams.append(Exam(name, score, group))

	return Course(course.name, course.id, exams)

def get_info(page):
	"""Information that is needed for other requests."""
	d = pq(page.text)
	degree = d('#selectedCarreraId').attr['value']
	unit = d('#selectedUnidadId').attr['value']
	plan = d('#selectedPlanId').attr['value']
	return (degree, unit, plan)


def get_all_courses(page):
	"""Returns an array with all the courses"""
	# We could avoid looking for data from certain types of courses
	# We could add a year to the courses but we would need to get them in another way.
	d = pq(page.text)

	# results = d.find('a').filter(lambda i: pq(this).attr('data-url') != None) # It gets you all the links from the course row so a lot of courses will be repeated
	results = d('[class=" modalAction"]') # It gets you only the courses that you have a score.
	courses = list()
	for result in results:
		query = pq(result)	
		# This can probably be done with queries.
		id = query.attr['data-url'].split('=')[-1]
		courses.append(Course(query.attr['data-title'].split('=')[-1], urllib.unquote(id), list()))
	courses = list(dict.fromkeys(courses))
	# courses.remove('')
	return list(filter((lambda x: x.id != '[legajo]'), courses))

# User and password will be ignored.
def fake_login(user, password):
	response = Response()
	response.code = 'ok'
	response.status_code = 200  # Check if this code is correct
	with open('pages/main.txt', 'r') as file:
		response._content = file.read()
	return response

def fake_get_course_content(degree, unit, plan, course):
	response = Response()
	response.code = 'ok'
	response.status_code = 200  # Check if this code is correct
	with open('pages/course.txt', 'r') as file:
		response._content = file.read()
	return response

def get_courses(username, password):
	"""Returns all the courses with scores"""
	page = login(username, password)
	degree, unit, plan = get_info(page)
	courses = get_all_courses(page)
	return list(map((lambda x: get_course_exams(x, get_course_content(degree, unit, plan, x.id))), courses))

# result = get_courses(sys.argv[1], sys.argv[2])