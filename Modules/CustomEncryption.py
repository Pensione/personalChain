import hashlib as h

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

