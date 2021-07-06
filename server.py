import socket
from Cryptodome.Cipher import AES
from tinyec import registry
from curve import *
from crypto import *
from datetime import datetime
import secrets, hashlib
import os, sys
import pickle, codecs


curve = secp256k1
prkey = rand.getrandbits(256) % curve.p
pbkey = curve.mul(curve.G,prkey)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345

server_socket.bind((host, port))
server_socket.listen(5)

conn, address = server_socket.accept()
print("Connection from: " + str(address)+"\n")


sendpubkey = transkeygen(pbkey)

rpubkey = conn.recv(4096)
recvpubkey = concadekey(curve,rpubkey.decode('utf-8'))

print("private key = ", prkey)
print("public key = ", sendpubkey)
print("Received public key = ", recvpubkey)
print("\n\t\t***** public key received *****\n")

pointkey= curve.mul(recvpubkey, prkey)
print(pointkey)
shared_key = compress_point(pointkey)
print("Shared key = ", shared_key, "\n")

conn.send(sendpubkey.encode('utf-8'))

location = "./files/encrypted/"
#filename = conn.recv(4096).decode()


while True:
	recv = conn.recv(4096)
	recv = pickle.loads(recv)

	if recv['ch'] == 1:
		vhash = hashlib.md5(str(recv['fdata']).encode('utf-8')).hexdigest()

		if recv['fhash'] == vhash:
			print("Integrity is verified...\n")
			path = os.path.join(location, recv['fname']) 
			file = open(path, 'w')
			file.close()
			#print(type(recv['fdata']))

			#data = codecs.decode(recv['fdata'])
			#print(type(data))
			with open(path, 'wb+') as f2:
				f2.write(recv['fdata'])

			msg = "file has been uploaded successfully..."
			print("\nencrypted file contents:")
			print("------------------------")

			print("\n", recv['fdata'], "\n")
			print(msg)
			conn.send(msg.encode("utf-8"))

		else:
			msg = "file has been modified..."
			print(msg)
			conn.send(msg.encode("utf-8"))


	elif recv['ch'] == 2:
		
		print("Requested filename:", recv['fname'], "\n")

		path1 = os.path.join(location, recv['fname'])
		with open(path1, 'rb+') as f1:
			rdata = f1.read()


		t1 = datetime.now()
		dcr_data = decrypt(rdata, shared_key)
		t2 = datetime.now()

		t = (t2-t1).total_seconds()
		#print(f"decryption time: {t} sec\n")

		path2 = os.path.join("./files/decrypted/", recv['fname']) 
		file = open(path2, 'w')
		file.close()

		with open(path2, 'r+') as f2:
			print("\ndecrypted file contents:")
			print('------------------------\n')
			print(dcr_data, "\n")
			f2.write(str(dcr_data))

		fhash = hashlib.md5(str(dcr_data).encode('utf-8')).hexdigest()
		obj = { 'dcrdata': dcr_data, 'fhash': fhash }

		conn.sendall(pickle.dumps(obj))


	elif recv['ch'] == 3:
		files = os.listdir(location)
		conn.sendall(pickle.dumps(files))
		continue
	
	print('***********************************************\n')
					
conn.close()

