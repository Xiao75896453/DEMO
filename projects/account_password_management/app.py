import uvicorn
from src.config.config import settings

if __name__ == "__main__":
    if settings.STAGE == "dev":
        uvicorn.run(
            "src.main:app", host="0.0.0.0", port=settings.SERVICE_PORT, reload=True
        )
    elif settings.STAGE == "stg":
        uvicorn.run("src.main:app", host="0.0.0.0", port=settings.SERVICE_PORT)
    elif settings.STAGE == "prod":
        uvicorn.run("src.main:app", host="0.0.0.0", port=settings.SERVICE_PORT)
