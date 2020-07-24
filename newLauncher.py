'''
PyQt-based Toontown launcher script by HelpfulTricks (for Toontown Rewritten and Toontown Corporate Clash) 
Current Version: v1.4-rc8 | Last updated: July 24, 2020
This script lets you log in quickly and efficiently, with a couple other bells and whistles as well.
Requirements: You just need to put the .exe file in your game folder. If you'd like to run the file straight from the python script, you'll need python 3.7, and you also need to have the requests, pywin32, and pygubu libraries installed.
'''

import subprocess, os, sys, threading, requests, win32api, win32gui, win32com.shell.shell as shell
from PyQt5 import QtCore, QtGui, QtWidgets

class mainWindow(QtWidgets.QMainWindow):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.setEnabled(True)
		Form.resize(540, 460)
		Form.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
		Form.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
		Form.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
		Form.setStyleSheet("background:transparent;")
		self.playButton = QtWidgets.QLabel(Form)
		self.playButton.setObjectName("playButton")
		QtGui.QFontDatabase.addApplicationFont(assetsPath() + "\\Impress.ttf")
		self.launcherBG = QtWidgets.QLabel(Form)
		self.launcherBG.setObjectName("launcherBG")
		self.launcherBG.raise_()
		font = QtGui.QFont()
		font.setFamily("Impress BT")
		font.setPointSize(12)
		self.cAccWidget = QtWidgets.QListWidget(Form)
		self.cAccWidget.setFont(font)
		self.cAccWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.cAccWidget.setObjectName("cAccWidget")
		self.rAccWidget = QtWidgets.QListWidget(Form)
		self.rAccWidget.setFont(font)
		self.rAccWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.rAccWidget.setObjectName("rAccWidget")
		self.cub, self.rub = [], []
		self.ucIcon = QtGui.QIcon()
		self.ucIcon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.chIcon = QtGui.QIcon()
		self.chIcon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbChecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		for i in cu:
			item = QtWidgets.QListWidgetItem()
			item.setIcon(self.ucIcon)
			item.setFlags(QtCore.Qt.ItemIsEnabled)
			self.cAccWidget.addItem(item)
			self.cub.append(self.cAccWidget.item(cu.index(i)))
		for i in ru:
			item = QtWidgets.QListWidgetItem()
			item.setIcon(self.ucIcon)
			item.setFlags(QtCore.Qt.ItemIsEnabled)
			self.rAccWidget.addItem(item)
			self.rub.append(self.rAccWidget.item(ru.index(i)))
		if cfg[u'game'] == 'C':
			self.current = cu
			self.currentUB = self.cub
			self.rAccWidget.hide()
		elif cfg[u'game'] == 'R':
			self.current = ru
			self.currentUB = self.rub
			self.cAccWidget.hide()
		self.accLabel = QtWidgets.QLabel(Form)
		font.setPointSize(18)
		self.accLabel.setFont(font)
		self.accLabel.setObjectName("accLabel")
		self.optionsWidget = QtWidgets.QListWidget(Form)
		self.optionsLabel = QtWidgets.QLabel(Form)
		self.optionsLabel.setFont(font)
		self.optionsLabel.setObjectName("optionsLabel")
		self.naButton = QtWidgets.QLabel(Form)
		self.naButton.setObjectName("naButton")
		self.naButton.setMouseTracking(True)
		self.cPopCount = QtWidgets.QLabel(Form)
		self.rPopCount = QtWidgets.QLabel(Form)
		font.setPointSize(12)
		self.optionsWidget.setFont(font)
		self.optionsWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.optionsWidget.setObjectName("optionsWidget")
		item = QtWidgets.QListWidgetItem()
		item.setIcon(self.ucIcon)
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		self.optionsWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		item.setIcon(self.ucIcon)
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		self.optionsWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		item.setIcon(self.ucIcon)
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		self.optionsWidget.addItem(item)
		self.cPopCount.setFont(font)
		self.cPopCount.setObjectName("cPopCount")
		self.rPopCount.setFont(font)
		self.rPopCount.setObjectName("rPopCount")
		self.logo = QtWidgets.QLabel(Form)
		self.logo.setObjectName("logo")
		self.naHitbox = QtWidgets.QPushButton(Form)
		self.naHitbox.setObjectName("naHitbox")
		self.pbHitbox = QtWidgets.QPushButton(Form)
		self.pbHitbox.setObjectName("pbHitbox")
		self.unField = QtWidgets.QLineEdit(Form)
		font.setPointSize(14)
		self.unField.setFont(font)
		self.unField.setObjectName("unField")
		self.pwField = QtWidgets.QLineEdit(Form)
		self.pwField.setFont(font)
		self.pwField.setEchoMode(QtWidgets.QLineEdit.Password)
		self.pwField.setObjectName("pwField")
		self.pwField.hide()
		self.unField.hide()
		font.setPointSize(10)
		self.playButton.raise_()
		self.naButton.raise_()
		self.accLabel.raise_()
		self.optionsLabel.raise_()
		self.cPopCount.raise_()
		self.rPopCount.raise_()
		self.cAccWidget.raise_()
		self.rAccWidget.raise_()
		self.optionsWidget.raise_()
		self.logo.raise_()
		self.naHitbox.raise_()
		self.pbHitbox.raise_()
		self.logoHitbox = QtWidgets.QPushButton(Form)
		self.logoHitbox.setObjectName("logoHitbox")
		self.logoHitbox.raise_()
		self.playButton.setGeometry(QtCore.QRect(6, 238, 271, 231))
		self.launcherBG.setGeometry(QtCore.QRect(0, 0, 860, 460))
		self.cAccWidget.setGeometry(QtCore.QRect(22, 58, 241, 233))
		self.rAccWidget.setGeometry(QtCore.QRect(22, 58, 241, 233))
		self.accLabel.setGeometry(QtCore.QRect(10, 3, 261, 51))
		self.optionsWidget.setGeometry(QtCore.QRect(290, 346, 231, 91))
		self.optionsLabel.setGeometry(QtCore.QRect(290, 295, 231, 51))
		self.naButton.setGeometry(QtCore.QRect(286, 107, 240, 240))
		self.cPopCount.setGeometry(QtCore.QRect(290, 128, 231, 31))
		self.rPopCount.setGeometry(QtCore.QRect(290, 128, 231, 31))
		self.logo.setGeometry(QtCore.QRect(305, 25, 201, 100))
		self.naHitbox.setGeometry(QtCore.QRect(290, 175, 231, 111))
		self.pbHitbox.setGeometry(QtCore.QRect(20, 310, 241, 127))
		self.logoHitbox.setGeometry(QtCore.QRect(305, 25, 201, 100))
		self.unField.setGeometry(QtCore.QRect(25, 100, 231, 41))
		self.pwField.setGeometry(QtCore.QRect(25, 170, 231, 41))
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Toontown Quick Launcher"))
		self.playButton.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\pbNormal.png\"/><img src=\"assets/pbNormal.png\"/></p></body></html>"))
		self.unField.setPlaceholderText(_translate("Form", "Username"))
		self.pwField.setPlaceholderText(_translate("Form", "Password"))
		__sortingEnabled = self.cAccWidget.isSortingEnabled()
		self.cAccWidget.setSortingEnabled(False)
		for i in cu:
			self.cub[cu.index(i)].setText(_translate("Form", i))
		self.cAccWidget.setSortingEnabled(__sortingEnabled)
		__sortingEnabled = self.cAccWidget.isSortingEnabled()
		self.rAccWidget.setSortingEnabled(False)
		for i in ru:
			self.rub[ru.index(i)].setText(_translate("Form", i))
		self.rAccWidget.setSortingEnabled(__sortingEnabled)
		self.accLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\">Accounts:</p></body></html>"))
		__sortingEnabled = self.optionsWidget.isSortingEnabled()
		self.optionsWidget.setSortingEnabled(False)
		self.vbButton, self.rsButton, self.clButton = self.optionsWidget.item(0), self.optionsWidget.item(1), self.optionsWidget.item(2)
		self.vbButton.setText(_translate("Form", "Console Output"))
		self.rsButton.setText(_translate("Form", "Restart on Game Exit"))
		self.clButton.setText(_translate("Form", "Close Launcher"))
		self.optionsWidget.setSortingEnabled(__sortingEnabled)
		self.optionsLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\">Options:</p></body></html>"))
		self.naButton.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\naNormal.png\"/></p></body></html>"))
		self.launcherBG.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\launcherBG.png\"/></p></body></html>"))
		self.cPopCount.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Getting Population...</span></p></body></html>"))
		self.rPopCount.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Getting Population...</span></p></body></html>"))
		self.cPopTrackerActive, self.rPopTrackerActive, self.cPopThread, self.rPopThread, self.cPopWait, self.rPopWait, self.gpWait, self.toonstepMode, self.rf, self.nacg, self.natc = True, True, threading.Thread(name="cPopThread",target=cPopTracker,args=(self,)), threading.Thread(name="rPopThread",target=rPopTracker,args=(self,)), threading.Event(), threading.Event(), {}, False, {}, '', {}
		self.cPopThread.start()
		self.rPopThread.start()
		if cfg[u'game'] == 'C':
			self.logo.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ccLogo.png\"/></p></body></html>"))
			self.rPopCount.hide()
		elif cfg[u'game'] == 'R':
			self.logo.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ttrLogo.png\"/></p></body></html>"))
			self.cPopCount.hide()
		self.pbHitbox.pressed.connect(self.pbPress)
		self.naHitbox.pressed.connect(self.naPress)
		self.pbHitbox.released.connect(self.pbRelease)
		self.naHitbox.released.connect(self.naRelease)
		self.pbHitbox.clicked.connect(self.pbClick)
		self.naHitbox.clicked.connect(self.naClick)
		if len(ableToRun) == 2:
			self.logoHitbox.clicked.connect(self.gameChange)
		self.cAccWidget.itemClicked.connect(self.usernameClicked)
		self.rAccWidget.itemClicked.connect(self.usernameClicked)
		self.optionsWidget.itemClicked.connect(self.optionClicked)
		QtCore.QMetaObject.connectSlotsByName(Form)
		
	def pbPress(self):
		self.playButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\pbClicked.png\"/><img src=\"" + assetsPath() + "\\pbClicked.png\"/></p></body></html>"))
	
	def naPress(self):
		self.naButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\naClicked.png\"/><img src=\"" + assetsPath() + "\\naClicked.png\"/></p></body></html>"))
	
	def pbRelease(self):
		self.playButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\pbNormal.png\"/><img src=\"" + assetsPath() + "\\pbNormal.png\"/></p></body></html>"))
		
	def naRelease(self):
		self.naButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\naNormal.png\"/><img src=\"" + assetsPath() + "\\naNormal.png\"/></p></body></html>"))
			
	def gameChange(self):
		global cfg, bothCU, clickedUsers
		if cfg[u'game'] == 'C':
			cfg[u'game'] = 'R'
			if mode != 1:
				self.cAccWidget.hide()
				self.rAccWidget.show()
			self.current = ru
			self.currentUB = self.rub
			self.cPopCount.hide()
			self.rPopCount.show()
			bothCU[0] = clickedUsers
			clickedUsers = bothCU[1]
			self.logo.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ttrLogo.png\"/></p></body></html>"))
		elif cfg[u'game'] == 'R':
			cfg[u'game'] = 'C'
			if mode != 1:
				self.cAccWidget.show()
				self.rAccWidget.hide()
			self.current = cu
			self.currentUB = self.cub
			self.rPopCount.hide()
			self.cPopCount.show()
			bothCU[1] = clickedUsers
			clickedUsers = bothCU[0]
			self.logo.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ccLogo.png\"/></p></body></html>"))

	def naClick(self):
		global mode
		if mode != 1:
			mode = 1
			self.cAccWidget.hide()
			self.rAccWidget.hide()
			self.accLabel.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\">New Account:</p></body></html>"))
			self.unField.show()
			self.pwField.show()
		else:
			mode = 0
			if cfg[u'game'] == 'C':
				self.cAccWidget.show()
			elif cfg[u'game'] == 'R':
				self.rAccWidget.show()
			self.accLabel.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\">Accounts:</p></body></html>"))
			self.unField.hide()
			self.pwField.hide()
		
	def naGoClick(self):
		if self.toonstepMode == False:				
			self.nacg = cfg[u'game']
			self.natc = {'username': self.unField.text(), 'password': self.pwField.text()}
		self.gpWait[self.natc[u'username']] = threading.Event()
		if self.nacg == 'C':
			os.chdir(cfg[u'clashDir'])
			exe = "CorporateClash.exe"
			r = requests.post('https://corporateclash.net/api/v1/login/' + self.natc[u'username'], json=self.natc).json()
			if r[u'reason'] == 1000 or r[u'reason'] == 0:
				cfg[u'clashAccounts'].append(self.natc)
				cu.append(self.unField.text())
				item = QtWidgets.QListWidgetItem()
				item.setIcon(self.ucIcon)
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				self.cAccWidget.addItem(item)
				self.cub.append(item)
				item.setText(QtCore.QCoreApplication.translate("Form", self.unField.text()))
				self.unField.setText("")
				self.pwField.setText("")
				self.naClick()
				button = self.cAccWidget.item(cu.index(self.natc[u'username']))
				gameThread = threading.Thread(name=self.natc[u'username'],target=startGame,args=(self.natc, True, self, button,))
				button.setFlags(QtCore.Qt.NoItemFlags)
				gameThread.start()
			else:
				print("Invalid login details")
		elif self.nacg == 'R':
			os.chdir(cfg[u'ttrDir'])
			exe = "TTREngine.exe"
			if self.toonstepMode:
				self.rf[u'appToken'] = self.pwField.text()
				r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=self.rf).json()
			else:
				r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=self.natc).json()
			success = r[u'success']
			if success == "partial":
				self.rf = {'appToken': "", 'authToken': r[u'responseToken']}
				self.unField.setPlaceholderText(QtCore.QCoreApplication.translate("Form", "--------------------"))
				self.pwField.setPlaceholderText(QtCore.QCoreApplication.translate("Form", "2FA or ToonStep Code"))
				self.unField.setText("")
				self.pwField.setText("")
				self.toonstepMode = True
			if success == "delayed":
				queueToken = {'queueToken': r[u'queueToken']}
				eta = r[u'eta']
				while success == "delayed":
					print("You've been put into the queue. ETA: " + eta + " seconds", end='\r')
					self.gpWait[self.natc[u'username']].wait(timeout=5)
					r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=queueToken).json()
					success = r[u'success']
					if success == "delayed":
						eta = r[u'eta']
			if success == "true":
				cfg[u'ttrAccounts'].append(self.natc)
				ru.append(self.unField.text())
				item = QtWidgets.QListWidgetItem()
				item.setIcon(self.ucIcon)
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				self.rAccWidget.addItem(item)
				self.rub.append(item)
				item.setText(QtCore.QCoreApplication.translate("Form", self.unField.text()))
				self.toonstepMode = False
				self.unField.setPlaceholderText(QtCore.QCoreApplication.translate("Form", "Username"))
				self.pwField.setPlaceholderText(QtCore.QCoreApplication.translate("Form", "Password"))
				self.unField.setText("")
				self.pwField.setText("")
				self.naClick()
				button = self.rAccWidget.item(ru.index(self.natc[u'username']))
				gameThread = threading.Thread(name=self.natc[u'username'],target=startGame,args=(self.natc, True, self, button,))
				button.setFlags(QtCore.Qt.NoItemFlags)
				gameThread.start()
	
	def pbClick(self):
		if mode == 1:
			self.naGoClick()
		else:
			while len(clickedUsers) != 0:
				la = False
				if len(clickedUsers) == 1:
					la = True
				if cfg[u'game'] == 'C':
					tcfg = cfg[u'clashAccounts']
					button = self.cAccWidget.item(cu.index(clickedUsers[0]))
				elif cfg[u'game'] == 'R':
					tcfg = cfg[u'ttrAccounts']
					button = self.rAccWidget.item(ru.index(clickedUsers[0]))
				for a in tcfg:
					if a[u'username'] == clickedUsers[0]:
						c = a
				gameThread = threading.Thread(name=clickedUsers[0],target=startGame,args=(c, la, self, button,))
				button.setFlags(QtCore.Qt.NoItemFlags)
				clickedUsers.remove(clickedUsers[0])
				gameThread.start()
	
	def onClose(self):
		os.chdir(wd)
		window.hide()
		self.cPopTrackerActive = False
		self.rPopTrackerActive = False
		with open('launcherConfig.json', 'w') as f:
			f.write(str(cfg))
		for e in self.gpWait:
			self.gpWait[e].set()
		for t in threading.enumerate():
			if not (t.getName() == "MainThread"):
				t.join()
		sys.exit()
		
	def usernameClicked(self, unBox):
		if unBox.flags() == QtCore.Qt.ItemIsEnabled:
			username = self.current[self.currentUB.index(unBox)]
			if username in clickedUsers:
				unBox.setIcon(self.ucIcon)
				clickedUsers.remove(username)
			else:
				unBox.setIcon(self.chIcon)
				clickedUsers.append(username)
	
	def optionClicked(self, opBox):
		#options = {'vb': False, 'rs': False, 'cl': False}
		if opBox.flags() == QtCore.Qt.ItemIsEnabled:
			if opBox == self.vbButton:
				option = clickedOptions[u'vb']
				clickedOptions[u'vb'] = not clickedOptions[u'vb']
			elif opBox == self.rsButton:
				option = clickedOptions[u'rs']
				clickedOptions[u'rs'] = not clickedOptions[u'rs']
			elif opBox == self.clButton:
				option = clickedOptions[u'cl']
				clickedOptions[u'cl'] = not clickedOptions[u'cl']
				if option:
					self.vbButton.setFlags(QtCore.Qt.ItemIsEnabled)
					self.rsButton.setFlags(QtCore.Qt.ItemIsEnabled)
				else:
					clickedOptions[u'vb'] = False
					clickedOptions[u'rs'] = False
					self.vbButton.setFlags(QtCore.Qt.NoItemFlags)
					self.vbButton.setIcon(self.ucIcon)
					self.rsButton.setFlags(QtCore.Qt.NoItemFlags)
					self.rsButton.setIcon(self.ucIcon)
					self.clButton.setIcon(self.chIcon)
			icon = QtGui.QIcon()
			if option:
				opBox.setIcon(self.ucIcon)
			else:
				opBox.setIcon(self.chIcon)

