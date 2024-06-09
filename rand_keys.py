from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from bitcoin import random_key, privtopub, pubtoaddr
import hashlib


addr = '12ie6iDXeyBcyjSgdrs8Jo5eUbHg4r2N7Q'	
public_key = b'\x04\x88\x86$\xb8\xaf\xf85\x89D\xd6\x16|\x9e-\xf2\xffm%\x00\x13\xd3\x1cf\x84z\xf1\xe1\xa7\xe5<\xb1\xaf\x07\x18\x15\xd7,\x1fX\x99\xc0\xa1\x86\xcc\xe8\x9b\x92\x06\x85\xea\x1do@*\n\xc3\xcd&\x9b6d\xc6\xa9&'
#my_private_key = public_key.hex()
public_key = '04888624b8aff8358944d6167c9e2df2ff6d250013d31c66847af1e1a7e53cb1af071815d72c1f5899c0a186cce89b920685ea1d6f402a0ac3cd269b3664c6a926'
#https://privatekeys.pw/key/f7f8e2eb962717e02f9748fe6f2dbd610152639c86f597846c59b78c5329d734
def private_key_to_addr(private_key):	
	my_public_key = privtopub(private_key)
	klen = 6
	if public_key[:klen] == my_public_key[:klen]:
		print('Private key = ' + private_key)
		print('Public key  = ' + my_public_key)
		my_bitcoin_address = pubtoaddr(my_public_key)
		print('Bitcoin Address = ' + my_bitcoin_address)
		return True

	klen = 4
	my_bitcoin_address = pubtoaddr(my_public_key)
	if my_bitcoin_address[:klen] == addr[:klen]:
		print('Private key = ' + private_key)
		print('Public key  = ' + my_public_key)
		print('Bitcoin Address = ' + my_bitcoin_address, ', expect addr is:', addr)
		return True
		#return my_bitcoin_address
	return False


def gen_rand_key():
	count = 0
	while True:
		count += 1
		if count % 1000 == 0:
			print('count =', count)
		my_private_key = random_key()
		ret = private_key_to_addr(my_private_key)
		if ret:
			break

	return
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
#gen_key()
gen_rand_key()

#decrypt()
#decrypt_mkey()
