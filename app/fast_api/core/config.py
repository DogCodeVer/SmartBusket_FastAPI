from pydantic import BaseSettings

class Settings(BaseSettings):
    PARSER_URL: str = "https://example.com/catalog"

    class Config:
        env_file = ".env"

settings = Settings()
