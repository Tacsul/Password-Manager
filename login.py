import json
import os
import bcrypt

from cryptography.fernet import Fernet

def upload_or_generate_key():
    if not os.path.exists("secret.key"):
        key=Fernet.generate_key()
        with open("secret.key","wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key","rb") as key_file:
            key=key_file.read()
    return Fernet(key)

fernet = upload_or_generate_key()

def register_user(username,password):
    password_bytes=password.encode('utf-8')
    
    salt=bcrypt.gensalt()
    password_hash_bytes=bcrypt.hashpw(password_bytes,salt)
    password_hash_text=password_hash_bytes.decode('utf-8')

    if os.path.exists('login.json'):
        with open('login.json','r') as f:
            login=json.load(f)
    else:
        login={}
    
    login[username]={
        "password":password_hash_text,
        "vault":{}
    }

    with open('login.json','w') as f:
        json.dump(login,f,indent=4)

def verify_login(username,password):
    if not os.path.exists('login.json'):
        return False
    
    with open('login.json','r') as f:
        login=json.load(f)

    if username not in login:
        return False
    
    password_bash=login[username]["password"].encode('utf-8')
    password_bytes=password.encode('utf-8')
    return bcrypt.checkpw(password_bytes,password_bash)
    
def verify_user(username):
    if not os.path.exists('login.json'):
        return False
    
    with open('login.json','r') as f:
        login=json.load(f)

    if username in login:
        return True
    return False

def add_password_safe(master_user,site,site_user,site_password):
    with open('login.json','r') as f:
        login=json.load(f)
    
    if "vault" not in login[master_user]:
        login[master_user]["vault"]={}

    user_crypt=fernet.encrypt(site_user.encode('utf-8')).decode('utf-8')
    pass_crypt=fernet.encrypt(site_password.encode('utf-8')).decode('utf-8')

    login[master_user]["vault"][site.lower()]={
        "username":user_crypt,
        "saved_password":pass_crypt
    }

    with open('login.json','w') as f:
        json.dump(login,f,indent=4)
    print(f"\n Parola pentru {site} a fost salvata!")

def print_safe(master_user):
    with open('login.json', 'r') as f:
        login=json.load(f)

    if "vault" not in login[master_user]:
        login[master_user]["vault"]={}
        with open('login.json','w') as f:
            json.dump(login,f,indent=4)

    safe=login[master_user]["vault"]

    if not safe:
        print("Your safe is empty. You have no password saved.")
        return
    
    print(f"\n === {master_user.upper()}'s Safe === ")
    for site,data in safe.items():
        user_decrypt=fernet.decrypt(data['username'].encode('utf-8')).decode('utf-8')
        pass_decrypt=fernet.decrypt(data['saved_password'].encode('utf-8')).decode('utf-8')
        print(f"Site: {site.capitalize()} | Username:{user_decrypt} | Password:{pass_decrypt}")
