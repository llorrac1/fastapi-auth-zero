from firebase_admin import credentials, initialize_app, db
import time

from fastapi.exceptions import HTTPException

from ...api.clients.schema import CreatedClientInDBSchema, CreatedClientSchema
from ...api.token.schema import RefreshTokenInDBSchema, CreatedRefreshTokenResponseSchema
from ...api.apikey.schema import APIKeyInDBModel

from .keys.key import key

cred = credentials.Certificate(key)
app = initialize_app(cred, 
    {
        'databaseURL': 'https://slick-97ec9-default-rtdb.firebaseio.com/'
        }
        )


class ClientsDB:
    async def create_client(id, client: dict) -> bool:
        print(client)
        try: 
            db.reference("clients").child(id).set(client)
            return True
        except Exception as e:
            print(e)
            return False


    async def get_client(client_id):
        try: 
            client = db.reference("clients").child(client_id).get() 
            if not client:
                return False
            try: 
                return client                
            except Exception as e:
                print(e)
                return e
        except Exception as e:
            print(e)
            return False


    async def get_clients(provider_id=None, user_id=None):
        if provider_id:
            data = db.reference("clients").order_by_child("provider_id").equal_to(provider_id).get()
            data2 = db.reference("clients").order_by_child("providerId").equal_to(provider_id).get()
            data = {**data, **data2}
            # Asthetically, this logic should live in Clients Service but ideally, it should be handled by firebase. Need to find out why it's not... 
            # return [await ClientsDB.get_client(d) for d in data]
            # response = db.reference("api_keys").order_by_child("provider_id").equal_to(org_id).get()
            # list_of_api_keys = [response[r] for r in response]
            response = [data[d] for d in data]
            return response
        
        if user_id:
            data = db.reference("clients").order_by_child("user_id").equal_to(user_id).get()
            data2 = db.reference("clients").order_by_child("userId").equal_to(user_id).get()
            data = {**data, **data2}
            # As above... 
            return [data(d) for d in data]
            
        data = db.reference("clients").get()
        return [data(d) for d in data]


    # def delete_client(client_id):
    #     db.reference("clients").child(client_id).delete()


    async def update_client(client_id, data):
        db.reference("clients").child(client_id).update(data)


    async def check_client(client_id, client_secret) -> CreatedClientSchema:
        try: 
            client = db.reference("clients").child(client_id).get()
            if client["client_id"] == client_id and client["client_secret"] == client_secret:
                print("client found")
                return CreatedClientSchema(**client)
            return False
        except Exception as e:
            print(e)
            return False


    async def invalidate_client(client_id):
        db.reference("clients").child(client_id).update({"is_deleted": True, "deleted_at": time.time()})


class TokenDB: 
    def create_token(id: str, token: dict):
        try: 
            # print(token)
            db.reference("tokens").child(id).set(token)
            print("stored refresh token")
            return True
        except Exception as e:
            print(e)
            return False

    def get_token(token):
        return db.reference("tokens").child(token).get()

    def get_tokens(user_id=None):
        if user_id:
            return db.reference("tokens").order_by_child("user_id").equal_to(user_id).get()
        return db.reference("tokens").get()

    def delete_token(token):
        db.reference("tokens").child(token).delete()

    def update_token(token, data):
        db.reference("tokens").child(token).update(data)

    def check_token(token):
        print("looking for refresh token")
        try:
            token = db.reference("tokens").child(token).get()

            if not token:
                print("no refresh token found")
                return False

            found_token = RefreshTokenInDBSchema(**token)
        
        except Exception as e:
            print(e)
            return False

        print("refresh token found")
        if found_token.is_revoked or found_token.expires < time.time():
            print("refresh token invalid or expired")
            return False
            
        return True
        

    def invalidate_token(token):
        try: 
            db.reference("tokens").child(token).update({"is_revoked": True, "revoked_at": time.time()})
            return True
        except Exception as e:
            print(e)
            return False


class APIKeyDB: 
    def create_api_key(id: str, key: dict):
        try: 
            db.reference("api_keys").child(id).set(key)
            return True
        except Exception as e:
            print(e)
            return False

    def get_api_key(key: str) -> dict or False:
        try:
            api_key = db.reference("api_keys").child(key).get()
            if not api_key:
                return False
            return api_key
        except Exception as e:
            print(e)
            return False

    async def get_api_keys_by_org_id(org_id: str):
        try:    
            ids = db.reference("api_keys").order_by_child("provider_id").equal_to(org_id).get()
            return ids 
        except Exception as e: 
            print(e)


    def get_api_keys(user_id=None, org_id=None) -> dict or False:
        if user_id:
            return db.reference("api_keys").order_by_child("user_id").equal_to(user_id).get()
        if org_id:
            try: 
                response = db.reference("api_keys").order_by_child("provider_id").equal_to(org_id).get()
                list_of_api_keys = [response[r] for r in response]
                return list_of_api_keys
            except Exception as e: 
                print(e)
                return False
    
        return db.reference("api_keys").get()


    def delete_api_key(key: str) -> bool:
        try: 
            current = APIKeyInDBModel(**APIKeyDB.get_api_key(key))
            current.updated_at = time.time()
            current.deleted_at = time.time()
            current.is_deleted = True
            # deleted = APIKeyInDBModel(**current)
            db.reference("api_keys").child(key).set(current.__dict__)
            return True
        except Exception as e:
            print(e)
            return False


    def update_api_key(key, data):
        db.reference("api_keys").child(key).update(data)


    def check_api_key(key):
        try:
            print("looking for api key")
            key = db.reference("api_keys").child(key).get()

            if not key:
                return False
            
            print("found apikey")
            return True
        except Exception as e:
            print(e)
            return False
