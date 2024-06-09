from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from bitcoin import random_key, privtopub, pubtoaddr
import hashlib
import requests

pks=[
 b'\x04\x88\x86$\xb8\xaf\xf85\x89D\xd6\x16|\x9e-\xf2\xffm%\x00\x13\xd3\x1cf\x84z\xf1\xe1\xa7\xe5<\xb1\xaf\x07\x18\x15\xd7,\x1fX\x99\xc0\xa1\x86\xcc\xe8\x9b\x92\x06\x85\xea\x1do@*\n\xc3\xcd&\x9b6d\xc6\xa9&',

#b'\x04r\x11\xa8$\xf5[PR(\xe4\xc3\xd5\x19L\x1f\xcf\xaa\x15\xa4V\xab\xdf7\xf9\xb9\xd9z@@\xaf\xc0s\xde\xe6\xc8\x90d\x98O\x038R7\xd9!g\xc1>#dF\xb4\x17\xaby\xa0\xfc\xaeA*\xe31kw',
#b"\x04\x94\xb9\xd3\xe7l[\x16)\xec\xf9\x7f\xff\x95\xd7\xa4\xbb\xda\xc8|\xc2`\x99\xad\xa2\x80f\xc6\xff\x1e\xb9\x19\x12#\xcd\x89q\x94\xa0\x8d\x0c'&\xc5t\x7f\x1d\xb4\x9e\x8c\xf9\x0eu\xdc>5P\xae\x9b0\x08o<\xd5\xaa", 
#b'\x04\x96\xb58\xe8SQ\x9crj,\x91\xe6\x1e\xc1\x16\x00\xae\x13\x90\x81:b|f\xfb\x8b\xe7\x94{\xe6<R\xdau\x897\x95\x15\xd4\xe0\xa6\x04\xf8\x14\x17\x81\xe6"\x94r\x11f\xbfb\x1es\xa8,\xbf#B\xc8X\xee', 
]

def pk_address():
	print('Bitcoin Address                       balance')
	for public_key in pks:
		my_public_key = public_key.hex()
		print('Public key  = ' + my_public_key)
		prefix = my_public_key[0:2]
		if prefix == '04':
			my_bitcoin_address = pubtoaddr(my_public_key)
			print('B:', my_bitcoin_address, '  ',  get_balance(my_bitcoin_address))
	
			#return
			#my_public_key = privtopub(my_private_key)
			if int(my_public_key[-1], 16) % 2 == 0:
			    my_compressed_public_key = '02' + my_public_key[2:66]
			else:
			    my_compressed_public_key = '03' + my_public_key[2:66]
			#print('Compressed Public key = ' + my_compressed_public_key)
		elif prefix == '02' or prefix == '03':
			my_compressed_public_key = my_public_key
		
		my_compressed_bitcoin_address = pubtoaddr(my_compressed_public_key)
		print('C:', my_public_key[:8], my_compressed_bitcoin_address, '  ',  get_balance(my_compressed_bitcoin_address))
	exit(0)

def get_balance(addr):
	url = 'https://api.blockchain.info/haskoin-store/btc/address/' + addr + '/balance'
	resp = requests.get(url)
	json = resp.json()
	if 'error' in json:
		balance = 0
	else:
		balance = json['confirmed']
	return str(balance)

#12ie6iDXeyBcyjSgdrs8Jo5eUbHg4r2N7Q
#<ckey item: {'public_key': b'\x04\x88\x86$\xb8\xaf\xf85\x89D\xd6\x16|\x9e-\xf2\xffm%\x00\x13\xd3\x1cf\x84z\xf1\xe1\xa7\xe5<\xb1\xaf\x07\x18\x15\xd7,\x1fX\x99\xc0\xa1\x86\xcc\xe8\x9b\x92\x06\x85\xea\x1do@*\n\xc3\xcd&\x9b6d\xc6\xa9&', 
#	'encrypted_private_key': b'\xcf\x9a\x1e\xd3 \xd1i8\x82*\xde@\x04o\x85\xd5\xf7ZT\xd2gn\x7f\xe1\xbf\xa9\xb4z\xed\t\xd8\xdd!\x97\xdd\x0f\xaf~\xe9fb\xdfy0\xaa\xb8\xce;'}>
#<mkey item: {'nID': 1, 
#	'encrypted_key': b'l\xdbGQ\xf9\xed\xc9\xdc\xa0\xed\x04\xda\xf1\xa5yo.\xcbf\x91F\x0c\x19\xdeDXM+"\xd2\x01Yxt\xecL\xedv\xc8\x06E^\x07\x9em\x81\x1d\xa8', 
#	'salt': b'\xfb\xf1\x92\xd3\xba\xf6\xbb\x02', 
#	'nDerivationMethod': 0, 'nDerivationIterations': 126145, 'otherParams': b''}>
def decrypt():
	password = b'my_secure_password'
	
	encrypted_private_key = b'\xcf\x9a\x1e\xd3 \xd1i8\x82*\xde@\x04o\x85\xd5\xf7ZT\xd2gn\x7f\xe1\xbf\xa9\xb4z\xed\t\xd8\xdd!\x97\xdd\x0f\xaf~\xe9fb\xdfy0\xaa\xb8\xce;'
	public_key = b'\x04\x88\x86$\xb8\xaf\xf85\x89D\xd6\x16|\x9e-\xf2\xffm%\x00\x13\xd3\x1cf\x84z\xf1\xe1\xa7\xe5<\xb1\xaf\x07\x18\x15\xd7,\x1fX\x99\xc0\xa1\x86\xcc\xe8\x9b\x92\x06\x85\xea\x1do@*\n\xc3\xcd&\x9b6d\xc6\xa9&'
	
	#  AES  Scrypt 
	salt = encrypted_private_key[:16]  #  16 
	nonce = encrypted_private_key[16:32]  #  16  nonce
	ciphertext = encrypted_private_key[32:]  # 
	
	#  Scrypt 
	key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
	
	#  AES-GCM 
	cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
	private_key = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
	
	print('Decrypted Private Key:', private_key.hex())
	print('Public Key:', public_key.hex())
	exit(0)


