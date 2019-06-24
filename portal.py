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
	r = session.post('http://www.austral.edu.ar/portal/Cuenta/IniciarSesion', data=payload, cookies=cookies)
	return r

def get_verification_token():
	"""Returns the verification token required for the login request"""
	URL = 'http://www.austral.edu.ar/portal/'
	r = session.get(url = URL)
	d = pq(r.text)
	return d('[name=__RequestVerificationToken]').attr['value'] # This token is sent in the form

def get_average():
	"""Finds the user's average"""
	user = sys.argv[1]
	password = sys.argv[2]
	response = login(user, password)
	d = pq(response.text)
	return d('#lblPromedio').find('span').text()


average = get_average()

print(average)