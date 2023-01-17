from pydantic import Field
from typing import Optional

from ...api.schema import BaseSchema as BaseModel

## TODO: Update bubble to reflect changes to model! 
class NewAPIKeyRequestSchema(BaseModel):
    provider_id: str = Field(...)
    name: str = Field(...)
    production: bool = Field(False)
    user_id: Optional[str] = Field(None)
    permissions: Optional[list] = Field(None)
    expires: Optional[int] = Field(None)

    class Config: 
        schema_extra = {
            "example": {
                "provider_id": "vdsbfdsanjbfabfdasbfda",
                "name": "APIKEy Name",
                "production": False
            }
        }


class BaseAPIKeySchema(BaseModel):
    provider_id: str = Field(...)
    name: str = Field(None)
    production: bool = Field(False)
    user_id: Optional[str] = Field(None)
    permissions: Optional[list] = Field(None)
    expires: Optional[int] = Field(None)


class APIKeySchema(BaseAPIKeySchema):
    api_key: str = Field(...)
    # is_revoked: bool = Field(False)
    # revoked_at: int = Field(None)
    created_at: int = Field(...)
    updated_at: int = Field(...)


class APIKeyInDBModel(APIKeySchema):
    is_deleted: bool = Field(False)
    deleted_at: int = Field(None)


class APIKeyResponse(APIKeySchema):
    class Config: 
        schema_extra = {
            "example": {"api_key": " ", "org_id": 1, "user_id": 1, "expires": 0, "is_revoked": False, "revoked_at": 0}
        } 


class CreatedAPIKeyResponseSchema(BaseModel):
    api_key: str 

    class Config: 
        schema_extra = {
            "example" : {"apiKey": "7d3e0410903cc9c20b05c37c0be5236d"}
        }


class InvalidatedAPIKeyResponseSchema(BaseModel): 
    message: str
    time: int


class APIKeyHeaderSchema(BaseModel):
    x_api_key: str = Field(None, title="x-api-key", alias="x-api-key")

    class Config: 
        schema_extra = {
            "example" : {'apiKey: 7d3e0410903cc9c20b05c37c0be5236d'}
        }

