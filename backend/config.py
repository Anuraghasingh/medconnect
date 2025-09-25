import os


class AppConfig:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # Database
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "anurag")
    DB_NAME = os.environ.get("DB_NAME", "medconnect")
    DB_POOL_NAME = os.environ.get("DB_POOL_NAME", "smart_health_pool")
    DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", "5"))