def decrypt_mkey():
	mkey = {
		'encrypted_key': b'l\xdbGQ\xf9\xed\xc9\xdc\xa0\xed\x04\xda\xf1\xa5yo.\xcbf\x91F\x0c\x19\xdeDXM+"\xd2\x01Yxt\xecL\xedv\xc8\x06E^\x07\x9em\x81\x1d\xa8', 
		'nDerivationIterations': 126145, 
	    'salt': b'\xfb\xf1\x92\xd3\xba\xf6\xbb\x02'
	}
	print(mkey['salt'].hex())
	exit(0)
	password = b'my_password'
	
	key = hashlib.sha256(password + mkey['salt']).digest()
	
	cipher = AES.new(key, AES.MODE_CBC, IV=mkey['salt'].hex())
	decrypted_key = cipher.decrypt(mkey['encrypted_key'])
	
	print('Decrypted Key:', decrypted_key)
	

#https://privatekeys.pw/key/1ae168fea63dc339a3c58419466ceaeef7f632653266d0e1236431a950cfe52a
def private_key_to_addr(private_key):
	print('Private key = ' + private_key)
	
	my_public_key = privtopub(private_key)
	print('Public key  = ' + my_public_key)
	
	my_bitcoin_address = pubtoaddr(my_public_key)
	print('Bitcoin Address     = ' + my_bitcoin_address)
	return my_bitcoin_address

def gen_key():
	my_private_key = '0000000000000000000000000000000000000000000000000000000000000002'
	my_private_keys = '1ae168fea63dc339a3c58419466ceaeef7f632653266d0e1236431a950cfe52a'
	#encrypted_private_key = b'\xcf\x9a\x1e\xd3 \xd1i8\x82*\xde@\x04o\x85\xd5\xf7ZT\xd2gn\x7f\xe1\xbf\xa9\xb4z\xed\t\xd8\xdd!\x97\xdd\x0f\xaf~\xe9fb\xdfy0\xaa\xb8\xce;'
	#my_private_keys = encrypted_private_key.hex()
	private_key_to_addr(my_private_keys)
	for i in range(int(len(my_private_keys)/2) - 32):
		my_private_key = my_private_keys[i*2:64+i*2]
		#large_number = 0x1E99423A4EDF92D71A713E5A768F63251E2B2C6AAFD208240FAE9E9E52817707
		#my_private_key = format(large_number, '064x')
		private_key_to_addr(my_private_key)

#		print('balance     = ' + get_balance(my_bitcoin_address))
	exit(0)
	
	#return
	my_public_key = privtopub(my_private_key)
	if int(my_public_key[-1], 16) % 2 == 0:
	    my_compressed_public_key = '02' + my_public_key[2:66]
	else:
	    my_compressed_public_key = '03' + my_public_key[2:66]
	print('Compressed Public key = ' + my_compressed_public_key)
	
	my_compressed_bitcoin_address = pubtoaddr(my_compressed_public_key)
	print('Compressed Address = ' + my_compressed_bitcoin_address)
	print('balance     = ' + get_balance(my_compressed_bitcoin_address))


def gen_rand_key():
	my_private_key = random_key()
	addr = private_key_to_addr(my_private_key)
	print('balance     = ' + get_balance(addr))

	my_public_key = privtopub(my_private_key)
	if int(my_public_key[-1], 16) % 2 == 0:
	    my_compressed_public_key = '02' + my_public_key[2:66]
	else:
	    my_compressed_public_key = '03' + my_public_key[2:66]
	print('Compressed Public key = ' + my_compressed_public_key)
	
	my_compressed_bitcoin_address = pubtoaddr(my_compressed_public_key)
	print('Compressed Address = ' + my_compressed_bitcoin_address)
	print('balance     = ' + get_balance(my_compressed_bitcoin_address))

#pk_address()
gen_key()
#gen_rand_key()

#decrypt()
#decrypt_mkey()
