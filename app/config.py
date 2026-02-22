from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name:str= "SkillSwap Matching Service"
    port: int = 8001
    database_url: str


#redis upstash
    redis_upstash_rest_url: str
    redis_upstash_rest_token: str

    class Config:
        env_file = ".env"
        extra= "ignore"

settings = Settings()       