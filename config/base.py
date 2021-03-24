from pydantic import BaseSettings


class Settings(BaseSettings):
    papers_tei: str = "papers_tei"


settings = Settings()
