#made by TheMaskedMeowth, this super epic script lets you log in at light speeds not previously known to mankind
#requirements: python 2.7, requests library (just do pip install requests on command prompt after you get python), you gotta put it in your TTR folder or else it wont work lol

from __future__ import print_function
import os
import msvcrt
import subprocess

def login():
	sm = ''
	outer = ''
	if len(credentials) == 1:
		info = "Press enter to launch the game, or enter argument characters (use \"h\" for info): "
	else:
		info = "Enter numbers between 0 and " + chr(47 + len(credentials)) + " for accounts, or argument characters (use \"h\" for info): "
	while True:
		if len(credentials) == 1:
			sm = ''
		print(info + sm + outer + '			   ', end='\r')
		x = msvcrt.getch()
		if sm.find(x) != -1:
			pass
		elif x == '\r':
			break
		elif x == 'o' or x == 'n' or x == 'e' or x == 'h' or x == 'a' or x == 'r' or x == 'u':
			outer = x
		elif ord(x) == 8:
			if outer != '':
				outer = ''
			else:
				sm = sm[:-1]
		elif ord(x) >= 48 and ord(x) <= len(credentials) + 47 and x not in sm:
			sm += x
	print(info + sm + outer)
	if len(credentials) == 1:
		sm = '0'
	if outer == 'n':
		newaccount()
	elif outer == 'h':
		help()
	elif outer == 'a':
		accountlist()
	elif outer == 'u':
		update()
	elif outer == 'e' or (outer == '' and sm == ''):
		return
	else:
		for c in sm:
			vb = False
			rs = False
			if c == sm[len(sm) - 1]:
				if outer != 'o':
					vb = True
				if outer == 'r':
					rs = True
			startgame(credentials[ord(c) - 48], vb, rs)
				
def startgame(tc, vb, rs):
	import requests
	import time
	url = ('https://www.toontownrewritten.com/api/login?format=json')
	r = requests.post(url, json=tc)
	response = r.json()
	success = response[u'success']
	if success == "delayed":
		queueToken = {'queueToken': response[u'queueToken']}
		delayed = True
		eta = response[u'eta']
		while delayed:
			print("You've been put into the queue. ETA: " + eta + " seconds", end='\r')
			time.sleep(5)
			r = requests.post(url, json=queueToken)
			response = r.json()
			success = response[u'success']
			if success == "true":
				delayed = False
			else:
				eta = response[u'eta']
	if success == "true":
		print("You've been put into the queue. ETA: 0 seconds")
		print("Welcome back to Toontown, " + tc[u'username'] + "!")
		os.environ["TTR_PLAYCOOKIE"] = r.json()[u'cookie']
		os.environ["TTR_GAMESERVER"] = r.json()[u'gameserver']
		if vb:
			print("Please note that verbose output only works for the last client opened.")
			clash = subprocess.Popen(args="TTREngine.exe")
			sphandler(clash, tc, rs)
		else:
			clash = subprocess.Popen(args="TTREngine.exe", creationflags=0x08000000)
		return True
	else:
		print("Oof! Login has failed. Press any key to restart...")
		junk = msvcrt.getch()
		os.system("cls")
		login()
		return False
	
def sphandler(clash, tc, rs):
	import time
	while True:
		time.sleep(3)
		poll = clash.poll()
		if poll != None:
			if rs:
				startgame(tc, True, True)
			else:
				login()
				break
				
def newaccount():
	un = raw_input("New Username: ")
	pw = ''
	while True:
		hpw = ''
		for c in pw:
			hpw += '*'
		print('New Password: ' + hpw + '										 ', end='\r')
		x = msvcrt.getch()
		if x == '\r':
			break
		elif ord(x) == 8:
			pw = pw[:-1]
		elif ord(x) >= 33 and ord(x) <= 126:
			pw += x
	print('New Password: ' + hpw)
	tc = {'username': un, 'password': pw,}
	t = startgame(tc, False, False)
	if t:
		credentials.append(tc)
		with open('credentials.json', 'w') as f:
			f.write(str(credentials))

def accountlist():
	for i in range(0, len(credentials)):
		print(str(i) + ": " + credentials[i][u'username'])
	login()

def help():
	print("So basically the numbers you put in are going to correspond to the accounts, and letters you put in each correspond to \n\"arguments\" you can use. Right now there are 6 arguments: \no: Launches the game as normal, but turns verbose output off and closes the launcher after\nr: Causes the game to immediately restart after it closes\nh: Accesses this help screen\nn: Allows you add a new account to your credentials list\na: Displays a list of usernames in your credentials list\ne: Exits the launcher\nPress any key when you're done with this dialog to restart.")
	junk = msvcrt.getch()
	os.system("cls")
	login()

credentials = []
logincheck = False
try:
	credentials = eval(open('credentials.json', 'r').read())
	logincheck = True
except:
	newaccount()
if logincheck:
	login()
