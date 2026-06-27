from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TypePermis
from app.schemas import MetadataResponse

router = APIRouter(prefix="/api/mobile", tags=["metadata"])


@router.get("/metadata/", response_model=MetadataResponse)
async def get_metadata(db: Session = Depends(get_db)):
    types_permis = db.query(TypePermis).all()

    bureaux = [
        "GUPEC Bunia",
        "GUPEC Kinshasa",
        "GUPEC Kisangani",
        "GUPEC Lubumbashi",
        "GUPEC Bukavu"
    ]

    return MetadataResponse(
        types_permis=[{"id": t.id, "code": t.code, "nom": t.nom, "description": t.description} for t in types_permis],
        bureaux=bureaux
    )