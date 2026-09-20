from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    B3_SEARCH_URL: str
    CVM_SEARCH_URL: str
    CVM_FRE_DOWNLOAD: str
    HUGGING_FACE_MODEL: str
    QDRANT_API_KEY: str
    QDRANT_CLUSTER_URL: str
    HF_TOKEN: str


settings = Settings()
