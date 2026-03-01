from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import auth
from slowapi.errors import RateLimitExceeded
from limiter import limiter

app = FastAPI(
    title="API de mis Finanzas",
    description="API para gestionar y controlar gastos personales.",
    version="1.0.0"
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "rate limit alcanzado, inténtalo más tarde"}
    )

app.include_router(auth.router)

@app.get("/")
async def read_root():
    return {"status": "OK"}