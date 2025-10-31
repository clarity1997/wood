from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth, products, upload, search, chat, cart
from .config import settings
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Furniture Shopping API",
    description="Backend API for furniture shopping app with merchant and user features",
    version="1.0.0"
)

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Android app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(cart.router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Furniture Shopping API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
