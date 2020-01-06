import PySimpleGUI as sg
import getpass
from datetime import datetime
import re

def cleanup(string):
	return re.sub(r'\W+', '_', string)

def savecredential(values):
	basepath = '/path/to/encrypted/volume'
	title = values['_TITLE_']
	mytimestamp = cleanup( datetime.today().strftime('%Y-%m-%d-%H:%M:%S') )
	fullpath = basepath + "/" + values['_RECIPIENT_'] + "/" + cleanup(title) + "_" + mytimestamp + ".txt"

	sharedby = getpass.getuser()

	output_text = "[Title:]\t%s\n[Shared by:]\t%s\n[URL:]\t\t%s\n[Accnt email:]\t%s\n[Username:]\t%s\n[Password:]\t%s\n[Notes:]\n%s\n[Date:]\t%s\n" % (title, sharedby, values['_URL_'], values['_EMAIL_'], values['_USERNAME_'], values['_PASSWORD_'], values['_NOTES_'], mytimestamp)

	output_file = open(fullpath, 'w')
	output_file.write(output_text)
	output_file.close()
	sg.Popup(event, 'Saved')

layout = [  [sg.Text('Share Password Locally', font='FreeSans 16')],
			[sg.Text('Share theses credentials with (Superhero name)'), sg.Combo(('user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'group1', 'group2', 'group3', 'everyone'), size=(12,1), key='_RECIPIENT_')],
			[sg.Text('Site Title   '), sg.InputText('', do_not_clear=False, key='_TITLE_')],
			[sg.Text('Site URL  '), sg.InputText('https://', do_not_clear=True, key='_URL_')],
			[sg.Text('Acct email'), sg.InputText('account@example.org', do_not_clear=True, key='_EMAIL_')],
			[sg.Text('Username'), sg.InputText('', do_not_clear=True, key='_USERNAME_')],
			[sg.Text('Password'), sg.InputText('use HSXKPasswd to create one if needed', do_not_clear=False, key='_PASSWORD_')],
			[sg.Text('Notes'), sg.Multiline('', size=(47,8), do_not_clear=False, key='_NOTES_')],
			[sg.Button('Save'), sg.Button('Exit')] ]

window = sg.Window('Share Password Locally', layout)

while True:
	event, values = window.read()
	if event in (None, 'Exit', 'Quit'):
		exit()
	if event in ('Save'):
		savecredential(values)
		
window.close()