def cPopTracker(self):
	url = 'https://corporateclash.net/api/v1/districts/'
	while True:
		if self.cPopTrackerActive:
			if cfg[u'game'] == 'C':
				try:
					r = requests.get(url).json()
					population = 0
					for a in r:
						population += a[u'population']
					self.cPopCount.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Population: " + str(population) + "</span></p></body></html>"))
					for i in range(0, 20):
						if self.cPopTrackerActive:
							self.cPopWait.wait(timeout=0.5)
						else:
							break
				except:
					pass
			else:
				self.cPopCount.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Getting Population...</span></p></body></html>"))
		else:
			break
			
def rPopTracker(self):
	url = 'https://www.toontownrewritten.com/api/population'
	while True:
		if self.rPopTrackerActive:
			if cfg[u'game'] == 'R':
				try:
					r = requests.get(url).json()
					population = r[u'totalPopulation']
					self.rPopCount.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Population: " + str(population) + "</span></p></body></html>"))
					for i in range(0, 20):
						if self.rPopTrackerActive:
							self.rPopWait.wait(timeout=0.5)
						else:
							break
				except:
					pass
			else:
				self.rPopCount.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Getting Population...</span></p></body></html>"))
		else:
			break

def startGame(tc, la, self, button):
	cg = cfg[u'game']
	self.gpWait[tc[u'username']] = threading.Event()
	if cg == 'C':
		os.chdir(cfg[u'clashDir'])
		exe = "CorporateClash.exe"
		r = requests.post('https://corporateclash.net/api/v1/login/' + tc[u'username'], json=tc).json()
		if r[u'reason'] == 1000 or r[u'reason'] == 0:
			os.environ["TT_PLAYCOOKIE"] = r[u'token']
			os.environ["TT_GAMESERVER"] = "gs.corporateclash.net"
		else:
			button.setText(str(r[u'friendlyreason']))
			print("Login failed with error code " + str(r[u'reason']) + ". (" + str(r[u'friendlyreason']) + ")")
			self.gpWait[tc[u'username']].wait(timeout=4)
			button.setText(QtCore.QCoreApplication.translate("Form", tc[u'username']))
			button.setFlags(QtCore.Qt.ItemIsEnabled)
			clickedUsers.append(tc[u'username'])
			return
	if cg == 'R':
		os.chdir(cfg[u'ttrDir'])
		exe = "TTREngine.exe"
		r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=tc).json()
		success = r[u'success']
		if success == "delayed":
			queueToken = {'queueToken': r[u'queueToken']}
			eta = r[u'eta']
			while success == "delayed":
				print("You've been put into the queue. ETA: " + eta + " seconds", end='\r')
				self.gpWait[tc[u'username']].wait(timeout=5)
				r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=queueToken).json()
				success = r[u'success']
				if success == "delayed":
					eta = r[u'eta']
		if success == "true":
			os.environ["TTR_PLAYCOOKIE"] = r[u'cookie']
			os.environ["TTR_GAMESERVER"] = r[u'gameserver']
		else:
			print("Oof! Login failed, try again.")
			button.setFlags(QtCore.Qt.ItemIsEnabled)
			clickedUsers.append(tc[u'username'])
			return
	print("Welcome back to Toontown, " + tc[u'username'] + "!								")
	if clickedOptions[u'vb'] and not clickedOptions[u'cl'] and la:
		gw = subprocess.Popen(args=exe)
	else:
		gw = subprocess.Popen(args=exe, creationflags=0x08000000)
	if clickedOptions[u'cl']:
		self.onClose()
	while True:
		self.gpWait[tc[u'username']].wait(timeout=1)
		poll = gw.poll()
		if poll != None:
			if clickedOptions[u'rs']:
				startGame(tc, True, self, button)
			else:
				button.setFlags(QtCore.Qt.ItemIsEnabled)
				clickedUsers.append(tc[u'username'])
			break
	
