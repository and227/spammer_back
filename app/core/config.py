from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional, Dict, Any

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @validator('DATABASE_URL', pre=True)
    def build_db_url(cls, url: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(url, str):
            return url
        pg_dsn = PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            path=f"/{values.get('POSTGRES_DB', '')}"
        )
        return pg_dsn

    USER_LOGIN: str
    USER_PASSWORD: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKER_EXPIRE_MINUTES: int = 60 * 24 * 15

    JWT_SECRET: str
    JWT_ALGO: str

    REDIS_SERVER: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    REDIS_DATABASE_NUM: str

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()