from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, profile, dossiers, metadata
from app.database import Base, engine  # ✅ AJOUTER CET IMPORT

# Créer les tables automatiquement au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SYGEPCO API",
    description="API pour le Système de Gestion des Permis de Construire",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dossiers.router)
app.include_router(metadata.router)

@app.get("/")
async def root():
    return {
        "message": "SYGEPCO API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "auth": "/api/mobile/login/, /api/mobile/register/",
            "profile": "/api/mobile/profile/",
            "dossiers": "/api/mobile/dossiers/",
            "metadata": "/api/mobile/metadata/"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage de SYGEPCO API...")
    print("📍 http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )