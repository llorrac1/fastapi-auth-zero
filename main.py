from fastapi import FastAPI, Body, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware

from .app.core.auth_conductor.services import AuthenticationService 

conductor = AuthenticationService().conductor

import time

from .app.api.token import router as jwt_router
from .app.api.apikey import router as apikey_router
from .app.api.clients import router as client_router


app = FastAPI(
        title="Slick Auth Service",
        version="0.0.1",
        terms_of_service="https://www.slickco.io/terms/",
        contact={
            "name": "API Team",
            "email": "api@slickco.io",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        docs_url='/', redoc_url="/redoc",
        servers=[
        ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.router.include_router(jwt_router.router)
app.router.include_router(apikey_router.router)
app.router.include_router(client_router.router)


@app.get("/auth", dependencies=[Depends(conductor)])
async def auth():
    return {
        "message": "Auth OK 🔐"
    }