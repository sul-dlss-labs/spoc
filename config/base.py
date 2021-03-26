from pydantic import BaseSettings


class Settings(BaseSettings):
    # Default value mapped in docker-compose
    papers_tei: str = "/usr/share/papers_tei"


settings = Settings()
