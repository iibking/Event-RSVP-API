from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import event

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Schema is managed by Alembic migrations (run: alembic upgrade head).
app.include_router(event.router)


@app.get("/", status_code=200)
async def health_check():
    return {"status": "API is running"}