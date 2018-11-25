#Toontown Corporate Clash & Toontown Rewritten launcher script v1.1
#made by TheMaskedMeowth, this super epic script lets you log in at light speeds not previously known to mankind
#requirements: python 3.7, requests library (just do pip install requests on command prompt after you get python), you have to put this file in your game folder

import os
import sys
import msvcrt
import subprocess
import win32com.shell.shell as shell

def login():
	sm = ''
	outer = ''
	if len(credentials) == 1:
		info = "Press enter to launch the game, or enter argument characters (use \"h\" for info): "
	else:
		info = "Enter numbers between 0 and " + chr(47 + len(credentials)) + " for accounts, or argument characters (use \"h\" for info): "
	while True:
		if len(credentials) == 1:
			sm = ""
		print(info + sm + str(outer) + '			   ', end='\r')
		lol = msvcrt.getch()
		x = chr(int.from_bytes(lol, byteorder='big'))
		if sm.find(str(x)) != -1:
			pass
		elif x == '\r':
			break
		elif x == 'o' or x == 'r' or x == 'd' or x == 'p' or x == 'n' or x == 'e' or x == 'h' or x == 'a' or x == 'u':
			outer = x
		elif ord(x) == 8:
			if outer != '':
				outer = ''
			else:
				sm = sm[:-1]
		elif ord(x) >= 48 and ord(x) <= len(credentials) + 47 and str(x) not in sm:
			sm += str(x)
	print(info + sm + str(outer))
	if len(credentials) == 1:
		sm = '0'
	if outer == 'd':
		debugstart()
	elif outer == 'p':
		population()
	elif outer == 'n':
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
			if game == 'C':
				startCC(credentials[ord(c) - 48], vb, rs)
			elif game == 'R':
				startTTR(credentials[ord(c) - 48], vb, rs)
				
def startCC(tc, vb, rs):
	import requests
	url = ('https://corporateclash.net/api/v1/login/' + tc[u'username'])
	r = requests.post(url, json=tc)
	if r.json()[u'reason'] == 1000 or r.json()[u'reason'] == 0:
		print("Welcome back to Toontown, " + tc[u'username'] + "!")
		os.environ["TT_PLAYCOOKIE"] = r.json()[u'token']
		os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
		if vb:
			gw = subprocess.Popen(args="CorporateClash.exe")
			spHandler(gw, tc, rs)
		else:
			gw = subprocess.Popen(args="CorporateClash.exe", creationflags=0x08000000)
		return True
	else:
		print("Login failed with error code " + str(r.json()[u'reason']) + ". (" + str(r.json()[u'friendlyreason']) + ")")
		print("Press any key to restart...")
		junk = msvcrt.getch()
		os.system("cls")
		login()
		return False
		
def startTTR(tc, vb, rs):
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
			gw = subprocess.Popen(args="TTREngine.exe")
			spHandler(gw, tc, rs)
		else:
			gw = subprocess.Popen(args="TTREngine.exe", creationflags=0x08000000)
		return True
	else:
		print("Oof! Login has failed. Press any key to restart...")
		junk = msvcrt.getch()
		os.system("cls")
		login()
		return False
		
def debugStart():
	os.environ["TT_PLAYCOOKIE"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
	clash = subprocess.Popen(args="CorporateClash.exe")
	
def spHandler(gw, tc, rs):
	import time
	print("Please note that verbose output only works for the last client opened.")
	while True:
		time.sleep(3)
		poll = gw.poll()
		if poll != None:
			if rs:
				startgame(tc, True, True)
			else:
				login()
				break

def population():
	import requests
	url = 'https://corporateclash.net/api/v1/districts/'
	r = requests.get(url).json()
	population = 0
	for a in r:
		population += a[u'population'] 
	print("There are currently " + str(population) + " people in-game.")
	login()
	
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
		print(chr(i + 48) + " - " + credentials[i][u'username'])
	login()

def clashHelp():
	print("So basically the numbers you put in are going to correspond to the accounts, and letters you put in each correspond to \n\"arguments\" you can use. Right now there are 6 arguments: \no: Launches the game as normal, but turns verbose output off and closes the launcher after\nr: Causes the game to immediately restart after it closes\nh: Accesses this help screen\np: Shows the current in-game population\nn: Allows you add a new account to your credentials list\na: Displays a list of usernames in your credentials list\nd: Launches the game without a playcookie for limited debug purposes.\ne: Exits the launcher\nPress any key when you're done with this dialog to restart.")
	junk = msvcrt.getch()
	os.system("cls")
	login()
	
def ttrHelp():
	print("So basically the numbers you put in are going to correspond to the accounts, and letters you put in each correspond to \n\"arguments\" you can use. Right now there are 6 arguments: \nh: Accesses this help screen\nn: Allows you add a new account to your credentials list\na: Displays a list of usernames in your credentials list\ne: Exits the launcher\nPress any key when you're done with this dialog to restart.")
	junk = msvcrt.getch()
	os.system("cls")
	login()

game = ''
p = os.path.split(os.path.normpath(sys.path[0]))[1]
if p == "Corporate Clash":
	game = 'C'
elif p == "Toontown Rewritten":
	if shell.IsUserAnAdmin():
		game = 'R'
	else:
		print("This script must be run as an administrator in order to launch Toontown Rewritten. Press any key to exit...")
		junk = msvcrt.getch()
		os.system("cls")
		sys.exit()
else:
	print("Please put this file in your Corporate Clash or Toontown Rewritten folder. Press any key to exit...")
	junk = msvcrt.getch()
	os.system("cls")
	sys.exit()
credentials = []
logincheck = False
try:
	credentials = eval(open('credentials.json', 'r').read())
	logincheck = True
except:
	newaccount()
if logincheck:
	login()