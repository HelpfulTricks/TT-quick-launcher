#made by TheMaskedMeowth, this super epic script lets you log in hella frickin quick
#requirements: python 2.7, requests library, you gotta put it in your TTCC folder or else it wont work lol

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
		elif x == 'o' or x == 'd' or x == 'n' or x == 'e' or x == 'h' or x == 'a' or x == 'r' or x == 'u':
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
	if outer == 'd':
		debugstart()
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
			startgame(credentials[ord(c) - 48], vb, rs)
				
def startgame(tc, vb, rs):
	import requests
	url = ('https://corporateclash.net/api/v1/login/')
	r = requests.post(url, json=tc)
	if r.json()[u'reason'] == 1000 or r.json()[u'reason'] == 0:
		print("Welcome back to Toontown, " + tc[u'username'] + "!")
		os.environ["TT_PLAYCOOKIE"] = r.json()[u'token']
		os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
		if vb:
			print("Please note that verbose output only works for the last client opened.")
			clash = subprocess.Popen(args="CorporateClash.exe")
			sphandler(clash, tc, rs)
		else:
			clash = subprocess.Popen(args="CorporateClash.exe", creationflags=0x08000000)
		return True
	else:
		print("Login failed with error code " + str(r.json()[u'reason']) + ". (" + str(r.json()[u'friendlyreason']) + ")")
		print("Press any key to restart...")
		junk = msvcrt.getch()
		os.system("cls")
		login()
		return False
		
def debugstart():
	os.environ["TT_PLAYCOOKIE"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
	clash = subprocess.Popen(args="CorporateClash.exe")
	
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
	t = startgame()
	if t:
		credentials.append(tc)
		with open('credentials.json', 'w') as f:
			f.write(str(credentials))

def accountlist():
	for i in range(0, len(credentials)):
		print(str(i) + ": " + credentials[i][u'username'])
	login()

def help():
	print("So basically the numbers you put in are going to correspond to the accounts, and letters you put in each correspond to \n\"arguments\" you can use. Right now there are 6 arguments: \no: Launches the game as normal, but turns verbose output off and closes the launcher after\nr: Causes the game to immediately restart after it closes\nh: Accesses this help screen\nn: Allows you add a new account to your credentials list\na: Displays a list of usernames in your credentials list\nd: Launches the game without a playcookie for limited debug purposes.\ne: Exits the launcher\nPress any key when you're done with this dialog to restart.")
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
