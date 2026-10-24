from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hashed_password(password:str):
    return password_hash.hash(password)

def verify_hash(password:str,hash_password:str):
    return password_hash.verify(password,hash_password)
