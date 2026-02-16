"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore import Client
from  app.dependencies import get_db
from  app.schemas.user import RegisterRequest, LoginRequest, AuthResponse
from  app.services.auth_service import UserRepository
from  app.utils.validators import PasswordHasher
from  app.utils.jwt import JWTHandler
from  app.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Client = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        request: Registration data
        db: Firestore client
        
    Returns:
        Authentication response with token
        
    Raises:
        HTTPException: If email already exists
    """
    user_repo = UserRepository(db)
    
    # Check if user already exists
    existing_user = await user_repo.get_user_by_email(request.email)
    if existing_user:
        logger.warning(f"Registration attempt with existing email: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = PasswordHasher.hash_password(request.password)
    
    # Create user
    user_id = await user_repo.create_user(
        name=request.name,
        email=request.email,
        password_hash=password_hash
    )
    
    # Generate JWT token
    token = JWTHandler.create_access_token(user_id=user_id, email=request.email)
    
    logger.info(f"User registered successfully: {request.email}")
    
    return AuthResponse(
        message="User created",
        token=token,
        user={
            "id": user_id,
            "name": request.name,
            "email": request.email
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    db: Client = Depends(get_db)
):
    """
    Login user and return JWT token.
    
    Args:
        request: Login credentials
        db: Firestore client
        
    Returns:
        Authentication response with token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user_repo = UserRepository(db)
    
    # Get user by email
    user = await user_repo.get_user_by_email(request.email)
    if not user:
        logger.warning(f"Login attempt with non-existent email: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not PasswordHasher.verify_password(request.password, user.password_hash):
        logger.warning(f"Login attempt with incorrect password: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    token = JWTHandler.create_access_token(user_id=user.id, email=user.email)
    
    logger.info(f"User logged in successfully: {request.email}")
    
    return AuthResponse(
        message="Login successful",
        token=token,
        user={
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    )
