from typing import Dict, List

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    admins: List[str] = ["353057906"]
    SUPABASE_URL: SecretStr
    SUPABASE_KEY: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
