import sys
import requests
from pyquery import PyQuery as pq

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

def get_course_content(degree, unit, plan, course):
	"""Returns the content for the specified subject.
	This data must be somehow parsed so that it becomes useful."""
	payload = {'carreraId': degree, 'unidadId': unit, 'planId': plan, 'materiaId': course}
	r = session.get(url = 'http://www.austral.edu.ar/portal/materias/notasmateria', params=payload)
	# print(r.status_code) # Only for testing purposes, remove
	# print(r.text) # Only for testing purposes, remove

def get_info(page):
	"""Information that is needed for other requests."""
	d = pq(page.text)
	degree = d('#selectedCarreraId').attr['value']
	unit = d('#selectedUnidadId').attr['value']
	plan = d('#selectedPlanId').attr['value']
	return (degree, unit, plan)


# We need to get the ids of all the courses
def get_all_courses(page):
	"""Returns an array with the ids of all the courses"""
	# We could avoid looking for data from certain types of courses
	d = pq(page.text)

	results = d.find('a').filter(lambda i: pq(this).attr('data-url') != None)
	courses = list()
	for result in results:
		# This can probably be done with queries.
		courses.append(pq(result).attr['data-url'].split('=')[-1])
	courses = list(dict.fromkeys(courses))
	courses.remove('')
	courses.remove('[legajo]')
	return courses

# We need a way to get the ids of all the subjects
# Should they be called subjects or courses?

page = login(sys.argv[1], sys.argv[2])

degree, unit, plan = get_info(page)

print(get_average(page))

print(get_all_courses(page))

get_course_content(degree, unit, plan, 'AL1')

#print(average)