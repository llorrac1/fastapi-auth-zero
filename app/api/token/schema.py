# api.jwt.schema.py 
from pydantic import Field
from typing import Optional
from enum import Enum

from ...api.schema import BaseSchema


class PublicAuthTokenSchema(BaseSchema):
    client_id: str
    client_secret: str

    class Config:
        title = "Auth Token"


class GetTokenResponseSchema(BaseSchema): # this is the response model for the /auth/token route
    access_token: str
    token_type: str = "Bearer"  


class AuthTokenSchemaSchema(BaseSchema):
    client_id: str
    client_secret: str
    audience: str = "api"
    grant_type: str = "client_credentials"
    expires: int


class GenerateAuthCodeSchema(BaseSchema):
    audience: str = Field('api', description='The audience of the token')
    scope: str = Field('openid', description='The scope of the token')
    response_type: str = Field('code', description='The response type of the token')
    client_id: str = Field('YOUR_CLIENT_ID', description='The client ID you received from Slick')
    state: Optional[str] = Field('YOUR_STATE', description='The state you received from Slick')


class GrantTypeSchema(str, Enum):
    authorization_code = "authorization_code"
    refresh_token = "refresh_token"


class BaseTokenSchema(BaseSchema):
    client_id: str = Field('YOUR_CLIENT_ID', description='The client ID you received from Slick')
    client_secret: str = Field('YOUR_CLIENT_SECRET', description='The client secret you received from Slick')


class GenerateAccessTokenSchema(BaseTokenSchema): 
    pass


class InternalGenerateAccessTokenSchema(GenerateAccessTokenSchema): 
    grant_type: GrantTypeSchema = Field('authorization_code', description='authorization_code or refresh_token')


class GenerateRefreshTokenSchema(BaseTokenSchema): 
    refresh_token: str = Field('YOUR_REFRESH_TOKEN', description='The refresh token you received from Slick')


class InternalGenerateRefreshTokenSchema(GenerateRefreshTokenSchema): 
    grant_type: str = Field('refresh_token', description='authorization_code or refresh_token')


class RevokeRefreshTokenSchema(GenerateRefreshTokenSchema):
    client_id: str = Field(...)
    client_secret: str = Field(...)
    refresh_token: str = Field(...)


class JWTDataSchema(BaseSchema):
    client_id: str = None
    provider_id: str = None
    prod: bool = False
    sub: str
    audience: str
    exp: float
    iat: float


class RefreshTokenInDBSchema(BaseSchema):
    refresh_token: str = Field(...)
    expires: int = Field(...)
    provider_id: str = Field(None)
    client_id: str = Field(None)
    is_revoked: bool = Field(False)
    revoked_at: int = Field(None)


class BaseCreatedAccessTokenResponseSchema(BaseSchema):
    access_token: str = Field(...)
    token_type: str = "Bearer" 
    expires_in: int


class CreatedAccessTokenResponseSchema(BaseCreatedAccessTokenResponseSchema):
    refresh_token: str = Field(...)

    class Config: 
        schema_extra = {
            "example": {
                "access_token":"eyJz93a...k4laUWw",
                "refresh_token":"GEbRxBN...edjnXbL",
                "token_type":"Bearer",
                "expires_in":86400
            }   
        }


class CreatedRefreshTokenResponseSchema(BaseCreatedAccessTokenResponseSchema):

    class Config: 
        schema_extra = {
            "example": {
                "access_token": "eyJ...MoQ",
                "expires_in": 86400,
                "token_type": "Bearer"
            }
        }


class SuccessfullyRevokedRefreshTokenResponseSchema(BaseSchema):
    message: str = "success"