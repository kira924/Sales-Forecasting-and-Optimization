from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Car Sales AI Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Model Paths
    PROFIT_MODEL_PATH: str = "models/profit_model.pkl"
    FEATURE_SCALER_PATH: str = "models/feature_scaler.pkl"
    PROPHET_MODEL_PATH: str = "models/prophet_model.pkl"
    PROPHET_SCALER_PATH: str = "models/prophet_scaler.pkl"
    
    # Database
    DATABASE_URL: str = "sqlite:///./car_sales.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)
os.makedirs("models", exist_ok=True)