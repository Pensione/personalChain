import hashlib as h
from ecdsa import SigningKey, NIST256p, VerifyingKey

def multiple_hash( input_string, count, **kwargs):
    result = input_string
    for i in range(0, count):
        result = h.sha256(bytes(str(input_string), encoding = "utf-8")).hexdigest()
        
    return result

def double_hash( input_string, **kwargs):
    ROUND_COUNT = 2
    for x in range(0, ROUND_COUNT):
        result = h.sha256(bytes(str(input_string), encoding = "utf-8")).hexdigest()
    
    return result

def vk_hex_to_bytes(vk, curve):
    byte_key = bytes.fromhex( vk )
    vk = VerifyingKey.from_string( byte_key, curve )
    return vk

def sk_hex_to_bytes(sk, curve):
    byte_key = bytes.fromhex( sk )
    sk = VerifyingKey.from_string( byte_key, curve )
    return sk
    

