from fastapi import Request, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey

import time
import secrets 

from ...api.apikey.schema import NewAPIKeyRequestSchema, APIKeySchema, APIKeyInDBModel
from ...db.firebase.db import APIKeyDB

from ..clients.services import ClientsService

clients_svc = ClientsService()

# # Initialise API Key security variables 
API_KEY_NAME = "x-api-key"

class APIKey(APIKeyHeader):
    pass

# api_key_header = APIKey(name=API_KEY_NAME, auto_error=False)

class APIKeyService:
    def __init__(self) -> None:
        self.db = APIKeyDB
        self.api_key_header = APIKey(name=API_KEY_NAME, auto_error=False)

    async def generate_api_key(self, new_api_key: NewAPIKeyRequestSchema) -> APIKeySchema:
        # try:  
        #     validated = await clients_svc.validate_client_secret(new_api_key.client_id, new_api_key.client_secret)
        #     if not validated:
        #         raise HTTPException(status_code=404, detail="invalid client id and secret")

        # except Exception as e:
        #     print(e)
        #     raise HTTPException(status_code=400, detail="could not validate client id and secret at this time")


        try: 
            api_key = secrets.token_hex(16)
            created_api_key = APIKeySchema(
                **new_api_key.dict(), 
                api_key=api_key, 
                created_at=time.time().__trunc__(), 
                updated_at=time.time().__trunc__()
                )
            APIKeyDB.create_api_key(api_key, created_api_key.dict())
            return created_api_key
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="could not save API Key")


    async def get_api_key(self, api_key: str) -> APIKeySchema:
        try: 
            key = APIKeyInDBModel(**APIKeyDB.get_api_key(api_key))

        except Exception as e: 
            print(e)
            raise HTTPException(status_code=400, detail="could not retrieve API Key")
            
        if key: 
            if not key.is_deleted:
                return APIKeySchema(**key.dict())

            print("api key is deleted")
            raise HTTPException(status_code=404, detail="invalid API Key")


    async def get_all_api_keys(self, provider_id: str):
        try:
            keys = APIKeyDB.get_api_keys(org_id = provider_id)
            if keys:
                return [APIKeySchema(**key) for key in keys]
            else:
                return False

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail='unknown')


    async def invalitate_api_key(self, api_key: str) -> bool:
        try:  
            APIKeyDB.delete_api_key(api_key)
            return True
        except Exception as e:
            print(e)
            return False


    async def check_api_keys(self, unverified_key: str): 
        # If there was a cache, you might consider checking it here 
        print("received check apikey request... " + str(unverified_key))
        key = APIKeyDB.check_api_key(unverified_key)
        return key


    async def verify_api_key_header(self, 
        unverified_key: str
    ) -> bool:

        if unverified_key: 
            check = await APIKeyService().check_api_keys(unverified_key)
            if check:
                return check
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid API Key"
                )

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid API Key"
            )
