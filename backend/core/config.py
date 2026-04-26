from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    mongodb_url: str
    mongodb_db_name: str
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    ml_artifacts_dir: str = "./ml_artifacts"
    static_figures_dir: str = "./static/figures"
    cors_origins: str = "http://localhost:3000"
    bert_model_path: str = "./ml_artifacts/bert_sentiment"
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    t5_model_name: str = "t5-base"
    app_name: str = "ComplaintIQ API"
    app_version: str = "1.0.0"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()