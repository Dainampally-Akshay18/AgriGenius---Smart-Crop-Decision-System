"""
Dependency injection for Firebase and other services.
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client
from app.config import config
from app.utils.logger import logger


class FirebaseService:
    """Singleton Firebase service."""
    
    _instance = None
    _db: Client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Firebase Admin SDK once."""
        try:
            # Check if already initialized
            firebase_admin.get_app()
            logger.info("Firebase already initialized")
        except ValueError:
            # Initialize Firebase with credentials from environment
            # Build complete service account credential dictionary
            cred_dict = {
                "type": "service_account",
                "project_id": config.FIREBASE_PROJECT_ID,
                "private_key_id": "",  # Not required for authentication
                "private_key": config.FIREBASE_PRIVATE_KEY.replace('\\n', '\n') if config.FIREBASE_PRIVATE_KEY else "",
                "client_email": config.FIREBASE_CLIENT_EMAIL,
                "client_id": "",  # Not required for authentication
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{config.FIREBASE_CLIENT_EMAIL}",
                "universe_domain": "googleapis.com"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully")
        
        # Get Firestore client
        self._db = firestore.client()
    
    @property
    def db(self) -> Client:
        """Get Firestore database client."""
        return self._db


def get_db() -> Client:
    """
    Dependency provider for Firestore database.
    
    Returns:
        Firestore client instance
    """
    firebase_service = FirebaseService()
    return firebase_service.db
