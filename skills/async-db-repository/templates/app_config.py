"""App config template (pydantic-settings + YAML overrides).

Only the DB part is shown. Keep the project's existing CORS/app fields.
"""

import yaml
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    postgresql_user: str
    postgresql_password: str
    postgresql_host: str
    postgresql_port: str
    postgresql_database: str

    @property
    def postgresql_connection_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgresql_user}:{self.postgresql_password}@"
            f"{self.postgresql_host}:{self.postgresql_port}/{self.postgresql_database}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    @classmethod
    def load_from_yaml(cls, yaml_path: str = "config.yaml") -> "AppConfig":
        with open(yaml_path, "r") as file:
            yaml_data = yaml.safe_load(file) or {}
        return cls(**yaml_data)


app_config = AppConfig.load_from_yaml()
