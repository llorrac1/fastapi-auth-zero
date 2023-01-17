from pydantic import Field
from typing import Optional
from enum import Enum

from ...api.schema import BaseSchema as BaseModel

class ClientIdAndSecret(BaseModel):
    client_id: str = Field(...)
    client_secret: Optional[str] = Field(...)

class CheckClient(BaseModel):
    client_id: str = Field(...)
    client_secret: Optional[str] = Field(...)


class BaseClientSchema(BaseModel):
    name: str = Field(...)
    provider_id: str = Field(...)
    user_id: str = Field(None)


class CreateClientRequestSchema(BaseClientSchema):
    description: str = Field(None)
    plan: str = Field(...)
    production: bool = Field(False)


class CreatedClientSchema(CreateClientRequestSchema):
    client_id: str = Field(...)
    client_secret: str = Field(...)
    created_at: str = Field(None)
    updated_at: str = Field(None)


class CreatedClientInDBSchema(CreatedClientSchema):
    deleted_at: str = Field(None)
    is_deleted: bool = Field(False)


class CreatedClientResponseSchema(CreatedClientSchema):
    pass