from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    B3_SEARCH_URL: str
    CVM_SEARCH_URL: str
    CVM_FRE_DOWNLOAD: str


settings = Settings()
