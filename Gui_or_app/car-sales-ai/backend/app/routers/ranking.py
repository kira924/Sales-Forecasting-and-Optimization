from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.models.schemas import RankingRequest, RankingResponse, User
from app.services.ml_service import ml_service
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/ranking", tags=["Priority Ranking"])
logger = logging.getLogger(__name__)

@router.post("/priority", response_model=RankingResponse)
async def generate_priority_ranking(
    request: RankingRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate priority ranking for car inventory
    
    - **cars**: List of cars to rank (1-50 cars)
    - **target_month**: Month when you expect to sell
    - **target_year**: Year of expected sale (2025-2026)
    - **region**: Sales region (East, West, North, South, Central)
    - **profit_margin**: Optional profit margin factor (0-1)
    """
    try:
        logger.info(f"Generating ranking for user: {current_user.email}, cars: {len(request.cars)}")
        
        result = ml_service.generate_priority_ranking(
            cars=request.cars,
            target_month=request.target_month,
            target_year=request.target_year,
            region=request.region,
            profit_margin=request.profit_margin
        )
        
        return RankingResponse(**result)
        
    except Exception as e:
        logger.error(f"Error generating ranking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate ranking"
        )

@router.get("/health")
async def ranking_health_check():
    """
    Check if ranking service is healthy
    """
    try:
        from app.models.schemas import CarInput
        
        # Quick test
        test_cars = [
            CarInput(make="Toyota", model="Camry", year=2023, quantity=1)
        ]
        test_result = ml_service.generate_priority_ranking(
            cars=test_cars,
            target_month="November",
            target_year=2025,
            region="East",
            profit_margin=None
        )
        
        return {
            "status": "healthy",
            "profit_model": ml_service.profit_model is not None,
            "test_passed": len(test_result['rankings']) > 0
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }