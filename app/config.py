from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name:str= "SkillSwap Matching Service"
    port: int = 8001
    database_url: str

    class Config:
        env_file = ".env"
        extra= "ignore"

settings = Settings()       