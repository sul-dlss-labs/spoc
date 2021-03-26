from pydantic import BaseSettings


class Settings(BaseSettings):
    # Default value mapped in docker-compose
    papers_tei: str = "/usr/share/papers_tei"
    api_url: str = "https://taxa.stanford.edu"


settings = Settings()
