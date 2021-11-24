import hashlib
hash_object = hashlib.sha256("Caroline".encode("utf-8"))
hex_dig = int(hash_object.hexdigest(), 16) % 16
print(hex_dig)
