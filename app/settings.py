from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Library Management API"
    db_uri: str = "postgresql://user:password@db/library"
    models_module: str = "app.models"
    api_prefix: str = "/api"
    version: str = "v1"
    openapi_url: str = f"{api_prefix}/openapi.json"
    docs_url: str = f"{api_prefix}/docs"
    redoc_url: str = f"{api_prefix}/redoc"
    allowed_hosts: str = "*"
    root_path: str = str(Path(__file__).resolve().parent.parent)

    class Config:
        env_file = ".env"


settings = Settings()
