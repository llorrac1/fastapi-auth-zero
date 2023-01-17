from fastapi import Header, Depends
from fastapi.exceptions import HTTPException

from .applications import applications

async def check_application(x_app_secret: str = Header(None)) -> bool:
    for app in applications:
        if app.secret == x_app_secret:
            return True 
    raise HTTPException(status_code=400, detail="x-app-secret header invalid")


