from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost/cvm_tmcel"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # ML Models
    churn_model_path: str = "./ml_models/churn_model.pkl"
    nbo_model_path: str = "./ml_models/nbo_model.pkl"
    
    # Campaign Settings
    sms_gateway_url: Optional[str] = None
    sms_api_key: Optional[str] = None
    
    # Feature Flags
    enable_real_sms: bool = False
    enable_ml_predictions: bool = True
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()