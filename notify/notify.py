import shlex, subprocess
import platform
from flask import Flask
from flask import request

# A very simple app to display notifications
app = Flask(__name__)

global notification_command # The command to show the notification.

if (platform.system() == 'Darwin'):
	# Command for mac
	notification_command = 'osascript -e \'display notification "{1}" with title "{0}"\''

if (platform.system() == 'Linux'):
	# Command for linux
	notification_command = 'notify-send "{0}, {1}"'

if (platform.system() == 'Windows'):
	# Command for window
	notification_command = ''

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/notify", methods=['POST'])
def notify():
	data = request.get_json()
	title = data['title']
	description = data['description']

	command_line = notification_command.format(title, description)
	args = shlex.split(command_line)
	subprocess.call(args)

	return "Notified"