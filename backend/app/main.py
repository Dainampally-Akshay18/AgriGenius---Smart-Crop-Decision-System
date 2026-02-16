"""
FastAPI application entry point.
"""
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from app.utils.logger import logger
from app.routers import auth, predict, weather

# Add project root to Python path to allow ml module imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Validate configuration
config.validate()

# Create FastAPI app
app = FastAPI(
    title="AgriGenius API",
    description="Smart Crop Decision System - Backend API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(predict.router, prefix="/api")
app.include_router(weather.router, prefix="/api")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {
        "status": "healthy",
        "service": "agri-genius-api",
        "environment": config.APP_ENV
    }


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("AgriGenius API starting up...")
    logger.info(f"Environment: {config.APP_ENV}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("AgriGenius API shutting down...")