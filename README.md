# Secure-File-Transmission-Using-Hybrid_Cryptogtraphy


In this, a hybrid approach has been used in order to handle file encryption and decryption mechanisms. 

For this, we used three algorithms namely, **ECC and AES algorithms** along with **MD5** for hashing purposes.

#### a). ECC 
Elliptic Curve Cryptography is a public-key approach based on the algebraic structure of elliptic curves over finite fields that can be used to create faster smaller and more efficient cryptographic keys. ECC generates keys through the properties of very large prime number. ECC uses Elliptic Curve Diffie-Hellman (ECDH) key exchange protocol for key exchange mechanism.

**Private keys (sk)** are generated random followed by Public keys are calculated by multiplying the private key with generator point of the curve.

>PKa = SKa * G

>PKb = SKb * G

The **Shared key** will be calculated which can be used as encryption and decryption purposes.

>Encryption key (side a) = PKb * SKa  

>Decryption key (side b) = PKa * SKb


#### b). AES
Advanced Encryption Standard (AES) algorithm is the most popular and widely adopted symmetric key approach. It make use of 128/192/256 bit keys. It is stronger and faster than triple-DES and provide full specification and design implementation. In this, AES is the primary algorithm for encryption and decryption of files.
In this project, we will be using **AES-ECB mode** which divide our input data into block size of 256 bits and process each separately and combine all together. We will be using 256 bits of key size.

#### C). MD5
Message Digest 5 (MD5) is a widely used hash function, produce a 128-bit hash value. It can be used as a checksum to verify data integrity. 


### Implementation:
python language has been used for implementation of the hybrid algorithm. For demonstration, we make use of socket programming in python with file encryption (upload) and file decryption (download) mechanisms. We used ECDH algorithm for key exchange mechanism and AES to carry out encryption and decryption processes using generated ECDH shared key. 
We have created 4 modules.
- **Curve.py** – this module contains methods for EC generation and operations.
- **Crypto.py** – this module contains the hybrid code for encryption, decryption and key formatting 
- **Server.py** and **Client.py** – these are nodes to be communicated 

