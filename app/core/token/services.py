import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from jose import JWTError, jwt
import secrets
from fastapi.exceptions import HTTPException

from ...db.firebase.db import TokenDB

from ...api.token.schema import JWTDataSchema, RefreshTokenInDBSchema, CreatedRefreshTokenResponseSchema, CreatedAccessTokenResponseSchema
from ..clients.services import ClientsService

clients_svc = ClientsService()

JWT_SECRET = "14f75b618e1109e51b3d940121f5377188dc3b1cecb82f9de76ab86325cf0bc9"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ACCESS_TOKEN_EXPIRE_SECONDS = 86400
REFRESH_TOKEN_EXPIRE_SECONDS = 2592000

class JWTService:
    def __init__(
        self
    ) -> None:
        self.db = TokenDB


    def generate_access_token(self, client_id, provider_id) -> JWTDataSchema:
        print("fleshing out JWT data...")
        new_token = JWTDataSchema(
            # client_id=client_id,
            provider_id=provider_id,
            sub=provider_id,
            audience="https://api.slickco.io/",
            exp=time.time().__trunc__() + ACCESS_TOKEN_EXPIRE_SECONDS,
            iat=time.time().__trunc__()
        )
        print("access token created: ",  new_token)

        return new_token


    def generate_refresh_token(self, client_id, provider_id) -> RefreshTokenInDBSchema:
        print("fleshing out refresh token data...")
        new_token = RefreshTokenInDBSchema(
            refresh_token=secrets.token_hex(32),
            provider_id=provider_id,
            client_id=client_id,
            expires=time.time().__trunc__() + REFRESH_TOKEN_EXPIRE_SECONDS
        )
        print("refresh token created: ",  new_token)

        return new_token


    def validate_refresh_token(self, refresh_token: str) -> bool:
        print("validating refresh token...")
        if not TokenDB.check_token(refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        return True


    def invalidate_refresh_token(self, refresh_token: str) -> bool:
        print("trying to invalidate refresh token...")
        if len(refresh_token) > 64: # 64 (32 bit) is the length of the refresh token in the DB
            raise HTTPException(status_code=401, detail="Invalid refresh token - too many characters")

        if not TokenDB.invalidate_token(refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        return True


    def signJWT_for_client(self, client_id: str, provider_id: str, using_refresh_token: False) -> CreatedAccessTokenResponseSchema or CreatedRefreshTokenResponseSchema:
        print("generating token...")
        payload = self.generate_access_token(client_id, provider_id)
        
        try: 
            print("trying to sign Jwt")
            access_token = jwt.encode(payload.dict(), JWT_SECRET, algorithm=JWT_ALGORITHM)
        except JWTError as e:
            print(e)
            return None

        
        if using_refresh_token:
            token_response = CreatedRefreshTokenResponseSchema(
                access_token=access_token,
                expires_in=payload.exp,
                token_type="bearer"
            )
            return token_response


        refresh_token = self.generate_refresh_token(client_id, provider_id)
        
        try: 
            TokenDB.create_token(refresh_token.refresh_token, refresh_token.dict())
        except Exception as e:
            print(e)
            return HTTPException(status_code=500, detail="Error creating refresh token")

        
        token_response = CreatedAccessTokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token.refresh_token,
            expires_in=payload.exp,
            token_type="bearer"
        )

        return (token_response)

    # TODO: Implement a better naming convention and flow here... 
    # async def create_access_token(self, client_id: str, provider_id: str, using_refresh_token: False) -> CreatedAccessTokenResponseSchema or CreatedRefreshTokenResponseSchema:
    #     print("generating token...")
    #     pass

    def signJWT_for_user(self, user_id: str) -> Dict[str, str]:
        payload = {
            "user_id": user_id,
            "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


        return self.token_response(auth_token=token)


    def decodeJWT(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            print(decoded_token)
            return decoded_token if decoded_token["exp"] >= time.time() else None
        except:
            return {}


    async def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = self.decodeJWT(jwtoken)
            print(payload)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid



  