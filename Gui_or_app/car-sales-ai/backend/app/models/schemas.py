from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from enum import Enum
from datetime import datetime

# ============================================
# AUTH SCHEMAS
# ============================================

class UserSignUp(BaseModel):
    """User registration schema"""
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., max_length=32, description="Password (min 8 characters)")
    company_name: Optional[str] = Field(None, max_length=100, description="Company name (optional)")
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if not v.strip():
            raise ValueError('Full name cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "password": "SecurePass123!",
                "company_name": "ABC Car Dealership"
            }
        }

class UserSignIn(BaseModel):
    """User login schema"""
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="User password")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!"
            }
        }

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None

class User(BaseModel):
    """User information schema"""
    email: str
    full_name: str
    company_name: Optional[str] = None
    created_at: Optional[datetime] = None

# ============================================
# FORECAST SCHEMAS
# ============================================

class ForecastViewType(str, Enum):
    """Forecast view types"""
    QUICK = "quick"
    FULL = "full"

class ForecastRequest(BaseModel):
    """Sales forecast request"""
    view_type: ForecastViewType = Field(
        default=ForecastViewType.FULL,
        description="View type: 'quick' for 3 months or 'full' for 12 months"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "view_type": "full"
            }
        }

class MonthlyForecast(BaseModel):
    """Monthly forecast data"""
    month: str = Field(..., description="Month name (e.g., 'Jan 2025')")
    forecast: float = Field(..., description="Predicted sales value")
    lower_bound: float = Field(..., description="Lower confidence bound (95%)")
    upper_bound: float = Field(..., description="Upper confidence bound (95%)")
    
    class Config:
        schema_extra = {
            "example": {
                "month": "Jan 2025",
                "forecast": 1501577.50,
                "lower_bound": 1325000.00,
                "upper_bound": 1678000.00
            }
        }

class ForecastResponse(BaseModel):
    """Sales forecast response"""
    total_forecast: float = Field(..., description="Total forecasted sales for the year")
    total_2024: float = Field(..., description="Total sales for 2024 (for comparison)")
    growth_rate: float = Field(..., description="Year-over-year growth rate (%)")
    monthly_forecast: List[MonthlyForecast] = Field(..., description="Monthly forecast breakdown")
    
    class Config:
        schema_extra = {
            "example": {
                "total_forecast": 18500000000.00,
                "total_2024": 17500000000.00,
                "growth_rate": 5.71,
                "monthly_forecast": [
                    {
                        "month": "Jan 2025",
                        "forecast": 1501577.50,
                        "lower_bound": 1325000.00,
                        "upper_bound": 1678000.00
                    }
                ]
            }
        }

# ============================================
# PRIORITY RANKING SCHEMAS
# ============================================

class CarMake(str, Enum):
    """Available car makes"""
    TOYOTA = "Toyota"
    BMW = "BMW"
    MERCEDES = "Mercedes"
    HONDA = "Honda"
    FORD = "Ford"
    HYUNDAI = "Hyundai"
    NISSAN = "Nissan"
    CHEVROLET = "Chevrolet"
    AUDI = "Audi"
    KIA = "Kia"

class SalesRegion(str, Enum):
    """Sales regions"""
    EAST = "East"
    WEST = "West"
    NORTH = "North"
    SOUTH = "South"
    CENTRAL = "Central"

class CarInput(BaseModel):
    """Car input for ranking"""
    make: str = Field(..., min_length=1, description="Car make (e.g., Toyota, BMW)")
    model: str = Field(..., min_length=1, description="Car model (e.g., Camry, X5)")
    year: int = Field(..., ge=2020, le=2026, description="Manufacturing year (2020-2026)")
    quantity: int = Field(default=1, ge=1, le=100, description="Number of units (1-100)")
    
    @validator('make', 'model')
    def validate_strings(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "make": "Mercedes",
                "model": "C-Class",
                "year": 2023,
                "quantity": 1
            }
        }

class RankingRequest(BaseModel):
    """Priority ranking request"""
    cars: List[CarInput] = Field(
        ..., 
        min_items=1, 
        max_items=50,
        description="List of cars to rank (1-50 cars)"
    )
    target_month: str = Field(
        ..., 
        min_length=3,
        description="Target month (e.g., 'November')"
    )
    target_year: int = Field(
        ..., 
        ge=2025, 
        le=2026,
        description="Target year (2025-2026)"
    )
    region: SalesRegion = Field(
        default=SalesRegion.EAST,
        description="Sales region"
    )
    profit_margin: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Profit margin factor (0-1, e.g., 0.15 for 15%)"
    )
    
    @validator('target_month')
    def validate_month(cls, v):
        valid_months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        if v not in valid_months:
            raise ValueError(f'Invalid month. Must be one of: {", ".join(valid_months)}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "cars": [
                    {
                        "make": "Mercedes",
                        "model": "C-Class",
                        "year": 2023,
                        "quantity": 1
                    },
                    {
                        "make": "Toyota",
                        "model": "Camry",
                        "year": 2023,
                        "quantity": 2
                    }
                ],
                "target_month": "November",
                "target_year": 2025,
                "region": "East",
                "profit_margin": 0.15
            }
        }

class RiskLevel(str, Enum):
    """Risk level categories"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class CarRanking(BaseModel):
    """Car ranking result"""
    make: str = Field(..., description="Car make")
    model: str = Field(..., description="Car model")
    year: int = Field(..., description="Manufacturing year")
    age: int = Field(..., description="Car age (years)")
    quantity: int = Field(..., description="Quantity")
    profit: float = Field(..., description="Predicted profit ($)")
    confidence: float = Field(..., description="Prediction confidence (%)")
    risk: RiskLevel = Field(..., description="Risk level (LOW/MEDIUM/HIGH)")
    
    class Config:
        schema_extra = {
            "example": {
                "make": "Mercedes",
                "model": "C-Class",
                "year": 2023,
                "age": 2,
                "quantity": 1,
                "profit": 2008.45,
                "confidence": 67.5,
                "risk": "LOW"
            }
        }

class RankingResponse(BaseModel):
    """Priority ranking response"""
    rankings: List[CarRanking] = Field(..., description="Ranked list of cars")
    
    class Config:
        schema_extra = {
            "example": {
                "rankings": [
                    {
                        "make": "Mercedes",
                        "model": "C-Class",
                        "year": 2023,
                        "age": 2,
                        "quantity": 1,
                        "profit": 2008.45,
                        "confidence": 67.5,
                        "risk": "LOW"
                    },
                    {
                        "make": "Toyota",
                        "model": "Camry",
                        "year": 2023,
                        "age": 2,
                        "quantity": 2,
                        "profit": 1782.00,
                        "confidence": 52.3,
                        "risk": "MEDIUM"
                    }
                ]
            }
        }

# ============================================
# RESPONSE MODELS
# ============================================

class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str
    data: Optional[dict] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"id": 123}
            }
        }

class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    error: str
    details: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Validation error",
                "details": "Email is required"
            }
        }

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: Optional[str] = None
    environment: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "environment": "production",
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }