"""
JWT token utilities.
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from   app.config import config


class JWTHandler:
    """JWT token creation and verification."""
    
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS = 24
    
    @staticmethod
    def create_access_token(user_id: str, email: str) -> str:
        """
        Create a JWT access token.
        
        Args:
            user_id: User document ID
            email: User email
            
        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(hours=JWTHandler.ACCESS_TOKEN_EXPIRE_HOURS)
        
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, config.JWT_SECRET, algorithm=JWTHandler.ALGORITHM)
        return token
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                config.JWT_SECRET,
                algorithms=[JWTHandler.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
