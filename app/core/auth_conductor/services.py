from fastapi import Security, HTTPException, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer
from fastapi.security.api_key import APIKeyHeader
from typing import Any, Union, Optional, Callable
from pydantic import BaseModel, Field

from ..apikey.services import APIKeyService
apikey_svc = APIKeyService()
from ..token.services import JWTService
jwt_svc = JWTService()

class AccessToken(HTTPBearer):
    pass

class XAPIKey(APIKeyHeader):
    name="x-api-key"
    pass
    
class AuthenticationService:
    def __init__(self) -> None:
        self.AccessToken = AccessToken
        self.XAPIKey = XAPIKey


    async def get_jwt_bearer(self, 
        auth: HTTPAuthorizationCredentials
    ):
        print(auth)
        if not auth: 
            return None

        if auth: 
            return await jwt_svc.verify_jwt(auth.credentials)
        else:
            raise HTTPException(
            status_code=403,
            detail="Auth Token"
        )


    async def verify_token(self,
        x_token: str | None = Depends(HTTPBearer(auto_error=False))):
        if not x_token:
            return None

        check = await self.get_jwt_bearer(x_token)    
        if not check:
            raise HTTPException(status_code=403, detail="Invalid Authorization header")
        
        return x_token


    async def verify_key(self,
        x_api_key: str = Depends(APIKeyHeader(name="x-api-key", auto_error=False))):
        if not x_api_key:
            return None

        check = await apikey_svc.verify_api_key_header(x_api_key)
        if not check:
            raise HTTPException(status_code=403, detail="x-api-key header invalid")
        return x_api_key


    async def conductor(self,
        api_key: str | None = Depends(APIKeyHeader(name="x-api-key", auto_error=False)),
        auth_header: str | None = Depends(AccessToken(auto_error=False)),
    ) -> ...:
        if api_key is None and auth_header is None:
            raise HTTPException(status_code=403)
        
        if api_key and not auth_header:
            return await self.verify_key(api_key)

        if auth_header and not api_key:
            print(auth_header)
            return await self.verify_token(auth_header)

        raise HTTPException(status_code=403)