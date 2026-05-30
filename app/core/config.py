from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    KEYOPENROUTER: str = "Faltou a keyOpenRouter"
    URLOPENROUTER: str = "Falto a URL da IA"
    MODEL_IA: str = "faltou o Modelo de IA"

    URLEVO: str = "Faltou a URL do Evo"
    KEYEVO: str = "Faltou a Key do Evo"
    LOCALURL: str = "Faltou a URL local do RobZap"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
