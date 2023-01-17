from fastapi import FastAPI

from api import jwt

# from .middleware import CommitSessionMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(jwt.router)

    # app.add_middleware(CommitSessionMiddleware)

    @app.get("/health")
    async def healthcheck() -> None:
        return None

    return app
