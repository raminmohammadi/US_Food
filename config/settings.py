from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str
    API_DESCRIPTION: str
    API_VERSION: str

    # Model Settings
    MODEL_PATH: str

    # Server Settings
    HOST: str
    PORT: int

    # Database Settings
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
