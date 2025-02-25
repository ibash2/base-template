from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@app-db:5432/bot"
    )

    tron_rpc_url: str = Field(alias="TRON_RPC_URL")
    tron_rpc_api_key: str = Field(alias="TRON_RPC_API_KEY")


def load_config() -> Config:
    return Config()  # type: ignore
