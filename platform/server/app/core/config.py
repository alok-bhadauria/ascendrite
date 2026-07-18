import os
import urllib.parse
from typing import List, Union
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve absolute path to the workspace root directory dynamically
# __file__ is platform/server/app/core/config.py
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # platform/server/app
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # g:/Projects/ascendrite
env_file_path = os.path.join(root_dir, ".env.local")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding="utf-8", extra="ignore")

    # Application Configuration
    APP_NAME: str = "Ascendrite"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_LOG_LEVEL: str = "INFO"

    # Database Configuration
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = "ascendrite"

    # JWT Configuration
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security Configuration
    SECURITY_COOKIE_SECURE: bool = False
    SECURITY_COOKIE_HTTPONLY: bool = True
    SECURITY_COOKIE_SAMESITE: str = "lax"

    # CORS Configuration
    CORS_ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("CORS_ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # Logging Configuration
    LOG_FORMAT: str = "json"

    # AI Providers Configuration
    LLM_PROVIDER: str = "openai"
    EMBEDDING_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_CHAT_MODEL: str = "gpt-4o"

    # Operational Feature Flags
    FEATURE_ENABLE_AI: bool = True
    FEATURE_ENABLE_BACKGROUND_WORKERS: bool = True
    FEATURE_ENABLE_EMAIL: bool = True

    # Development & Testing Feature Flags
    FEATURE_ENABLE_SEARCH: bool = True
    FEATURE_ENABLE_REGISTRATION: bool = True
    FEATURE_ENABLE_ANALYTICS: bool = True

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_PRESET: str = "ascendrite"

    # Future Third-Party Integrations / Driver URL Strings (Derived exclusively at runtime)
    REDIS_URL: str = ""
    POSTGRES_URL: str = ""

    # Role-Separated PostgreSQL Variables
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "ascendrite"
    POSTGRES_ADMIN_USER: str = "ascendrite_admin"
    POSTGRES_ADMIN_PASSWORD: str = ""
    POSTGRES_APP_USER: str = "ascendrite_app"
    POSTGRES_APP_PASSWORD: str = ""

    # Role-Separated MongoDB Variables
    MONGODB_HOST: str = "127.0.0.1"
    MONGODB_PORT: int = 27017
    MONGODB_DATABASE: str = "ascendrite"
    MONGODB_AUTH_SOURCE: str = "admin"
    MONGODB_ADMIN_USER: str = "ascendrite_admin"
    MONGODB_ADMIN_PASSWORD: str = ""
    MONGODB_APP_USER: str = "ascendrite_app"
    MONGODB_APP_PASSWORD: str = ""

    # Role-Separated Cache Variables
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DATABASE: int = 0
    REDIS_ADMIN_USER: str = "ascendrite_admin"
    REDIS_ADMIN_PASSWORD: str = ""
    REDIS_APP_USER: str = "ascendrite_app"
    REDIS_APP_PASSWORD: str = ""

    # RustFS Object Storage Variables
    S3_ENDPOINT: str = "http://127.0.0.1:9000"
    S3_CONSOLE_ENDPOINT: str = "http://127.0.0.1:9001"
    S3_REGION: str = "ap-south-1"
    S3_ADMIN_USER: str = "ascendrite_admin"
    S3_ADMIN_PASSWORD: str = ""
    S3_APP_PARENT_USER: str = "ascendrite_app"
    S3_RUNTIME_ACCESS_KEY: str = "ascendrite_runtime"
    S3_RUNTIME_SECRET_KEY: str = ""

    # Vector DB Backend Selection
    VECTOR_BACKEND: str = "pgvector"

    # Runtime Profile Query Helpers
    @property
    def current_profile(self) -> str:
        return self.APP_ENV.lower()

    @property
    def is_development(self) -> bool:
        return self.current_profile == "development"

    @property
    def is_testing(self) -> bool:
        return self.current_profile == "testing"

    @property
    def is_production(self) -> bool:
        return self.current_profile == "production"

    @property
    def is_debug_enabled(self) -> bool:
        return self.APP_DEBUG

    def is_feature_enabled(self, feature_name: str) -> bool:
        flag_name = f"FEATURE_ENABLE_{feature_name.upper()}"
        return getattr(self, flag_name, False)

    @model_validator(mode="after")
    def resolve_legacy_urls(self) -> "Settings":
        if not self.MONGODB_URI:
            encoded_mongo_user = urllib.parse.quote(self.MONGODB_APP_USER, safe="")
            encoded_mongo_pass = urllib.parse.quote(self.MONGODB_APP_PASSWORD, safe="")
            if encoded_mongo_user and encoded_mongo_pass:
                self.MONGODB_URI = f"mongodb://{encoded_mongo_user}:{encoded_mongo_pass}@{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DATABASE}?authSource={self.MONGODB_AUTH_SOURCE}"
            elif encoded_mongo_user:
                self.MONGODB_URI = f"mongodb://{encoded_mongo_user}@{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DATABASE}?authSource={self.MONGODB_AUTH_SOURCE}"
            else:
                self.MONGODB_URI = f"mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DATABASE}?authSource={self.MONGODB_AUTH_SOURCE}"
        self.MONGODB_DB_NAME = self.MONGODB_DATABASE

        if not self.POSTGRES_URL:
            encoded_pg_user = urllib.parse.quote(self.POSTGRES_APP_USER, safe="")
            encoded_pg_pass = urllib.parse.quote(self.POSTGRES_APP_PASSWORD, safe="")
            if encoded_pg_user and encoded_pg_pass:
                self.POSTGRES_URL = f"postgresql://{encoded_pg_user}:{encoded_pg_pass}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
            elif encoded_pg_user:
                self.POSTGRES_URL = f"postgresql://{encoded_pg_user}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
            else:
                self.POSTGRES_URL = f"postgresql://{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

        if not self.REDIS_URL:
            encoded_redis_user = urllib.parse.quote(self.REDIS_APP_USER, safe="")
            encoded_redis_pass = urllib.parse.quote(self.REDIS_APP_PASSWORD, safe="")
            if encoded_redis_user and encoded_redis_pass:
                self.REDIS_URL = f"redis://{encoded_redis_user}:{encoded_redis_pass}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"
            elif encoded_redis_user:
                self.REDIS_URL = f"redis://{encoded_redis_user}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"
            else:
                self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"

        return self

settings = Settings()
