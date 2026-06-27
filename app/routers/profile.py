from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserProfile, UpdateProfileRequest
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/mobile", tags=["profile"])


@router.get("/profile/", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        postnom=current_user.postnom,
        genre=current_user.genre,
        phone=current_user.phone,
        commune=current_user.commune,
        adresse=current_user.adresse,
        type_personne=current_user.type_personne,
        raison_sociale=current_user.raison_sociale,
        sigle=current_user.sigle,
        forme_juridique=current_user.forme_juridique,
        nif=current_user.nif,
        rccm=current_user.rccm,
        id_nationale=current_user.id_nationale,
        secteur_activite=current_user.secteur_activite,
        representant=current_user.representant,
        fonction_representant=current_user.fonction_representant
    )


@router.put("/profile/", response_model=UserProfile)
async def update_profile(
        request: UpdateProfileRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    for field, value in request.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return await get_profile(current_user)