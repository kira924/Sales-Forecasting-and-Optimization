from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.models.schemas import ForecastRequest, ForecastResponse, User
from app.services.ml_service import ml_service
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/forecast", tags=["Sales Forecasting"])
logger = logging.getLogger(__name__)

@router.post("/sales", response_model=ForecastResponse)
async def generate_sales_forecast(
    request: ForecastRequest = ForecastRequest(),
    current_user: User = Depends(get_current_user)
):
    """
    Generate sales forecast for the next 12 months
    
    - **view_type**: 'quick' for 3 months or 'full' for 12 months
    """
    try:
        logger.info(f"Generating forecast for user: {current_user.email}")
        
        result = ml_service.generate_sales_forecast(request.view_type)
        
        return ForecastResponse(**result)
        
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate forecast"
        )

@router.get("/health")
async def forecast_health_check():
    """
    Check if forecast service is healthy
    """
    try:
        # Quick test
        test_result = ml_service.generate_sales_forecast("quick")
        
        return {
            "status": "healthy",
            "prophet_model": ml_service.prophet_model is not None,
            "test_passed": len(test_result['monthly_forecast']) > 0
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }