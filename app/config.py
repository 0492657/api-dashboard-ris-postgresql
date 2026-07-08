from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    secret_key_api: str
    base_url: str

    db_host_ris: str
    db_port_ris: str
    db_database_ris: str
    db_username_ris: str
    db_password_ris: str

    db_host_maris: str
    db_port_maris: str
    db_database_maris: str
    db_username_maris: str
    db_password_maris: str

    db_host_orange: str
    db_port_orange: str
    db_database_orange: str
    db_username_orange: str
    db_password_orange: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

settings = Settings()