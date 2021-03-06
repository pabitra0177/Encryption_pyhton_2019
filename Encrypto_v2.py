# the main UI
# check : Gtk-Message: 20:05:27.575: GtkDialog mapped without a transient parent. This is discouraged.
## 	pyhton 3.67
##  Gedit
##	Crypto
##	116CS0177

''''
variable declaration:-

1) self.main_flag:- 	status -class string
						it is used to notify the process is encryption or decryption

2) self.key:-	status - class member variable string
				It contains the 16 digit key for both enc and dec

3) self.in_path:-	status- class member string var
					string input file adr with file name


4) self.op_path:- 	status- class member string var
					op path only , file name not included

5)self.log_path:-	status- class member string var
					log file path

6)process_flag
'''

'''
x.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
'''

#from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from Crypto.Cipher import AES,DES3
from Crypto import Random
from random import randint,seed,shuffle

from time import ctime,sleep
import sys
import os
import struct
import csv


padd=['@','!','$','%','&','?','>','<','+','~','*','1','2','3','4','5','6','7','8','9','0','(',')','{','}']

class App(QWidget):
	"""   """
	def selector(self,text):
		if text=='ENCRYPTION':
			self.main_flag='e'
		elif text=='DECRYPTION' :
			self.main_flag='d'
		elif text=='Folder Encryption':
			self.main_flag='fe'
		elif text=='Folder Decryption':
			self.main_flag='fd'
		#print(self.main_flag)

	def check(self):
		print("hello")


	def onActivated(self,text):
		if self.main_flag=='':
			self.set_colour()
		else :
			self.clr_colour() 
			
		#print(self.in_path)
		if self.main_flag=='e':
			l=self.in_path.split('/')
			fname=l[-1]
			#print(fname)
			self.op_path=self.op_path+'/'+fname+'.enc'
		elif self.main_flag=='d':
			op=os.path.splitext(self.in_path)[0]
			op=op.split('/')
			self.op_path=self.op_path+'/'+op[-1]
		if text=='AES':
			self.process_flag='AES'
			self.myMessageBox.setText("AES is selected, MODE:-CBC , Now enter the key ")
		elif text=='DES3':
			self.process_flag='DES3'


	def key_generator(self,text):
		if self.main_flag=='' or self.op_path=='' or self.in_path==None:
			self.set_colour()
		else :
			self.clr_colour() 
		
		if len(text)==10 and(self.main_flag=='e' or self.main_flag=='fe')and (self.process_flag=='DES3' or self.process_flag=='AES'):  
			## this part is for encryption
			self.key=text;
			key_length=len(self.key)
			
			#print(key)
			padding_length=16-key_length;
			i=0
			## randomness generator  seed()
			seed()
			for i in range(padding_length):
				l=len(padd)
				x=randint(0,l-1)
				self.key=self.key+padd[x]

			#print(key)  # now the 16 byte key is ready
			self.myMessageBox.setText(self.key)

		if (self.main_flag=='d' or self.main_flag=='fd') and len(text)==16 and (self.process_flag=='DES3' or self.process_flag=='AES'):
			## this part is for decryption
			self.key=text
			#print(self.key)
			self.myMessageBox.setText(self.key)


	def shuffler(self):
		if self.main_flag=='e' or self.main_flag=='fe':
			# shufflling
			self.key=str(self.key)
			self.key=list(self.key)
			shuffle(self.key)
			self.key=''.join(self.key)
			## shuffled key is ready
			self.myMessageBox.setText(self.key)
		else:
			self.myMessageBox.setText("check check")	
					

	def open_files(self):   # browser Button
		#print(self.main_flag)
		if self.main_flag=='':
			self.set_colour()
		else :
			self.clr_colour() 
		
		if self.main_flag=='e' or self.main_flag=='d': 
			dialog = QFileDialog()
			fname = dialog.getOpenFileName(self, "Open file")
			filename=fname[0]
			self.in_path=filename
			self.myTextBox.setText(self.in_path)
		
		elif self.main_flag=='fe' or self.main_flag=='fd':
			self.in_path= str(QFileDialog.getExistingDirectory(self, "Select Directory"))
			self.myTextBox.setText(self.in_path)
			
			ip_path=self.in_path
			for r, d, f in os.walk(ip_path):
				for file in f:
					self.file_list.append(os.path.join(r, file))
			##print(self.file_list) working perfectly

	
	def open_files_log(self):   # log file browser Button
		dialog = QFileDialog()
		fname = dialog.getOpenFileName(self, "Open log file")
		filename=fname[0]
		self.log_path=filename
		self.logTextBox.setText(filename)

	def op_files(self):
		if self.main_flag=='' or self.in_path==None:
			self.set_colour()
		else :
			self.clr_colour() 
		
		self.op_path= str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.opTextBox.setText(self.op_path)

	def runner(self):
		if self.main_flag=='':
			self.set_colour()
		else :
			self.clr_colour() 
		
		if self.main_flag=='e' or self.main_flag=='d':
			self.startP()
		elif self.main_flag=='fe' or self.main_flag=='fd':
			#self.check()
			Op=self.op_path
			for f in self.file_list:
				self.in_path=f
				if self.main_flag=='fe': # encryption
					l=self.in_path.split('/')
					fname=l[-1]
					#print(fname)
					self.op_path=Op+'/'+fname+'.enc'
					
				elif self.main_flag=='fd': # decryption
					op=os.path.splitext(self.in_path)[0]
					op=op.split('/')
					self.op_path=Op+'/'+op[-1]
				
				#print(self.in_path)
				#print(self.op_path)		
				self.startP()
			if self.main_flag=='fe':
				self.myMessageBox.setText("Folder encryption completed")
			if self.main_flag=='fd':
				self.myMessageBox.setText("folder decryption completed")
			sleep(2)
			self.close()		

	def startP(self):
		#print(self.process_flag)
		if (self.main_flag=='' or self.process_flag=='' or self.key=='' or self.in_path==None or self.in_path==''):
			self.set_colour()
		else:
			self.clr_colour()
				
		if self.process_flag=='AES':
			if len(self.key)!=16:
				#print(self.key)
				len(self.key)
				self.myMessageBox.setText("You have to enter key")
			elif len(self.key)==16 and (self.main_flag=='e' or self.main_flag=='fe'):
				#	now let's  do the encryption
				self.myMessageBox.setText("Encryption is going on")
				key=self.key
				in_filename=self.in_path
				log_path=self.log_path
				out_filename=self.op_path
				chunksize=self.chunksize;
				# **** #
				log=[]
				curr_time=ctime()
				cTime=curr_time.split(' ')
				date=cTime[3]+"/"+cTime[1]+"/"+cTime[-1]
				day=cTime[0]
				clk=cTime[4]

				log.append(day)
				log.append(date)
				log.append(clk)

				log.append(key)
				log.append(in_filename)

				if  out_filename=='':
					out_filename = in_filename + '.enc'

				# system key file
				iv =Random.new().read(AES.block_size)
				encryptor = AES.new(key, AES.MODE_CBC, iv)
				filesize = os.path.getsize(in_filename)

				with open(in_filename, 'rb') as infile:
					with open(out_filename, 'wb') as outfile:
						outfile.write(struct.pack('<Q', filesize))
						outfile.write(iv)

						while True:
							chunk = infile.read(chunksize)
							#print(type(chunk))
							if len(chunk) == 0:
								break
							elif len(chunk) % 16 != 0:
								chunk += b' ' * (16 - len(chunk) % 16)

							outfile.write(encryptor.encrypt(chunk))
				outfile.close()
				log.append(out_filename)
				log.append(self.process_flag)
				#logging
				with open(log_path,'a') as logf:
					writer = csv.writer(logf)
					writer.writerow(log)
					logf.close()
				if self.main_flag=='e':	
					self.myMessageBox.setText("Encryption completed")
					self.close()

			elif len(self.key)==16 and ( self.main_flag=='d' or self.main_flag=='fd'):
				""" decryption """
				self.myMessageBox.setText("Decryption is going on")
				key=self.key
				in_filename=self.in_path
				log_path=self.log_path
				out_filename=self.op_path
				chunksize=self.chunksize;

				log=[]
				curr_time=ctime()
				cTime=curr_time.split(' ')
				date=cTime[3]+"/"+cTime[1]+"/"+cTime[-1]
				day=cTime[0]
				clk=cTime[4]

				log.append(day)
				log.append(date)
				log.append(clk)

				log.append(key)
				log.append(in_filename)

				if  out_filename=='':
					out_filename = os.path.splitext(in_filename)[0]

				with open(in_filename, 'rb') as infile:
					original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
					iv = infile.read(16)
					decryptor = AES.new(key, AES.MODE_CBC, iv)

					with open(out_filename, 'wb') as outfile:
						while True:
							chunk = infile.read(chunksize)
							if len(chunk) == 0:
								break
							outfile.write(decryptor.decrypt(chunk))

						outfile.truncate(original_size)
						outfile.close()
				log.append(out_filename)
				log.append(self.process_flag)
				#logging
				with open(log_path,'a') as logf:
					writer = csv.writer(logf)
					writer.writerow(log)
					logf.close()
				if self.main_flag=='d':
					self.myMessageBox.setText("Decryption is completed")
					self.close()
				
		##################################################################################
		##################################################################################
		if	self.process_flag=='DES3':
			if len(self.key)!=16:
				#print(self.key)
				len(self.key)
				self.myMessageBox.setText("You have to enter key")
				
			elif len(self.key)==16 and (self.main_flag=='e' or self.main_flag=='fe'):
				#	now let's  do the encryption
				self.myMessageBox.setText("Encryption is going on")
				key=self.key
				in_filename=self.in_path
				log_path=self.log_path
				out_filename=self.op_path
				chunksize=self.chunksize;
				# **** #
				log=[]
				curr_time=ctime()
				cTime=curr_time.split(' ')
				date=cTime[3]+"/"+cTime[1]+"/"+cTime[-1]
				day=cTime[0]
				clk=cTime[4]

				log.append(day)
				log.append(date)
				log.append(clk)

				log.append(key)
				log.append(in_filename)

				if  out_filename=='':
					out_filename = in_filename + '.enc'

				# system key file
				iv =Random.new().read(DES3.block_size)
				encryptor = DES3.new(key, DES3.MODE_OFB, iv)
				filesize = os.path.getsize(in_filename)

				with open(in_filename, 'rb') as infile:
					with open(out_filename, 'wb') as outfile:
						outfile.write(struct.pack('<Q', filesize))
						outfile.write(iv)

						while True:
							chunk = infile.read(chunksize)
							#print(type(chunk))
							if len(chunk) == 0:
								break
							elif len(chunk) % 8 != 0:
								chunk += b' ' * (8 - len(chunk) % 8)

							outfile.write(encryptor.encrypt(chunk))
				outfile.close()
				log.append(out_filename)
				log.append(self.process_flag)
				#logging
				with open(log_path,'a') as logf:
					writer = csv.writer(logf)
					writer.writerow(log)
					logf.close()
				if self.main_flag=='e':	
					self.myMessageBox.setText("Encryption completed")
					self.close()

			elif len(self.key)==16 and (self.main_flag=='d' or self.main_flag=='fd'):
				""" decryption """
				self.myMessageBox.setText("Decryption is going on")
				key=self.key
				in_filename=self.in_path
				log_path=self.log_path
				out_filename=self.op_path
				chunksize=self.chunksize;

				log=[]
				curr_time=ctime()
				cTime=curr_time.split(' ')
				date=cTime[3]+"/"+cTime[1]+"/"+cTime[-1]
				day=cTime[0]
				clk=cTime[4]

				log.append(day)
				log.append(date)
				log.append(clk)

				log.append(key)
				log.append(in_filename)

				if out_filename=='':
					out_filename = os.path.splitext(in_filename)[0]

				with open(in_filename, 'rb') as infile:
					original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
					iv = infile.read(8)
					decryptor = DES3.new(key, DES3.MODE_OFB, iv)

					with open(out_filename, 'wb') as outfile:
						while True:
							chunk = infile.read(chunksize)
							if len(chunk) == 0:
								break
							outfile.write(decryptor.decrypt(chunk))

						outfile.truncate(original_size)
						outfile.close()
				log.append(out_filename)
				log.append(self.process_flag)
				#logging
				with open(log_path,'a') as logf:
					writer = csv.writer(logf)
					writer.writerow(log)
					logf.close()
				if self.main_flag=='d':	
					self.myMessageBox.setText("Decryption is completed")
					self.close()
	
	
	def set_colour(self):
		''' sets colour of ERROR label '''
		self.dummy.setStyleSheet('color:red')
		pass
		
	def clr_colour(self):
		''' clears the error'''
		self.dummy.setStyleSheet('color:lightGray')
		pass	


	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.main_flag=''
		########################### EDIT TO CHANGE OUTPUT PATH
		self.op_path=''# '/home/pabitra/Encrypto'  ## folder not file
		###########################################################
		self.key=''
		#self.in_path=''			
		self.file_list=[]	
		
		self.log_path='/home/pabitra/Encrypto/crypto_log.csv'
		f=open(self.log_path,'a')
		f.close()

		self.process_flag=''
		self.chunksize=64*1024

		# Basic tile,icon,geometry,statusBar
		self.setWindowTitle("Encrypto")
		self.setWindowIcon(QIcon("14970129516348746919"))
		self.setGeometry(100,100,420,380)

		# Colouring
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.lightGray)
		p.setColor(self.foregroundRole(), Qt.darkCyan)
		self.setPalette(p)


		## 5) select encryption or decryption
		self.bil_main=QLabel("<b>Choice  <\b>")
		self.select = QComboBox(self)
		self.select.addItem(' select ')
		self.select.addItem('ENCRYPTION')
		self.select.addItem('DECRYPTION')
		self.select.addItem('Folder Encryption')
		self.select.addItem('Folder Decryption')
		self.select.activated[str].connect(self.selector)


		## 1.1) browse button to select file to be encrypted or decrypted
		self.bil1=QLabel("<b>Define input file <\b>")
		self.bil1.setFont(QFont("Times",14,QFont.Bold)) ## change size 
		browserButton=QPushButton("browse files ",self)
		browserButton.resize(browserButton.sizeHint())
		browserButton.setFont(QFont("Times",13,QFont.DemiBold)) ## change size
		browserButton.setToolTip("Press to select the file you want ")
		browserButton.clicked.connect(self.open_files)
		#print(self.result)
		## 1.2) this is a text box to show the file selected
		self.myTextBox=QTextEdit(self)


		## 4)log file
		self.bil_log=QLabel("<b>log<\b>")
		self.bil_log.setFont(QFont("Times",14,QFont.Bold)) ## change size
		self.log_browser=QPushButton("select log file  ",self)
		self.log_browser.resize(browserButton.sizeHint())
		self.log_browser.setFont(QFont("Times",13,QFont.DemiBold)) ## change size
		self.log_browser.setToolTip("Press to select the log file you want ")
		self.log_browser.clicked.connect(self.open_files_log)
		self.logTextBox=QTextEdit(self)
		self.logTextBox.setText("selected by default")

		## 8) op path
		self.bil_op=QLabel("<b>Define output path <\b>")
		self.bil_op.setFont(QFont("Times",14,QFont.Bold)) ## change size
		opButton=QPushButton("select op folder ",self)
		opButton.resize(opButton.sizeHint())
		opButton.setFont(QFont("Times",13,QFont.DemiBold)) ## change size
		opButton.setToolTip("select the output folder ")
		opButton.clicked.connect(self.op_files)

		## 8.2) this is a text box to show the file selected
		self.opTextBox=QTextEdit(self)


		## 2) combobox to select type of encryption
		self.bil_type=QLabel("<b>Select the type of encryption<\b>")
		self.bil_type.setFont(QFont("Times",14,QFont.Bold)) ## change size
		combo = QComboBox(self)
		combo.addItem("Select")
		combo.addItem('AES')
		combo.addItem('DES3')
		#combo.addItem('XOR')
		combo.activated[str].connect(self.onActivated)

		## 3) key enter
		self.bil_key=QLabel("<b>Key <\b>")
		self.bil_key.setFont(QFont("Times",12,QFont.Bold)) ## change size
		self.keyBox=QLineEdit(self)
		try:
			self.keyBox.textChanged[str].connect(self.key_generator)
		except:
			pass
		
		##3.2) shuffle button
		shuffleButton= QPushButton("Shuffle",self)
		shuffleButton.resize(shuffleButton.sizeHint())
		shuffleButton.setToolTip("Press to shuffle the key ")
		shuffleButton.clicked.connect(self.shuffler)
		
		## 6) start the process
		startButton= QPushButton("START",self)
		startButton.setFont(QFont("Times",14,QFont.Black)) ## change size
		startButton.resize(startButton.sizeHint())
		startButton.setToolTip("Press to  run the Encryption ")
		startButton.clicked.connect(self.runner)

		## 7) message box
		self.bil_msg=QLabel("<b>Message Box<\b>")
		self.myMessageBox=QTextEdit(self)
		self.myMessageBox.setText("Please enter all the credential for the program to run")

		## dummy
		self.dummy=QLabel("<b>ERROR<\b>")
		self.clr_colour()		
		
		## grid
		grid=QGridLayout()
		grid.setSpacing(9)
		grid.addWidget(self.bil_main,1,0) # " Choice "
		grid.addWidget(self.dummy,1,2) # "hello"
		grid.addWidget(self.select,2,0) #"e/d" selection combobox 
		grid.addWidget(self.bil1,3,0)
		grid.addWidget(self.myTextBox,4,0) ## i/p file 
		grid.addWidget(browserButton,4,1,1,2)#"i/p file browse button "
		grid.addWidget(self.bil_log,5,0)
		grid.addWidget(self.logTextBox,6,0) 
		grid.addWidget(self.log_browser,6,1,1,2) # log file browse button
		grid.addWidget(self.bil_op,7,0)
		grid.addWidget(self.opTextBox,8,0)
		grid.addWidget(opButton,8,1,1,2) ##op folder button
		grid.addWidget(self.bil_type,9,0)
		grid.addWidget(combo,10,0)
		grid.addWidget(self.bil_key,11,0)
		grid.addWidget(self.keyBox,12,0)
		grid.addWidget(shuffleButton,12,1)
		grid.addWidget(self.bil_msg,13,0)
		grid.addWidget(self.myMessageBox,14,0,1,3)
		grid.addWidget(startButton,15,0)
		self.setLayout(grid)

		self.show()

	def closeEvent(self,event):
		reply=QMessageBox.question(self,"Message","Quit ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply==QMessageBox.Yes:
			event.accept()
		if reply==QMessageBox.No :
			event.ignore()


# ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
if __name__ == '__main__':
	app=QApplication(sys.argv)
	app.setStyle('Fusion')
	r=App()
	sys.exit(app.exec_())
