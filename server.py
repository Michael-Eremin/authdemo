#FastAPI Server
import base64
import hmac
import hashlib
import json
from typing import Optional
from fastapi import FastAPI, Form, Cookie, Body
from fastapi.responses import Response


app = FastAPI()

SECRET_KEY = "3307c7193bda597c06dd418211ea2cde78a67ceddc688cc5500bc4ea64abd420"
PASSWORD_SALT = "8b5039944349eb24f01154e346424858cba054a765711933c210c6d59006d2dd"


def sign_data(data: str) -> str:
    '''Возвращает подписанные данные data'''
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()

def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username

def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256( (password + PASSWORD_SALT).encode() ).hexdigest().lower()
    stored_password_hash = users[username]["password"].lower()
    return password_hash == stored_password_hash


users = {
    "michael@user.com": {
        "name": "Михаил",
        "password": "96e6f23ae5efb74436b28c9f1af7981419a833c490903da7a97790e17fe4cc06",
        "balance": 100_000

    },
    "petr@user.com": {
        "name": "Петр",
        "password": "cac7a30e0346d0e1be335c7ab8df1e040c4af40118eb59cefe986b63b5e48279",
        "balance": 555_555
    }


}

@app.get("/")
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    return Response(
        f"Привет, {users[valid_username]['name']}!<br />"
        f"Баланс: {users[valid_username]['balance']}!",
        media_type="text/html")
    
    

@app.post("/login")
#def process_login_page(username : str = Form(...), password : str =Form(...)):
def process_login_page(data: dict = Body(...)):
    username = data["username"]
    password = data["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({
                "success": False,
                "message": "Я вас не знаю!"
            }),
            media_type="application/json")

    response = Response(
        json.dumps({
            "success": True,
            "message": f"Привет, {user['name']}!<br />Баланс: {user['balance']}"

        }),
        media_type="application/json")

    username_signed = base64.b64encode(username.encode()).decode() + "." + sign_data(username)    
    response.set_cookie(key="username", value=username_signed, expires=60*60*24*365)
    return response
