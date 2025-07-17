from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".conf",
        env_file_encoding="utf-8",
        extra="ignore"  # Игнорировать лишние переменные в .conf
    )


class ServerConfig(BaseConfig):

    host: str
    port: int

    
server_config = ServerConfig()