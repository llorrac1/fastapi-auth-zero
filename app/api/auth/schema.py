from ...api.schema import BaseSchema as BaseModel


class Client(BaseModel):
    client_id: str
    client_secret: str
    base_url: str
    audience: str
    grant_type: str
    scope: str


class User(BaseModel):
    user_id: str
    email: str
    email_verified: bool
    name: str
    picture: str
    updated_at: str
    created_at: str
    app_metadata: dict
    user_metadata: dict


class UserCreate(BaseModel):
    email: str
    password: str
    connection: str
    user_metadata: dict
    app_metadata: dict


# class Auth0User(BaseModel):
#     email: str
#     password: str
#     connection: str
#     scope: str
#     grant_type: str


class AuthCode(BaseModel):
    code: str
    state: str


class AuthToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    id_token: str


class AccessToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str
    id_token: str


class RefreshToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str
    id_token: str


class Login(BaseModel):
    email: str
    password: str
    scope: str
    connection: str
    grant_type: str


class IdToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: int
    iat: int
    nonce: str
    auth_time: int
    acr: str
    amr: str
    # at_hash: str
    # c_hash: str
    # name: str
    # given_name: str
    # family_name: str
    # nickname: str
    # picture: str
    # email: str
    # email_verified: bool
    # phone_number: str
    # phone_number_verified: bool
    # address: dict
    # updated_at: int
    # preferred_username: str
    # birthdate: str
    # gender: str
    # zoneinfo: str
    # locale: str
    # username: str