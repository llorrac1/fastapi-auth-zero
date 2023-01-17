from fastapi import APIRouter, HTTPException, Body

from .schema import GenerateAccessTokenSchema, GenerateRefreshTokenSchema, RevokeRefreshTokenSchema, CreatedAccessTokenResponseSchema, CreatedRefreshTokenResponseSchema, SuccessfullyRevokedRefreshTokenResponseSchema
from ...core.token.services import JWTService 
from ...core.clients.services import ClientsService

jwtsvc = JWTService()
clients_svc = ClientsService()

router = APIRouter(
    tags=["Access Token"],
    prefix="/token"
)


@router.post(""
, response_model=CreatedAccessTokenResponseSchema
)
async def generate_access_token(payload: GenerateAccessTokenSchema = Body(...)):
    ## TODO: Move to JWT Service 
    client = await clients_svc.get_client_by_id(
        client_id=payload.client_id, 
        client_secret=payload.client_secret)
    if not client:
        raise HTTPException(status_code=400, detail="Wrong details!")

    try:
        token = jwtsvc.signJWT_for_client(payload.client_id, client.provider_id, False)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Couldn't generate token")


@router.post("/refresh",
response_model=CreatedRefreshTokenResponseSchema
)
async def generate_refresh_token(payload: GenerateRefreshTokenSchema = Body(...)):
    client = await clients_svc.get_client_by_id(payload.client_id, payload.client_secret)
    if not client:
        raise HTTPException(status_code=400, detail="Wrong details!")

    if not jwtsvc.validate_refresh_token(payload.refresh_token):
        raise HTTPException(status_code=400, detail="Could not refresh access token.")

    try:
        token = jwtsvc.signJWT_for_client(payload.client_id, client.provider_id, using_refresh_token=True)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Could not refresh access token")


@router.post("/revoke", 
response_model=SuccessfullyRevokedRefreshTokenResponseSchema)
async def revoke_refresh_token(
    payload: RevokeRefreshTokenSchema,
    ):
    client = clients_svc.validate_client_secret(payload.client_id, payload.client_secret)
    if not client:
        raise HTTPException(status_code=400, detail="Wrong details!")

    if not jwtsvc.invalidate_refresh_token(payload.refresh_token):
        raise HTTPException(status_code=400, detail="Could not revoke token.")

    return {
        "message": "success"
    }
    