import socket
from Cryptodome.Cipher import AES
from crypto import *
from curve import *
from datetime import datetime
import secrets
import hashlib
import os,pickle


curve = secp256k1
prkey = rand.getrandbits(256) % curve.p
pbkey = curve.mul(curve.G, prkey)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()
port = 12345
client_socket.connect((host, port))

sendpubkey = transkeygen(pbkey)
client_socket.send(sendpubkey.encode('utf-8'))


rpubkey = client_socket.recv(4096)
recvpubkey = concadekey(curve,rpubkey.decode('utf-8'))

print("\nprivate key = ", prkey)
print("public key = ", sendpubkey)
print("Received Public key = ", recvpubkey) 
print("\n\t\t***** public key received *****\n")

pointkey = curve.mul(recvpubkey, prkey)
print(pointkey)
shared_key = compress_point(pointkey)
print("Shared key = ", shared_key, "\n")

location = "C:/Users/Mohan/Desktop/"


while True:
	print("\n\n-------------------------------------------------------")
	print("1-Upload\t2-Download\t3-listOut\t0-exit")
	print("-------------------------------------------------------\n")

	ch = int(input("Your choice: "))

	if ch == 0:
		print("Your communication has been terminated...")
		break

	if ch == 1:
		fname = input("Enter the filename to be uploaded: ")
		#client_socket.send(filename.encode())
		filepath = os.path.join(location, fname)
		with open(filepath, 'r') as f:
			rtext = f.read()
			if not rtext:
				break 
			print("\nFile contents:")
			print("--------------\n")

			print(rtext,"\n")
			
			t1 = datetime.now()
			fdata = encrypt(rtext, shared_key)
			t2 = datetime.now()

			t = (t2-t1).total_seconds()
			#print(f'encryption time: {t} sec\n')
			

			fhash = hashlib.md5(str(fdata).encode('utf-8')).hexdigest()
			dobj = {'ch': ch, 'fname': fname, 'fdata': fdata, 'fhash': fhash} 

			client_socket.sendall(pickle.dumps(dobj))
			res = client_socket.recv(4096).decode('utf-8')
			print(res)


	elif ch == 2:
		fname = input("Enter the filename to be downloaded: ")
		dobj = {'ch': ch, 'fname': fname}

		client_socket.sendall(pickle.dumps(dobj))

		recvdata = client_socket.recv(4096)
		recvdata = pickle.loads(recvdata)

		vhash = hashlib.md5(str(recvdata['dcrdata']).encode('utf-8')).hexdigest()

		if recvdata['fhash'] == vhash:
			print("\nIntegrity is verified...\n")

		print('\nReceived file contents:')
		print('-----------------------\n')
		print(recvdata['dcrdata'], "\n")
		print("File has been downloaded successfully...")


	elif ch == 3:
		dobj = {'ch': ch }
		client_socket.sendall(pickle.dumps(dobj))
		files = client_socket.recv(4096)
		files = pickle.loads(files)

		print('\nYour files')
		if len(files) == 0:
			print("--empty--")
		print('-----------')

		for file in files:
			print('#',file, '\n')

	print("***********************************************************")

client_socket.close()
