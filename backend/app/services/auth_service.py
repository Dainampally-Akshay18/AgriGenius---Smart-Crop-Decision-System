"""
User repository for Firestore operations.
"""
from datetime import datetime
from typing import Optional
from google.cloud.firestore import Client
from   app.models.user import User
from   app.utils.logger import logger


class UserRepository:
    """Repository for user database operations."""
    
    COLLECTION_NAME = "users"
    
    def __init__(self, db: Client):
        """
        Initialize user repository.
        
        Args:
            db: Firestore client instance
        """
        self.db = db
        self.collection = db.collection(self.COLLECTION_NAME)
    
    async def create_user(self, name: str, email: str, password_hash: str) -> str:
        """
        Create a new user in Firestore.
        
        Args:
            name: User's name
            email: User's email
            password_hash: Hashed password
            
        Returns:
            User document ID
        """
        user_data = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow()
        }
        
        doc_ref = self.collection.document()
        doc_ref.set(user_data)
        
        logger.info(f"User created: {email} (ID: {doc_ref.id})")
        return doc_ref.id
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User's email
            
        Returns:
            User object if found, None otherwise
        """
        query = self.collection.where("email", "==", email).limit(1)
        docs = query.stream()
        
        for doc in docs:
            user_data = doc.to_dict()
            user_data["id"] = doc.id
            return User(**user_data)
        
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by document ID.
        
        Args:
            user_id: User document ID
            
        Returns:
            User object if found, None otherwise
        """
        doc_ref = self.collection.document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            user_data = doc.to_dict()
            user_data["id"] = doc.id
            return User(**user_data)
        
        return None
