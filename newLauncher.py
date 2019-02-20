#PyQt-based Toontown launcher script by TheMaskedMeowth (for Toontown Rewritten and Toontown Corporate Clash) 
#Current Version: v1.4 | Last updated: January PUT SOMETHING HERE PLEASE PLEASE PLEASE, 2019
#This script lets you log in quickly and efficiently, with a couple other bells and whistles as well.
#Requirements: You'll need python 3.7, and you'll have to put this file in your game folder. If you'd like to run the file straight from the python script, you also need to have the requests, pywin32, and pygubu libraries installed.

import subprocess, os, sys, threading, requests, win32api, win32gui, win32com.shell.shell as shell
from PyQt5 import QtCore, QtGui, QtWidgets

class mainWindow(QtWidgets.QMainWindow):
	def setupUi(self, Form, FormTwo):
		Form.setObjectName("Form")
		Form.setEnabled(True)
		Form.resize(701, 648)
		Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		Form.setStyleSheet("background:transparent;")
		self.playButton = QtWidgets.QLabel(Form)
		self.playButton.setGeometry(QtCore.QRect(76, 327, 271, 231))
		self.playButton.setObjectName("playButton")
		QtGui.QFontDatabase.addApplicationFont(assetsPath() + "\\Impress.ttf")
		self.launcherBG = QtWidgets.QLabel(Form)
		self.launcherBG.setGeometry(QtCore.QRect(40, 50, 681, 531))
		self.launcherBG.setObjectName("launcherBG")
		self.launcherBG.raise_()
		font = QtGui.QFont()
		font.setFamily("Impress BT")
		font.setPointSize(12)
		self.cAccWidget = QtWidgets.QListWidget(Form)
		self.cAccWidget.setGeometry(QtCore.QRect(90, 144, 241, 233))
		self.cAccWidget.setFont(font)
		self.cAccWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.cAccWidget.setObjectName("cAccWidget")
		self.rAccWidget = QtWidgets.QListWidget(Form)
		self.rAccWidget.setGeometry(QtCore.QRect(90, 144, 241, 233))
		self.rAccWidget.setFont(font)
		self.rAccWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.rAccWidget.setObjectName("rAccWidget")
		self.cub, self.rub = [], []
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		for i in cu:
			item = QtWidgets.QListWidgetItem()
			item.setIcon(icon)
			item.setFlags(QtCore.Qt.ItemIsEnabled)
			self.cAccWidget.addItem(item)
			self.cub.append(self.cAccWidget.item(cu.index(i)))
		for i in ru:
			item = QtWidgets.QListWidgetItem()
			item.setIcon(icon)
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
		self.accLabel.setGeometry(QtCore.QRect(80, 87, 261, 51))
		font.setPointSize(18)
		self.accLabel.setFont(font)
		self.accLabel.setObjectName("accLabel")
		self.optionsWidget = QtWidgets.QListWidget(Form)
		self.optionsWidget.setGeometry(QtCore.QRect(360, 431, 231, 91))
		font.setPointSize(12)
		self.optionsWidget.setFont(font)
		self.optionsWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.optionsWidget.setObjectName("optionsWidget")
		item = QtWidgets.QListWidgetItem()
		item.setIcon(icon)
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		self.optionsWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		item.setIcon(icon)
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		self.optionsWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		item.setIcon(icon)
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		self.optionsWidget.addItem(item)
		self.optionsLabel = QtWidgets.QLabel(Form)
		self.optionsLabel.setGeometry(QtCore.QRect(360, 380, 231, 51))
		font.setPointSize(18)
		self.optionsLabel.setFont(font)
		self.optionsLabel.setObjectName("optionsLabel")
		self.naButton = QtWidgets.QLabel(Form)
		self.naButton.setGeometry(QtCore.QRect(356, 192, 240, 240))
		self.naButton.setObjectName("naButton")
		self.naButton.setMouseTracking(True)
		self.popCount = QtWidgets.QLabel(Form)
		self.popCount.setGeometry(QtCore.QRect(360, 213, 231, 31))
		font.setPointSize(12)
		self.popCount.setFont(font)
		self.popCount.setObjectName("popCount")
		self.logo = QtWidgets.QLabel(Form)
		self.logo.setGeometry(QtCore.QRect(375, 110, 201, 100))
		self.logo.setObjectName("logo")
		self.exitButton = QtWidgets.QLabel(Form)
		self.exitButton.setGeometry(QtCore.QRect(540, 30, 71, 71))
		self.exitButton.setObjectName("exitButton")
		self.minButton = QtWidgets.QLabel(Form)
		self.minButton.setGeometry(QtCore.QRect(480, 30, 71, 71))
		self.minButton.setObjectName("minButton")
		self.naHitbox = QtWidgets.QPushButton(Form)
		self.naHitbox.setGeometry(QtCore.QRect(360, 260, 231, 111))
		self.naHitbox.setObjectName("naHitbox")
		self.pbHitbox = QtWidgets.QPushButton(Form)
		self.pbHitbox.setGeometry(QtCore.QRect(90, 400, 241, 121))
		self.pbHitbox.setObjectName("pbHitbox")
		self.exitHitbox = QtWidgets.QPushButton(Form)
		self.exitHitbox.setGeometry(QtCore.QRect(540, 30, 71, 71))
		self.exitHitbox.setObjectName("exitHitbox")
		self.minHitbox = QtWidgets.QPushButton(Form)
		self.minHitbox.setGeometry(QtCore.QRect(480, 30, 71, 71))
		self.minHitbox.setObjectName("minHitbox")
		FormTwo.setObjectName("Form")
		FormTwo.setEnabled(True)
		FormTwo.resize(311, 221)
		FormTwo.setMinimumSize(QtCore.QSize(0, 0))
		FormTwo.setMaximumSize(QtCore.QSize(800, 800))
		FormTwo.setStyleSheet("")
		self.unField = QtWidgets.QLineEdit(FormTwo)
		self.unField.setGeometry(QtCore.QRect(40, 40, 231, 41))
		font.setPointSize(14)
		self.unField.setFont(font)
		self.unField.setObjectName("unField")
		self.pwField = QtWidgets.QLineEdit(FormTwo)
		self.pwField.setGeometry(QtCore.QRect(40, 90, 231, 41))
		font.setPointSize(14)
		self.pwField.setFont(font)
		self.pwField.setEchoMode(QtWidgets.QLineEdit.Password)
		self.pwField.setObjectName("pwField")
		self.naGoButton = QtWidgets.QPushButton(FormTwo)
		self.naGoButton.setGeometry(QtCore.QRect(80, 150, 151, 31))
		self.naGoButton.setObjectName("naGoButton")
		FormTwo.hide()
		self.playButton.raise_()
		self.naButton.raise_()
		self.accLabel.raise_()
		self.optionsLabel.raise_()
		self.popCount.raise_()
		self.cAccWidget.raise_()
		self.rAccWidget.raise_()
		self.optionsWidget.raise_()
		self.logo.raise_()
		self.exitButton.raise_()
		self.minButton.raise_()
		self.naHitbox.raise_()
		self.pbHitbox.raise_()
		self.logoHitbox = QtWidgets.QPushButton(Form)
		self.logoHitbox.setGeometry(QtCore.QRect(375, 110, 201, 100))
		self.logoHitbox.setObjectName("logoHitbox")
		self.logoHitbox.raise_()
		self.exitHitbox.raise_()
		self.minHitbox.raise_()
		self.oldPos = self.pos()
		self.retranslateUi(Form, FormTwo)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form, FormTwo):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.playButton.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\pbNormal.png\"/><img src=\"assets/pbNormal.png\"/></p></body></html>"))
		FormTwo.setWindowTitle(_translate("Form", "Form"))
		self.unField.setPlaceholderText(_translate("Form", "Username"))
		self.pwField.setPlaceholderText(_translate("Form", "Password"))
		self.naGoButton.setText(_translate("Form", "Go!"))
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
		self.vbButton.setText(_translate("Form", "No Verbose Output"))
		self.rsButton.setText(_translate("Form", "Restart on Game Exit"))
		self.clButton.setText(_translate("Form", "Close Launcher"))
		self.optionsWidget.setSortingEnabled(__sortingEnabled)
		self.optionsLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\">Options:</p></body></html>"))
		self.naButton.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\naNormal.png\"/></p></body></html>"))
		self.launcherBG.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\launcherBG.png\"/></p></body></html>"))
		self.popCount.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Getting Population...</span></p></body></html>"))
		self.popTrackerActive, self.popThread, self.popWait, self.gpWait = True, threading.Thread(name="popThread",target=popTracker,args=(self, self.popCount,)), threading.Event(), {}
		self.popThread.start()
		if cfg[u'game'] == 'C':
			self.logo.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ccLogo.png\"/></p></body></html>"))
		elif cfg[u'game'] == 'R':
			self.logo.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ttrLogo.png\"/></p></body></html>"))
			self.logo.setGeometry(QtCore.QRect(345, 100, 250, 123))
			self.logoHitbox.setGeometry(QtCore.QRect(345, 100, 250, 123))
			self.popCount.hide()
		self.exitButton.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\exitNormal.png\"/></p></body></html>"))
		self.minButton.setText(_translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\minNormal.png\"/></p></body></html>"))
		self.pbHitbox.pressed.connect(self.pbPress)
		self.naHitbox.pressed.connect(self.naPress)
		self.pbHitbox.released.connect(self.pbRelease)
		self.naHitbox.released.connect(self.naRelease)
		self.pbHitbox.clicked.connect(self.pbClick)
		self.naHitbox.clicked.connect(self.naClick)
		self.exitHitbox.clicked.connect(self.onClose)
		self.minHitbox.clicked.connect(self.minClick)
		self.naGoButton.clicked.connect(self.naGoClick)
		if len(ableToRun) == 2:
			self.logoHitbox.clicked.connect(self.gameChange)
		self.cAccWidget.itemClicked.connect(self.usernameClicked)
		self.rAccWidget.itemClicked.connect(self.usernameClicked)
		self.optionsWidget.itemClicked.connect(self.optionClicked)
		
	def pbPress(self):
		self.playButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\pbClicked.png\"/><img src=\"" + assetsPath() + "\\pbClicked.png\"/></p></body></html>"))
	
	def naPress(self):
		self.naButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\naClicked.png\"/><img src=\"" + assetsPath() + "\\naClicked.png\"/></p></body></html>"))
	
	def pbRelease(self):
		self.playButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\pbNormal.png\"/><img src=\"" + assetsPath() + "\\pbNormal.png\"/></p></body></html>"))
		
	def naRelease(self):
		self.naButton.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\naNormal.png\"/><img src=\"" + assetsPath() + "\\naNormal.png\"/></p></body></html>"))
		
	def pbClick(self):
		while clickedUsers != []:
			la = False
			if len(clickedUsers) == 1:
				la = True
			if cfg[u'game'] == 'C':
				for a in cfg[u'clashAccounts']:
					if a[u'username'] == clickedUsers[0]:
						c = a
				self.cAccWidget.item(cu.index(clickedUsers[0])).setFlags(QtCore.Qt.NoItemFlags)
			elif cfg[u'game'] == 'R':
				for a in cfg[u'ttrAccounts']:
					if a[u'username'] == clickedUsers[0]:
						c = a
				self.rAccWidget.item(ru.index(clickedUsers[0])).setFlags(QtCore.Qt.NoItemFlags)
			gameThread = threading.Thread(name=clickedUsers[0],target=startGame,args=(c, la, self,))
			gameThread.start()
			clickedUsers.remove(clickedUsers[0])
			
	def gameChange(self):
		global cfg, bothCU, clickedUsers
		if cfg[u'game'] == 'C':
			cfg[u'game'] = 'R'
			self.cAccWidget.hide()
			self.rAccWidget.show()
			self.current = ru
			self.currentUB = self.rub
			self.popCount.hide()
			bothCU[0] = clickedUsers
			clickedUsers = bothCU[1]
			self.logo.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ttrLogo.png\"/></p></body></html>"))
			self.logo.setGeometry(QtCore.QRect(345, 100, 250, 123))
			self.logoHitbox.setGeometry(QtCore.QRect(345, 100, 250, 123))
		elif cfg[u'game'] == 'R':
			cfg[u'game'] = 'C'
			self.cAccWidget.show()
			self.rAccWidget.hide()
			self.current = cu
			self.currentUB = self.cub
			self.popCount.show()
			bothCU[1] = clickedUsers
			clickedUsers = bothCU[0]
			self.logo.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p><img src=\"" + assetsPath() + "\\ccLogo.png\"/></p></body></html>"))
			self.logo.setGeometry(QtCore.QRect(375, 110, 201, 100))
			self.logoHitbox.setGeometry(QtCore.QRect(375, 110, 201, 100))
		print(clickedUsers)

	def naClick(self):
		naWindow.show()
		
	def naGoClick(self):
		cg = cfg[u'game']
		tc = {'username': self.unField.text(), 'password': self.pwField.text()}
		if cg == 'C':
			exe = "CorporateClash.exe"
			r = requests.post('https://corporateclash.net/api/v1/login/' + tc[u'username'], json=tc).json()
			if r[u'reason'] == 1000 or r[u'reason'] == 0:
				cfg[u'clashAccounts'].append(tc)
				cu.append(self.unField.text())
				item = QtWidgets.QListWidgetItem()
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("assets/cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				item.setIcon(icon)
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				self.cAccWidget.addItem(item)
				self.cub.append(item)
				item.setText(QtCore.QCoreApplication.translate("Form", self.unField.text()))
				naWindow.hide()
			else:
				print("Invalid login details")
		naWait = threading.Event()
		if cg == 'R':
			exe = "TTREngine.exe"
			r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=tc).json()
			success = r[u'success']
			if success == "delayed":
				queueToken = {'queueToken': r[u'queueToken']}
				eta = r[u'eta']
				while success == "delayed":
					print("You've been put into the queue. ETA: " + eta + " seconds", end='\r')
					naWait.wait(timeout=5)
					r = requests.post('https://www.toontownrewritten.com/api/login?format=json', json=queueToken).json()
					success = r[u'success']
					if success == "delayed":
						eta = r[u'eta']
			if success == "true":
				cfg[u'ttrAccounts'].append(tc)
				ru.append(self.unField.text())
				item = QtWidgets.QListWidgetItem()
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				item.setIcon(icon)
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				self.rAccWidget.addItem(item)
				self.rub.append(item)
				item.setText(QtCore.QCoreApplication.translate("Form", self.unField.text()))
				naWindow.hide()

	def minClick(self):
		window.showMinimized()
		
	def onClose(self):
		window.hide()
		self.popTrackerActive = False
		with open('launcherConfig.json', 'w') as f:
			f.write(str(cfg))
		for e in self.gpWait:
			e.set()
		self.popWait.set()
		for t in threading.enumerate():
			if not (t.getName() == "MainThread"):
				t.join()
		sys.exit()
		
	def usernameClicked(self, unBox):
		if unBox.flags() == QtCore.Qt.ItemIsEnabled:
			username = self.current[self.currentUB.index(unBox)]
			if username in clickedUsers:
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				unBox.setIcon(icon)
				clickedUsers.remove(username)
			else:
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbChecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				unBox.setIcon(icon)
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
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
					self.vbButton.setFlags(QtCore.Qt.NoItemFlags)
					self.vbButton.setIcon(icon)
					self.rsButton.setFlags(QtCore.Qt.NoItemFlags)
					self.rsButton.setIcon(icon)
					icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbChecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
					self.clButton.setIcon(icon)
			icon = QtGui.QIcon()
			if option:
				icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbUnchecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			else:
				icon.addPixmap(QtGui.QPixmap(assetsPath() + "\\cbChecked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			opBox.setIcon(icon)

def popTracker(self, popCount):
	while True:
		if self.popTrackerActive:
			url = 'https://corporateclash.net/api/v1/districts/'
			r = requests.get(url).json()
			population = 0
			for a in r:
				population += a[u'population']
			popCount.setText(QtCore.QCoreApplication.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Population: " + str(population) + "</span></p></body></html>"))
			self.popWait.wait(timeout=10)
		else:
			break
	
def startGame(tc, la, self):
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
			print("Login failed with error code " + str(r[u'reason']) + ". (" + str(r[u'friendlyreason']) + ")")
			self.cAccWidget.item(cu.index(tc[u'username'])).setFlags(QtCore.Qt.ItemIsEnabled)
			clickedUsers.append(tc[u'username'])
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
			self.rAccWidget.item(ru.index(tc[u'username'])).setFlags(QtCore.Qt.ItemIsEnabled)
			clickedUsers.append(tc[u'username'])
	print("Welcome back to Toontown, " + tc[u'username'] + "!								")
	if not clickedOptions[u'vb'] and not clickedOptions[u'cl'] and la:
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
				startGame(tc, True, self)
			else:
				if cg == 'C':
					self.cub[cu.index(tc[u'username'])].setFlags(QtCore.Qt.ItemIsEnabled)
				elif cg == 'R':
					self.cub[ru.index(tc[u'username'])].setFlags(QtCore.Qt.ItemIsEnabled)
				clickedUsers.append(tc[u'username'])
			self.gpWait[tc[u'username']].set()
			break
	
def assetsPath():
	try:
		base_path = sys._MEIPASS
	except:
		base_path = os.path.abspath(".")
	return str(os.path.join(base_path, "assets"))

app, dirWindow, window, naWindow, ui = QtWidgets.QApplication(sys.argv), QtWidgets.QDialog(), QtWidgets.QDialog(), QtWidgets.QDialog(), mainWindow()	
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

ui.setupUi(window, naWindow)
window.show()
sys.exit(app.exec_())