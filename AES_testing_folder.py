## now try to do the same but read files from a folder
#python 3.6
# Atom
# walker
# 116CS0177

from Crypto.Cipher import AES
from Crypto import Random
from random import randint,seed,shuffle
from time import ctime ## time
import sys
import os  # path handling
import struct # system key packing
import csv # log


padd=['@','!','$','%','&','?','>','<','+','~','*','1','2','3','4','5','6','7','8','9','0','(',')','{','}']


def key_generator(key):
	####  key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	# standard  key length is 12+4;; 4 is the size of fixed padding
	key_length=len(key)
	# if nothing is inserted prompt again
	if	(key_length==0):
		print('Enter the key')
		key=input()

	key_length=len(key)
	if	(key_length>12):
		key=key[:12] # if input key length over 12 truncate it
		key_length=12

	#print(key)
	padding_length=16-key_length;
	i=0
	## randomness generator  seed()
	seed()
	for i in range(padding_length):
		l=len(padd)
		x=randint(0,l-1)
		key=key+padd[x]

	#print(key)  # now the 16 byte key is ready
	'''
	# shufflling
	key=list(key)
	shuffle(key)
	key=''.join(key)
	## shuffled key is ready
	'''
	print(key)
	key=key.encode('utf-8')
	return key

def encrypt_file(key, in_filename,log_filename=None, out_filename=None,  chunksize=64*1024):
	log=[]
	curr_time=ctime()
	cTime=curr_time.split(' ')
	date=cTime[1]+cTime[2]+cTime[-1]
	day=cTime[0]
	clk=cTime[3]

	log.append(day)
	log.append(date)
	log.append(clk)

	log.append(key)
	log.append(in_filename)

	if not out_filename:
		out_filename = in_filename + '.enc'

	iv =Random.new().read(AES.block_size)
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	filesize = os.path.getsize(in_filename)

	with open(in_filename,'rb') as infile: #open("test.txt",mode = 'rb',encoding = 'utf-8')
		with open(out_filename, 'wb') as outfile:
			outfile.write(struct.pack('<Q', filesize))
			outfile.write(iv)

			while True:
				chunk = infile.read(chunksize)
				print(type(chunk))
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += b' ' * (16 - len(chunk) % 16)# if b' ' * 4 gives b'    '; b indicates binary

				outfile.write(encryptor.encrypt(chunk))
	outfile.close()
	log.append(out_filename)
	#logging	
	with open(log_path,'a') as logf:
		writer = csv.writer(logf)
		writer.writerow(log)
	logf.close()

def decrypt_file(key, in_filename,log_file=None,out_filename=None, chunksize=24*1024):
	log=[]
	curr_time=ctime()
	cTime=curr_time.split(' ')
	date=cTime[1]+cTime[2]+cTime[-1]
	day=cTime[0]
	clk=cTime[3]

	log.append(day)
	log.append(date)
	log.append(clk)

	log.append(key)
	log.append(in_filename)

	if not out_filename:
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
	#logging
	
	with open(log_path,'a') as logf:
		writer = csv.writer(logf)
		writer.writerow(log)
	logf.close()
	



ip_path='/home/pabitra/Encrypto/test'  ## from UI
op_path='/home/pabitra/Encrypto/test2'  ## folder not file

log_path='crypto_log.csv'
f=open(log_path,'a') # if_it wasn't there it will get created
f.close()

print("press 1 to perform encryption	")
print("press 2 to perform decryption    ")
f=input()

if f=='1':
	key=input('Enter an alphanumeric key   ')
	key=key_generator(key)

	file_list=[]
	# r=root, d=directories, f = files
	for r, d, f in os.walk(ip_path):
		for file in f:
			file_list.append(os.path.join(r, file))

	print(file_list)
	for ip_file in file_list:
		l=ip_file.split('/') # check the slash
		fname=l[-1]
		op_file=op_path+'/'+fname+'.enc'
		encrypt_file(key,ip_file,log_path,op_file)

elif f=='2':
	key=input("Enter the key  ")
	key=key.encode('utf-8')

	file_list=[]
	# for decryption i/p is o/p and vice-versa
	# SWAPing
	ip_path,op_path=op_path,ip_path

	# r=root, d=directories, f = files
	for r, d, f in os.walk(ip_path):
		for file in f:
			file_list.append(os.path.join(r, file))

	for ip_file in file_list:
		op=os.path.splitext(ip_file)[0]
		op=op.split('\\')
		op_file=op_path+'\\'+op[-1]
		decrypt_file(key,ip_file,log_path,op_file)
else:
	print("its 1 or 2 you dumb ")
