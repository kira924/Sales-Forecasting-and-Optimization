from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta

from app.models.schemas import UserSignUp, UserSignIn, Token, User, SuccessResponse
from app.services.auth_service import auth_service, get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=SuccessResponse)
async def sign_up(user_data: UserSignUp):
    """
    Register a new user
    """
    try:
        password = user_data.password[:72]
        user = auth_service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            company_name=user_data.company_name
        )
        
        return SuccessResponse(
            success=True,
            message="Account created successfully",
            data={"email": user["email"]}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/signin", response_model=Token)
async def sign_in(credentials: UserSignIn):
    """
    Login and get access token
    """
    user = auth_service.authenticate_user(
        credentials.email, 
        credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user

@router.post("/logout", response_model=SuccessResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout (client-side token removal)
    """
    return SuccessResponse(
        success=True,
        message="Logged out successfully"
    )