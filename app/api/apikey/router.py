from fastapi import APIRouter, HTTPException, Header, Depends

from .schema import NewAPIKeyRequestSchema, APIKeyResponse, CreatedAPIKeyResponseSchema, InvalidatedAPIKeyResponseSchema

from ...core.clients.services import ClientsService
from ...core.apikey.services import APIKeyService
from ...core.auth_conductor.services import AuthenticationService
from ...core.admin.services import check_application

client_svc = ClientsService()
apikey_svc = APIKeyService()


router = APIRouter(
        tags=["API Key"],
        prefix="/apikey",
        dependencies=[Depends(check_application)],
)


@router.post("", response_model=CreatedAPIKeyResponseSchema)
async def generate_api_key(
    payload: NewAPIKeyRequestSchema
    ) -> APIKeyResponse:

    apikey = await apikey_svc.generate_api_key(payload)

    if not apikey: 
        return 

    else: 
        return CreatedAPIKeyResponseSchema(api_key=apikey.api_key)


@router.get("/{providerid}")
async def retrieve_all_api_keys(providerid: str):
    try: 
        keys = await apikey_svc.get_all_api_keys(provider_id=providerid)
        return {
            "apikeys": 
            keys
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="could not process request")


@router.get("/{providerid}/{apikey}", response_model=APIKeyResponse)
async def retrieve_api_key(
    apikey: str,
    providerid: str
    ): 
    
    key = await apikey_svc.get_api_key(api_key=apikey)
    if key: 
        return APIKeyResponse(**key.dict())

    return key
        


@router.post("/{providerid}/{apikey}/invalidate")
async def invalidate_api_key(apikey: str, providerid: str):
    try: 
        invalidated = await apikey_svc.invalitate_api_key(api_key=apikey)
        if invalidated: 
            return {"message" : "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="could not invalidate apikey")