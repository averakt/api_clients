import uvicorn
from app.models.database import database
from app.routers import users
from fastapi import FastAPI
import os

app = FastAPI(docs_url="/users/docs", redoc_url="/users/redoc", openapi_url="/users/openapi.json")

if os.environ['USE_MOCK_FOR_TEST'] == 1:
    aaa = 1
else:
    @app.on_event("startup")
    async def startup():
        await database.connect()


    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
