from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from flask import request, make_response
import requests, jwt, os
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

MAIN_API_URL = os.getenv(
    "MAIN_API_URL",
    "http://127.0.0.1:5000"
)

class LoginSchema(BaseModel):
    email: str
    senha: str

class registerSchema(BaseModel):
    name: str
    email: str
    senha: str

info = Info(title="auth API", version="1.0.0")

app = OpenAPI(__name__, info=info)
CORS(app,
     origins=["http://localhost:5173"],
     supports_credentials=True
    )


@app.get("/check-main")
def check_main():
    params={ "name": "Taua"}
    response = requests.get("http://127.0.0.1:5000/usuarios", params=params)
    print(response.url)

    return {
        "status_code": response.status_code,
        "response": response.json()  
    }, 200

@app.post('/auth/register')
def register(body: registerSchema):
    response = requests.post(f"{MAIN_API_URL}/usuario",
                             json={
                                 "name": body.name,
                                 "email": body.email,
                                 "senha": body.senha
                             } )
    return response.json(), response.status_code

@app.post('/auth/login')
def login(body: LoginSchema):
    response = requests.post(f"{MAIN_API_URL}/auth/verify", 
                             json={
                                 "email": body.email,
                                 "senha": body.senha
                             })
    if response.status_code == 200:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
        refresh_expiration = datetime.now(timezone.utc) + timedelta(days=7) 
        user_data = response.json()
        payload = {
            "usuId": user_data.get("usuId"),
            "email": user_data.get("email"),
            "type": "access",
            "exp": expiration
        }
        refresh_payload ={
            "usuId": user_data.get("usuId"),
            "email": user_data.get("email"),
            "type": "refresh",
            "exp": refresh_expiration
        }
        token = jwt.encode(
            payload,
            "secret_test",
            algorithm="HS256"
        )
        refresh_token = jwt.encode(
            refresh_payload,
            "secret_test",
            algorithm="HS256"
        )
        response = make_response(
            {
                "Message": "Login successful"
            }, 
            200
        )
        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=30 * 60,
            path="/"
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
            path="/auth/refresh"
        )
        return response
    else:
        return response.json(), response.status_code

@app.post('/auth/validate')
def validate_token():
    access_token = request.cookies.get("access_token")
    if not access_token:
        return {"Message": "Access token missing"}, 401
    try:
        decoded_token = jwt.decode(
            access_token,
            "secret_test",
            algorithms=["HS256"]
        )
        if decoded_token.get("type") != "access":
            return {"Message": "Invalid Token Type"}
        return decoded_token, 200
    except jwt.ExpiredSignatureError:
        return {"Message": "Token Expired"}, 401
    except jwt.InvalidTokenError:
        return {"Message": "Invalid Token"}, 401

@app.post('/auth/refresh')
def refresh_token():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return {"Message": "Invalid Authorization header format"}, 401
    try:
        decoded_token = jwt.decode(
            refresh_token,
            "secret_test",
            algorithms=["HS256"]
        )
        if decoded_token.get("type") != "refresh":
            return {"Message": "Invalid Token Type"}, 401
        new_expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
        new_payload = {
            "usuId": decoded_token.get("usuId"),
            "email": decoded_token.get("email"),
            "type": "access",
            "exp": new_expiration
        }
        new_access_token = jwt.encode(
            new_payload,
            "secret_test",
            algorithm="HS256"
        )
        response = make_response(
            {"Message": "Access token refreshed"}, 200
        )
        response.set_cookie(
            "access_token",
            new_access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=30 * 60,
            path="/"
        )
        return response
    
    except jwt.ExpiredSignatureError:
        return {"Message": "Token Expired"}, 401
    except jwt.InvalidTokenError:
        return {"Message": "Invalid Token"}, 401

@app.post('/auth/logout')
def logout():
    response = make_response(
        {"Message": "Logout successful"}, 200
    )
    response.delete_cookie(
        "access_token",
        path="/",
        secure=False,
        httponly=True,
        samesite="Lax"
    ) 
    response.delete_cookie(
        "refresh_token",
        path="/auth/refresh",
        secure=False,
        httponly=True,
        samesite="Lax"
    )
    return response

    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)


        
    
