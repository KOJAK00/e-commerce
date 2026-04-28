from pwdlib import PasswordHash
pwd_cxt = PasswordHash.recommended()

class hash():
    def argon2(password : str) :
        return pwd_cxt.hash(password) 
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)