from hashlib import blake2b
from hmac import compare_digest
from os import urandom
from binascii import hexlify

def create_key(): # create random key
    return hexlify(urandom(24)).decode('utf-8') 
    
def sign(public_key, secret_key): # create digital signature from public_key and secret key
    public_key = public_key.encode('utf-8')
    secret_key = secret_key.encode('utf-8')
    h = blake2b(digest_size=24, key=secret_key)
    h.update(public_key)
    return h.hexdigest()

def verify(public_key, secret_key, sig): # verify digital signature
    good_sig = sign(public_key, secret_key)
    return compare_digest(good_sig, sig)




    
    