def assetsPath():
	os.chdir(wd)
	try:
		base_path = sys._MEIPASS
	except:
		base_path = os.path.abspath(".")
	return str(os.path.join(base_path, "assets"))

app, dirWindow, window, ui, wd, mode = QtWidgets.QApplication(sys.argv), QtWidgets.QDialog(), QtWidgets.QDialog(), mainWindow(), os.path.dirname(os.path.realpath(__file__)), 0
try:
	cfg = eval(open('launcherConfig.json', 'r').read())
except:
	check = [True, True]
	while check[0]:
		clashDir = str(QtWidgets.QFileDialog.getExistingDirectory(dirWindow, "Select Corporate Clash Directory (if not installed, click Cancel)"))
		if clashDir == "":
			check[0] = False
		else:
			for f in os.listdir(clashDir):
				print(str(f))
				if str(f) == "CorporateClash.exe":
					check[0] = False
	while check[1]:
		ttrDir = str(QtWidgets.QFileDialog.getExistingDirectory(dirWindow, "Select Toontown Rewritten Directory (if not installed, click Cancel)"))
		if ttrDir == "":
			check[1] = False
		else:
			for f in os.listdir(ttrDir):
				if str(f) == "TTREngine.exe":
					check[1] = False
	cfg = {'clashAccounts': [], 'ttrAccounts': [], 'clashDir': clashDir, 'ttrDir': ttrDir, 'game': ''}
ableToRun, cu, ru, bothCU = [], [], [], [[], []]
if cfg[u'clashDir'] != "":
	ableToRun.append('C')
	for i in cfg[u'clashAccounts']:
		cu.append(i[u'username'])
if cfg[u'ttrDir'] != "" and shell.IsUserAnAdmin():
	ableToRun.append('R')
	for i in cfg[u'ttrAccounts']:
		ru.append(i[u'username'])
if len(ableToRun) == 0:
	sys.exit()
if cfg[u'game'] == '' or len(ableToRun) == 1:
	cfg[u'game'] = ableToRun[0]
clickedUsers, clickedOptions = [], {'vb': False, 'rs': False, 'cl': False}

ui.setupUi(window)
window.show()
app.exec_()
ui.onClose()