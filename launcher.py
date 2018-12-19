#Pygubu-based Toontown launcher script v1.3.1 by TheMaskedMeowth (for Toontown Rewritten and Toontown Corporate Clash)
#This super epic script lets you log in pretty fast, and it's all self-contained within one little file
#Requirements: You'll need python 3.7, and you'll have to put this file in your game folder

import subprocess, time, os, sys, msvcrt, tkinter as tk, _thread as thread
try:
	import requests, win32gui, win32con, win32com.shell.shell as shell, pygubu
except:
	subprocess.check_call(["py", '-m', 'pip', 'install', 'requests'])
	subprocess.check_call(["py", '-m', 'pip', 'install', 'pywin32'])
	subprocess.check_call(["py", '-m', 'pip', 'install', 'pygubu'])
	import requests, win32gui, win32con, win32com.shell.shell as shell, pygubu
	
class Application:
	def __init__(self, master):
		self.builder = builder = pygubu.Builder()
		builder.add_from_string(xmlData)
		self.mainwindow = builder.get_object(winName, master)
		builder.connect_callbacks(self)
		if game == 'C' and winName == "main":
			thread.start_new_thread(popTracker, (self,))
		if len(usernames) == 1:
			self.builder.get_variable('acct0').set(True)
	
	def onGoClick(self):
		accList = []
		for u in usernames:
			if self.builder.get_variable('acct' + str(usernames.index(u))).get():
				for a in credentials:
					if u == a[u'username']:
						accList.append(a)
		if accList != []:
			win32gui.ShowWindow(cmdWindow,win32con.SW_NORMAL)
			win32gui.SetForegroundWindow(cmdWindow)
			popWindowChecker = False
			self.mainwindow.master.destroy()
			options = {'vb': False, 'rs': False, 'cl': False}
			for a in accList:
				if len(accList) - 1 == accList.index(a):
					options = {'vb': not self.builder.get_variable('vb').get(), 'rs': self.builder.get_variable('rs').get(), 'cl': self.builder.get_variable('cl').get()}
				if game == 'C':
					startCC(a, options)
				elif game == 'R':
					startTTR(a, options)
	
	def onNAClick(self):
		popWindowChecker = False
		self.mainwindow.master.destroy()
		launchWindow("newAccount")

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
				
	def onClCheck(self):
		if self.builder.get_variable('cl').get():
			self.builder.get_object('noVerbose').configure(state='disabled')
			self.builder.get_variable('vb').set(False)
			self.builder.get_object('restart').configure(state='disabled')
			self.builder.get_variable('rs').set(False)
		else:
			self.builder.get_object('noVerbose').configure(state='normal')
			self.builder.get_object('restart').configure(state='normal')
			
def popTracker(self):
	while popWindowChecker:
		url = 'https://corporateclash.net/api/v1/districts/'
		r = requests.get(url).json()
		population = 0
		for a in r:
			population += a[u'population']
		if popWindowChecker:
			self.builder.get_object('popTracker').configure(text='Population: ' + str(population))
			time.sleep(10)
			
def launchWindow(winName):
	root = tk.Tk()
	app = Application(root)
	if game == 'C':
		winTitle = "Corporate Clash Launcher"
	elif game == 'R':
		winTitle = "Toontown Rewritten Launcher"
	root.title(winTitle)
	win32gui.ShowWindow(cmdWindow, win32con.SW_MINIMIZE)
	root.iconbitmap("Launcher.exe")
	root.mainloop()
	
def exitLauncher(message):
	print(message)
	junk = msvcrt.getch()
	os.system("cls")
	sys.exit()
	
def startCC(tc, options):
	url = ('https://corporateclash.net/api/v1/login/' + tc[u'username'])
	r = requests.post(url, json=tc)
	if r.json()[u'reason'] == 1000 or r.json()[u'reason'] == 0:
		print("Welcome back to Toontown, " + tc[u'username'] + "!")
		os.environ["TT_PLAYCOOKIE"] = r.json()[u'token']
		os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
		if options[u'vb'] and not options[u'cl']:
			gw = subprocess.Popen(args="CorporateClash.exe")
		else:
			gw = subprocess.Popen(args="CorporateClash.exe", creationflags=0x08000000)
		if not options[u'cl']:
			spHandler(gw, tc, options)
		return True
	else:
		print("Login failed with error code " + str(r.json()[u'reason']) + ". (" + str(r.json()[u'friendlyreason']) + ")")
		launchWindow(winName)
		return False
		
def startTTR(tc, options):
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
			time.sleep(3)
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
		if options[u'vb'] and not options[u'cl']:
			gw = subprocess.Popen(args="TTREngine.exe")
		else:
			gw = subprocess.Popen(args="TTREngine.exe", creationflags=0x08000000)
		if not options[u'cl']:
			spHandler(gw, tc, options)
		return True
	else:
		print("Oof! Login failed with no error code.")
		launchWindow(winName)
		return False
		
