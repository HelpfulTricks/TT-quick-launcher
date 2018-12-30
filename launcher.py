#Pygubu-based Toontown launcher script by TheMaskedMeowth (for Toontown Rewritten and Toontown Corporate Clash) 
#Current Version: v1.3.5 | Last updated: December 30, 2018
#This script lets you log in quickly and efficiently, with a couple other bells and whistles as well.
#Requirements: You'll need python 3.7, and you'll have to put this file in your game folder. If you'd like to run the file straight from the python script, you also need to have the requests, pywin32, and pygubu libraries installed.

import subprocess, time, os, sys, msvcrt, tkinter as tk, _thread as thread, requests, win32gui, win32con, win32com.shell.shell as shell, pygubu

class Application:
	def __init__(self, master, wn):
		self.builder = builder = pygubu.Builder()
		builder.add_from_string(xmlData)
		self.mw = builder.get_object(wn, master)
		builder.connect_callbacks(self)
		if wn == "main":
			if not hasCredentials:
				self.mw.master.withdraw()
			self.mw.master.protocol("WM_DELETE_WINDOW", onMainClose)
			if game == 'C':
				ptLabel = self.builder.get_object('popTracker')
				thread.start_new_thread(popTracker, (self, ptLabel))
			if len(usernames) == 1:
				self.builder.get_variable('acct' + str(0)).set(True)
		elif wn == "newAccount":
			if hasCredentials:
				self.mw.master.withdraw()
				self.mw.master.protocol("WM_DELETE_WINDOW", onNAClose)
			else:
				self.mw.master.protocol("WM_DELETE_WINDOW", onMainClose)
	
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
			mainWindow.mw.master.withdraw()
			options = {'vb': False, 'rs': False, 'cl': False, 'la': False}
			for a in accList:
				if len(accList) - 1 == accList.index(a):
					options = {'vb': not self.builder.get_variable('vb').get(), 'rs': self.builder.get_variable('rs').get(), 'cl': self.builder.get_variable('cl').get(), 'la': True}
				startGame(a, options, mainWindow)
	
	def onNAClick(self):
		mainWindow.mw.master.withdraw()
		unhideWindow(naWindow)

	def onNAGoClick(self):
		account = {'username': self.builder.get_object('unField').get(), 'password': self.builder.get_object('passField').get()}
		win32gui.ShowWindow(cmdWindow,win32con.SW_NORMAL)
		win32gui.SetForegroundWindow(cmdWindow)
		self.builder.get_object('passField').delete(0, 'end')
		naWindow.mw.master.withdraw()
		if hasCredentials:
			window = mainWindow
		else:
			window = naWindow
		t = startGame(account, {'vb': True, 'rs': False, 'cl': False, 'la': True}, window)
		if t:
			credentials.append(account)
			with open('credentials.json', 'w') as f:
				f.write(str(credentials))
			sys.exit()
				
	def onClCheck(self):
		if self.builder.get_variable('cl').get():
			self.builder.get_object('noVerbose').configure(state='disabled')
			self.builder.get_variable('vb').set(False)
			self.builder.get_object('restart').configure(state='disabled')
			self.builder.get_variable('rs').set(False)
		else:
			self.builder.get_object('noVerbose').configure(state='normal')
			self.builder.get_object('restart').configure(state='normal')
			
def onMainClose():
	sys.exit()

def onNAClose():
	unhideWindow(mainWindow)
	naWindow.mw.master.withdraw()

def popTracker(self, ptLabel):
	while True:
		if ptLabel.winfo_viewable():
			url = 'https://corporateclash.net/api/v1/districts/'
			r = requests.get(url).json()
			population = 0
			for a in r:
				population += a[u'population']
			self.builder.get_object('popTracker').configure(text='Population: ' + str(population))
			time.sleep(10)
		
def launchWindow(wn):
	root = tk.Tk()
	if game == 'C':
		root.title("Corporate Clash Launcher")
	elif game == 'R':
		root.title("Toontown Rewritten Launcher")
	win32gui.ShowWindow(cmdWindow, win32con.SW_MINIMIZE)
	root.iconbitmap("Launcher.exe")
	app = Application(root, wn)
	return app
	
def unhideWindow(window):
	win32gui.ShowWindow(cmdWindow, win32con.SW_MINIMIZE)
	window.mw.master.update()
	window.mw.master.deiconify()
	
def exitLauncher(message):
	print(message)
	junk = msvcrt.getch()
	os.system("cls")
	sys.exit()
	
def startGame(tc, options, window):
	if game == 'C':
		exe = "CorporateClash.exe"
		r = requests.post('https://corporateclash.net/api/v1/login/' + tc[u'username'], json=tc).json()
		if r[u'reason'] == 1000 or r[u'reason'] == 0:
			os.environ["TT_PLAYCOOKIE"] = r[u'token']
			os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
		else:
			print("Login failed with error code " + str(r[u'reason']) + ". (" + str(r[u'friendlyreason']) + ")")
			unhideWindow(window)
			return False
	if game == 'R':
		exe = "TTREngine.exe"
		r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=tc).json()
		success = r[u'success']
		if success == "delayed":
			queueToken = {'queueToken': r[u'queueToken']}
			eta = r[u'eta']
			while success == "delayed":
				print("You've been put into the queue. ETA: " + eta + " seconds", end='\r')
				time.sleep(5)
				r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=queueToken).json()
				success = r[u'success']
				if success == "delayed":
					eta = r[u'eta']
		if success == "true":
			os.environ["TTR_PLAYCOOKIE"] = r[u'cookie']
			os.environ["TTR_GAMESERVER"] = r[u'gameserver']
		else:
			print("Oof! Login failed, try again.")
			unhideWindow(window)
			return False
	print("Welcome back to Toontown, " + tc[u'username'] + "!								")
	if options[u'vb'] and not options[u'cl']:
		gw = subprocess.Popen(args=exe)
	else:
		gw = subprocess.Popen(args=exe, creationflags=0x08000000)
	if options[u'la'] and not options[u'cl']:
		naWindow.builder.get_object('unField').delete(0, 'end')
		spHandler(gw, tc, options, window)
	elif options[u'cl']:
		sys.exit()
	return True
		
def spHandler(gw, tc, options, window):
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
				startGame(tc, options, window)
			else:
				unhideWindow(window)
				break

if os.path.split(os.path.dirname(os.path.abspath(__file__)))[1] == "Corporate Clash":
	game = ('C')
elif os.path.split(os.path.dirname(os.path.abspath(__file__)))[1] == "Toontown Rewritten":
	if shell.IsUserAnAdmin():
		game = ('R')
	else:
		exitLauncher("This script must be run as an administrator in order to launch Toontown Rewritten. Press any key to exit...")
else:
	exitLauncher("Please put this file in your Corporate Clash or Toontown Rewritten folder. Press any key to exit...")
cmdWindow = win32gui.GetForegroundWindow()
credentials = []
hasCredentials = True
usernames = []
try:
	credentials = eval(open('credentials.json', 'r').read())
	for i in credentials:
		usernames.append(i[u'username'])
except:
	hasCredentials = False
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

mainWindow = launchWindow("main")
naWindow = launchWindow("newAccount")
mainWindow.mw.master.mainloop()