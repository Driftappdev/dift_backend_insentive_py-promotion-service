import yaml
from pydantic import BaseSettings, Field

class MongoSettings(BaseSettings):
    uri: str
    db_name: str
    max_pool_size: int = 50
    min_pool_size: int = 10
    connect_timeout_ms: int = 10000

class RedisSettings(BaseSettings):
    url: str
    default_ttl: int = 3600

class RedpandaSettings(BaseSettings):
    bootstrap_servers: str
    promotion_topic: str = "promotions"
    group_id: str = "promotion_service_group"
    auto_offset_reset: str = "earliest"

class PromotionSettings(BaseSettings):
    default_discount_type: str = "percentage"
    default_discount_value: float = 10.0
    max_conditions: int = 10
    cross_feature_enabled: bool = True

class AdminAPISettings(BaseSettings):
    enabled: bool = True
    host: str = "0.0.0.0"
    port: int = 8001
    auth_required: bool = True
    jwt_secret: str = "CHANGE_ME"

class ServiceAPISettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    docs_enabled: bool = True

class Settings(BaseSettings):
    app_name: str
    environment: str = "development"
    log_level: str = "INFO"
    timezone: str = "UTC"

    mongo: MongoSettings
    redis: RedisSettings
    redpanda: RedpandaSettings
    promotion: PromotionSettings
    admin_api: AdminAPISettings
    service_api: ServiceAPISettings

def load_config(path="src/config/config.yaml") -> Settings:
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return Settings(**cfg)

# Load settings
settings = load_config()
