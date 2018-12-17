#Pygubu-based Toontown launcher script v1.2.3 by TheMaskedMeowth (for Toontown Rewritten and Toontown Corporate Clash)
#This super epic script lets you log in at light speeds not previously known to mankind AND it looks cool too
#Requirements: python 3.7, you have to put this file and guiLauncher.ui in your game folder
#The other script, launcher.py, is a command prompt-based version of this. They both use the same credentials.json to save accounts, so you can use them interchangably.

import subprocess, os, sys, msvcrt, tkinter as tk
try:
	import requests, win32gui, win32con, win32com.shell.shell as shell, pygubu
except:
	subprocess.check_call(["py", '-m', 'pip', 'install', 'requests'])
	subprocess.check_call(["py", '-m', 'pip', 'install', 'pywin32'])
	subprocess.check_call(["py", '-m', 'pip', 'install', 'pygubu'])
	import requests, win32gui, win32con, win32com.shell.shell as shell, pygubu
	
class Application:
	def __init__(self, master, credentials, winName):
		usernames = ""
		for i in credentials:
			usernames += "\"" + i[u'username'] + "\" "	
		self.builder = builder = pygubu.Builder()
		try:
			builder.add_from_file('guiLauncher.ui')
		except:
			exitLauncher("Please make sure that guiLauncher.ui is in the same folder as this script! Press any key to exit...")
		self.mainwindow = builder.get_object(winName, master)
		if winName == "newAccount":
			builder.connect_callbacks({'onNAGoClick': self.onNAGoClick})
		elif winName == "main":
			builder.connect_callbacks({'onGoClick': self.onGoClick})
			self.builder.get_object('accountList').configure(values=usernames)
	
	def onGoClick(self):
		username = self.builder.get_object('accountList').get()
		option = self.builder.get_object('otherOptions').get()
		if option == "New Account":
			self.mainwindow.master.destroy()
			account = launchWindow("newAccount")	
		else:
			account = ""
			for i in credentials:
				if username == i[u'username']:
					account = i
			if account == "":
				return
			vb = True
			rs = False
			if option == "No Verbose Output":
				vb = False
			elif option == "Restart on Exit":
				rs = True
			win32gui.ShowWindow(cmdWindow,win32con.SW_NORMAL)
			win32gui.SetForegroundWindow(cmdWindow)
			self.mainwindow.master.destroy()
			if game == 'C':
				startCC(account, vb, rs)
			elif game == 'R':
				startTTR(account, vb, rs)
			
	def onNAGoClick(self):
		account = {'username': self.builder.get_object('unField').get(), 'password': self.builder.get_object('passField').get()}
		win32gui.ShowWindow(cmdWindow,win32con.SW_NORMAL)
		win32gui.SetForegroundWindow(cmdWindow)
		self.mainwindow.master.destroy()
		if game == 'C':
			t = startCC(account, False, False)
		elif game == 'R':
			t = startTTR(account, False, False)
		if t:
			credentials.append(account)
			with open('credentials.json', 'w') as f:
				f.write(str(credentials))

def launchWindow(winName):
	win32gui.ShowWindow(cmdWindow, win32con.SW_MINIMIZE)
	root = tk.Tk()
	app = Application(root, credentials, winName)
	root.title("Toontown Launcher")
	root.mainloop()
	
def exitLauncher(message):
	print(message)
	junk = msvcrt.getch()
	os.system("cls")
	sys.exit()
	
def startCC(tc, vb, rs):
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
		launchWindow(winName)
		return False
		
def startTTR(tc, vb, rs):
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
		print("Oof! Login failed with no error code.")
		launchWindow(winName)
		return False
		
def spHandler(gw, tc, rs):
	import time
	while True:
		time.sleep(3)
		poll = gw.poll()
		if poll != None:
			if rs:
				if game == 'C':
					startCC(tc, True, True)
				elif game == 'R':
					startTTR(tc, True, True)
			else:
				launchWindow("main")
				break
	
def decGlobals():
	globals = []
	p = os.path.split(os.path.normpath(sys.path[0]))[1]
	if p == "Corporate Clash":
		globals.append('C')
	elif p == "Toontown Rewritten":
		if shell.IsUserAnAdmin():
			globals.append('R')
		else:
			exitLauncher("This script must be run as an administrator in order to launch Toontown Rewritten. Press any key to exit...")
	else:
		exitLauncher("Please put this file in your Corporate Clash or Toontown Rewritten folder. Press any key to exit...")
	globals.append(win32gui.GetForegroundWindow())
	globals.append([])
	globals.append("")
	try:
		globals[2] = eval(open('credentials.json', 'r').read())
		globals[3] = "main"
	except:
		globals[3] = "newAccount"
	return globals

game, cmdWindow, credentials, winName = decGlobals()
launchWindow(winName)