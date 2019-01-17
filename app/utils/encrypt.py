from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex,a2b_hex
from datetime import datetime,timedelta
from app.auth.models import User
from flask import current_app
from app import db

def encrypt_token(email,expiration):
    key = current_app.config["AES_KEY"].encode('utf-8')
    data = (email + "|" + datetime.strftime(datetime.utcnow(),"%Y-%m-%d %H:%M:%S")+"|"+str(expiration)).encode('utf-8')
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key,AES.MODE_CFB,iv)
    ciphertext = iv + cipher.encrypt(data)
    return b2a_hex(ciphertext).decode('utf-8')

def reset_passwd(ciphertext,password):
    key = current_app.config["AES_KEY"].encode('utf-8')  
    ciphertext = a2b_hex(ciphertext.encode('utf-8')) 
    decrypt = AES.new(key,AES.MODE_CFB,ciphertext[:16])
    decrypttext = decrypt.decrypt(ciphertext[16:]).decode()
    email = decrypttext.split("|")[0]
    time_str = decrypttext.split("|")[1]
    expiration =  decrypttext.split("|")[2]
    start_time = datetime.strptime(time_str,"%Y-%m-%d %H:%M:%S")
    now_time = datetime.utcnow()
    user = User.query.filter_by(email = email).first()
    if now_time - start_time > timedelta(seconds=int(expiration)) or user is None:
        return False
    user.password = password
    db.session.commit()
    return True

def generate_confirmation_token(user_id,expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'],expiration)
    return s.dumps({'confirm':user_id}).decode("utf-8") 

def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
    except:
        return False
        
    user_id = data.get("confirm")
    user = User.query.filter_by(id=user_id).first()
    if user is None :
        return False

    if user.confirmed:
        return True

    user.confirmed = True
    db.session.commit()
    return True


