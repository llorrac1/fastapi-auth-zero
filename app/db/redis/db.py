from decouple import config
from redis_om import HashModel, Field, Migrator, get_redis_connection
from typing import Optional

REDIS_URL = config("REDIS_URL")
REDIS_PORT = config("REDIS_PORT")
REDIS_PASSWORD = config("REDIS_PASSWORD")


redis = get_redis_connection(
    port=REDIS_PORT,
    decode_responses=True,
)

class BaseRedisClass(HashModel):
    class Meta:
        database = redis


class RefreshToken(BaseRedisClass):
    pass


class User(BaseRedisClass):
    id = Field()
    email = Field()
    password = Field()
    is_active = Field()
    is_superuser = Field()


class Token(BaseRedisClass):
    access_token = Field()
    token_type = Field()
    user_id = Field()

    @classmethod
    def get_user_id(cls, access_token: str) -> Optional[str]:
        token = cls.get(access_token)
        if token:
            return token.user_id
        return None

    @classmethod
    def get_user(cls, access_token: str) -> Optional[User]:
        user_id = cls.get_user_id(access_token)
        if user_id:
            return User.get(user_id)
        return None

    @classmethod
    def get_user_id_from_refresh_token(cls, refresh_token: str) -> Optional[str]:
        token = cls.get(refresh_token)
        if token:
            return token.user_id
        return None

    @classmethod
    def get_user_from_refresh_token(cls, refresh_token: str) -> Optional[User]:
        user_id = cls.get_user_id_from_refresh_token(refresh_token)
        if user_id:
            return User.get(user_id)
        return None

    @classmethod
    def get_user_id_from_reset_token(cls, reset_token: str) -> Optional[str]:
        token = cls.get(reset_token)
        if token:
            return token.user_id
        return None

    @classmethod
    def get_user_from_reset_token(cls, reset_token: str) -> Optional[User]:
        user_id = cls.get_user_id_from_reset_token(reset_token)
        if user_id:
            return User.get(user_id)
        return None

    @classmethod
    def get_user_id_from_verify_token(cls, verify_token: str) -> Optional[str]:
        token = cls.get(verify_token)
        if token:
            return token.user_id
        return None

    @classmethod
    def get_user_from_verify_token(cls, verify_token: str) -> Optional[User]:
        user_id = cls.get_user_id_from_verify_token(verify_token)
        if user_id:
            return User.get(user_id)
        return None

    @classmethod
    def get_user_id_from_change_password_token(cls, change_password_token: str) -> Optional[str]:
        token = cls.get(change_password_token)
        if token:
            return token.user_id
        return None


class RefreshToken(BaseRedisClass):
    refresh_token = Field()
    user_id = Field()

    @classmethod
    def save_token(cls, user_id: str, refresh_token: str) -> str:
        refresh_token = cls(RefreshToken(refresh_token=refresh_token, user_id=user_id))
        return refresh_token.refresh_token

    @classmethod
    def get_token(cls, refresh_token: str) -> Optional[str]:
        token = cls.get(refresh_token)
        if token:
            return token.user_id
        return None

    @classmethod
    def get_user(cls, refresh_token: str) -> Optional[User]:
        user_id = cls.get_user_id(refresh_token)
        if user_id:
            return User.get(user_id)
        return None





class Migrate:
    def __init__(self):
        self.migrator = Migrator(redis)

    def migrate(self):
        self.migrator.run(User)
        self.migrator.run(Token)