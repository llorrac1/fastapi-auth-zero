import secrets
import time

from ...api.clients.schema import CreateClientRequestSchema, CreatedClientSchema, CreatedClientInDBSchema, ClientIdAndSecret

from ...db.firebase.db import ClientsDB

from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

    
class ClientsService:
    def __init__(
        self,
    ) -> None: 
        self.db = ClientsDB


    async def check_client_secret(self, client_id, client_secret) -> bool:
        if not await self.db.check_client(client_id, client_secret):
            return False
        
        return True

    async def _validate_client_secret_pair(self, client: CreatedClientSchema, client_id, client_secret): 
        if not client.client_id == client_id and not client.client_secret == client_secret:
            return False

        return True


    async def get_client_by_id(self, client_id: str, client_secret: str, provider_id: str = None) -> CreatedClientSchema:
        # if not provider_id: 
        #     # raise HTTPException(status_code=400, detail="need a provider id")
        #     pass

        try:
            client = await self.db.get_client(client_id)

            if not client:
                raise HTTPException(status_code=404, detail="invalid client id")

            else: 
                
                client = CreatedClientSchema(**client)
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="could not retrieve client")

        if not self._validate_client_secret_pair(client, client_id, client_secret):
            raise HTTPException(status_code=404, detail="invalid client id and secret")

        return client


    async def get_clients_by_provider_id(self, provider_id: str) -> dict: 
        if not provider_id: 
           raise HTTPException(status_code=404, detail="need a provider id")

        try: 
            clients = await self.db.get_clients(provider_id=provider_id)
            clients = [CreatedClientSchema(**client) for client in clients]
            return clients
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="could not retrieve clients from DB using this provider id")


    async def create_client(self, new_client: CreateClientRequestSchema) -> CreatedClientSchema:
        try: 
            created_client = CreatedClientSchema(
                **new_client.dict(),
                client_id = secrets.token_hex(16),
                client_secret = secrets.token_hex(32),
                created_at=time.time().__trunc__(),
                updated_at=time.time().__trunc__()
                )
    
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="could not populate client data - may be our fault, but please check the client parameters and try again")

        try: 
            if not await self.db.create_client(created_client.client_id, created_client.dict()): 
                raise HTTPException(status_code=400, detail="could not create client in DB - may be our fault, but please check the client parameters and try again")
        
            return created_client

        except Exception as e: 
            print(e)
            raise HTTPException(status_code=400, detail="could not create client in db")