def spHandler(gw, tc, options):
	import time
	if not options[u'vb']:
		win32gui.ShowWindow(cmdWindow, win32con.SW_HIDE)
	while True:
		time.sleep(3)
		poll = gw.poll()
		if poll != None:
			if not options[u'vb']:
				win32gui.ShowWindow(cmdWindow, win32con.SW_NORMAL)
			if options[u'rs']:
				if game == 'C':
					startCC(tc, options)
				elif game == 'R':
					startTTR(tc, options)
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
	globals.extend([win32gui.GetForegroundWindow(), [], "", []])
	try:
		globals[2] = eval(open('credentials.json', 'r').read())
		globals[3] = ("main")
		for i in globals[2]:
			globals[4].append(i[u'username'])
	except:
		globals[3]=("newAccount")
	return globals	

game, cmdWindow, credentials, winName, usernames = decGlobals()
row = 0

xmlData = '''<?xml version='1.0' encoding='utf-8'?>
<interface>
  <object class="ttk.Frame" id="main">
    <property name="height">200</property>
    <property name="padding">20</property>
    <property name="width">200</property>
    <layout>
      <property name="column">0</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
    </layout>
    <child>
      <object class="ttk.Labelframe" id="accountMenu">
        <property name="height">200</property>
        <property name="text" translatable="yes">Select Accounts:</property>
        <property name="width">200</property>
        <layout>
          <property name="column">0</property>
          <property name="padx">8</property>
          <property name="pady">10</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
          <property name="sticky">n</property>
        </layout>'''
for i in usernames:
	row += 1
	xmlData += '''
        <child>
          <object class="tk.Checkbutton" id="cb''' + str(usernames.index(i)) + '''">
            <property name="text" translatable="yes">''' + i + '''</property>
            <property name="variable">boolean:acct''' + str(usernames.index(i)) + '''</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">''' + str(row) + '''</property>
              <property name="sticky">w</property>
            </layout>
          </object>
        </child>'''
xmlData += '''    
      </object>
    </child>
    <child>
      <object class="ttk.Labelframe" id="optionsMenu">
        <property name="height">200</property>
        <property name="text" translatable="yes">Options and Launch:</property>
        <property name="width">200</property>
        <layout>
          <property name="column">1</property>
          <property name="padx">8</property>
          <property name="pady">10</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
          <property name="sticky">n</property>
          <rows>
            <row id="3">
              <property name="minsize">0</property>
              <property name="pad">8</property>
            </row>
          </rows>
        </layout>
        <child>
          <object class="tk.Checkbutton" id="noVerbose">
            <property name="text" translatable="yes">No Verbose Output</property>
            <property name="variable">boolean:vb</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
              <property name="sticky">w</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="tk.Checkbutton" id="restart">
            <property name="overrelief">flat</property>
            <property name="overrelief">flat</property>
            <property name="text" translatable="yes">Restart on Exit</property>
            <property name="variable">boolean:rs</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">1</property>
              <property name="sticky">w</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="tk.Checkbutton" id="closeLauncher">
            <property name="command">onClCheck</property>
            <property name="overrelief">flat</property>
            <property name="overrelief">flat</property>
            <property name="text" translatable="yes">Close on Launch</property>
            <property name="variable">boolean:cl</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">2</property>
              <property name="sticky">w</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Button" id="goButton">
            <property name="command">onGoClick</property>
            <property name="text" translatable="yes">Launch Game</property>
            <layout>
              <property name="column">0</property>
              <property name="ipadx">20</property>
              <property name="ipady">10</property>
              <property name="pady">10</property>
              <property name="propagate">True</property>
              <property name="row">4</property>
              <property name="sticky">s</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Button" id="naButton">
            <property name="command">onNAClick</property>
            <property name="text" translatable="yes">New Account</property>
            <layout>
              <property name="column">0</property>
              <property name="pady">0</property>
              <property name="propagate">True</property>
              <property name="row">3</property>
              <property name="sticky">s</property>
            </layout>
          </object>
        </child>'''
if game == 'C':
	popWindowChecker = True
	xmlData += '''
        <child>
          <object class="ttk.Label" id="popTracker">
            <property name="text" translatable="yes">Getting population...</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">5</property>
            </layout>
          </object>
        </child>'''
xmlData += '''
      </object>
    </child>
  </object>
  <object class="ttk.Frame" id="newAccount">
    <property name="padding">30</property>
    <layout>
      <property name="column">0</property>
      <property name="propagate">True</property>
      <property name="row">1</property>
    </layout>
    <child>
      <object class="ttk.Entry" id="unField">
        <property name="font">TkDefaultFont</property>
        <property name="validate">focusin</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">1</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Label" id="unLabel">
        <property name="text" translatable="yes">Username</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Label" id="passLabel">
        <property name="text" translatable="yes">Password</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">2</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Entry" id="passField">
        <property name="font">TkDefaultFont</property>
        <property name="justify">left</property>
        <property name="show">•</property>
        <property name="state">normal</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">3</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Button" id="goButtonNA">
        <property name="command">onNAGoClick</property>
        <property name="text" translatable="yes">Launch Game</property>
        <layout>
          <property name="column">0</property>
          <property name="ipadx">20</property>
          <property name="ipady">10</property>
          <property name="pady">15</property>
          <property name="propagate">True</property>
          <property name="row">5</property>
        </layout>
      </object>
    </child>
  </object>
</interface>'''

launchWindow(winName)
