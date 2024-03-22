from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str

@dataclass
class ApiKey:
    token: str

@dataclass
class Config:
    api: ApiKey
    db: DatabaseConfig

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
    api=ApiKey(
        token=env('API_TOKEN')
    ),
    db=DatabaseConfig(
        database=env('DB_DATABASE'),
        db_user=env('DB_USER'),
        db_password=env('DB_PASSWORD'),
        db_host=env('DB_HOST')
    ))

