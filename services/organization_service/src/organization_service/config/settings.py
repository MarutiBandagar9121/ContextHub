from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str = "organization_service"
    app_version:str = "0.1.0"
    port: int = 8001
    database_url:str

    jwt_public_key_path: str
    jwt_algorithm: str = "RS256"

    user_service_host:str = "http://localhost:8000"
    user_service_name:str = "Contexthub_Auth_Service"
    user_service_timeout:int = 30
    user_service_retry_count:int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()