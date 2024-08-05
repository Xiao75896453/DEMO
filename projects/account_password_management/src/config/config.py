from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STAGE: str
    SERVICE_PORT: int

    class Config:
        env_file = (
            "projects/account_password_management/.env",
            "projects/account_password_management/.env.stg",
            "projects/account_password_management/.env.prod",
        )


settings = Settings()
