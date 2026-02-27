from fastapi import FastAPI
from routers import auth

app = FastAPI(
    title="API de mis Finanzas",
    description="API para gestionar y controlar gastos personales.",
    version="1.0.0"
)

app.include_router(auth.router)

@app.get("/")
async def read_root():
    return {"status": "OK"}