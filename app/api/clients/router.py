from fastapi import APIRouter, Body, Depends

from .schema import CreateClientRequestSchema, CreatedClientResponseSchema
from ...core.clients.services import ClientsService
from ...core.auth_conductor.services import AuthenticationService
from ...core.admin.services import check_application

svc = ClientsService()
auth_svc = ClientsService()

router = APIRouter(
        tags=["Clients"],
        prefix="/admin/clients",
        dependencies=[Depends(check_application)],
)


@router.post("",
response_model=CreatedClientResponseSchema
)
async def create_client(payload: CreateClientRequestSchema = Body(...)):

    new_client = await svc.create_client(payload)

    return CreatedClientResponseSchema(**new_client.dict())



@router.get("/{providerid}"
)
async def retrieve_all_clients(providerid: str):
    return {
        "clients" : 
        await svc.get_clients_by_provider_id(provider_id=providerid)
    }



@router.get("/{providerid}/{clientid}"
)
async def retrieve_a_client(
    clientid: str, 
    providerid: str):
    return await svc.get_client_by_id(client_id=clientid, provider_id=providerid)

