from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os
import shutil
from app.database import get_db
from app.models import User, Dossier, TypePermis, Document, dossier_types_permis
from app.schemas import (
    DossierCreateRequest, DossierUpdateRequest,
    DossierResponse, DossierDetailResponse,
    PaginatedResponse, DocumentUploadResponse
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/mobile", tags=["dossiers"])


@router.get("/dossiers/", response_model=PaginatedResponse)
async def get_dossiers(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 20
):
    dossiers = db.query(Dossier).filter(Dossier.user_id == current_user.id).all()

    results = []
    for dossier in dossiers:
        types_permis = db.query(TypePermis).join(
            dossier_types_permis,
            TypePermis.id == dossier_types_permis.c.type_permis_id
        ).filter(dossier_types_permis.c.dossier_id == dossier.id).all()

        results.append(DossierResponse(
            id=dossier.id,
            numero_dossier=dossier.numero_dossier,
            statut=dossier.statut,
            statut_display=dossier.statut_display,
            date_creation=dossier.date_creation,
            commune=dossier.commune,
            territoire=dossier.territoire,
            types_permis=[{"id": t.id, "code": t.code, "nom": t.nom, "description": t.description} for t in
                          types_permis],
            montant_taxes=float(dossier.montant_taxes),
            montant_paye=float(dossier.montant_paye)
        ))

    return PaginatedResponse(
        count=len(results),
        next=None,
        previous=None,
        results=results
    )


@router.post("/dossiers/", response_model=DossierResponse)
async def create_dossier(
        request: DossierCreateRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    new_dossier = Dossier(
        user_id=current_user.id,
        statut="brouillon",
        statut_display="Brouillon"
    )

    db.add(new_dossier)
    db.commit()
    db.refresh(new_dossier)

    # Ajouter les types de permis
    for type_id in request.types_permis_ids:
        type_permis = db.query(TypePermis).filter(TypePermis.id == type_id).first()
        if type_permis:
            new_dossier.types_permis.append(type_permis)

    db.commit()
    db.refresh(new_dossier)

    return await _dossier_to_response(new_dossier, db)


@router.get("/dossiers/{dossier_id}/", response_model=DossierDetailResponse)
async def get_dossier_detail(
        dossier_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    dossier = db.query(Dossier).filter(
        Dossier.id == dossier_id,
        Dossier.user_id == current_user.id
    ).first()

    if not dossier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier non trouvé"
        )

    types_permis = db.query(TypePermis).join(
        dossier_types_permis,
        TypePermis.id == dossier_types_permis.c.type_permis_id
    ).filter(dossier_types_permis.c.dossier_id == dossier.id).all()

    return DossierDetailResponse(
        id=dossier.id,
        numero_dossier=dossier.numero_dossier,
        statut=dossier.statut,
        statut_display=dossier.statut_display,
        date_creation=dossier.date_creation,
        commune=dossier.commune,
        territoire=dossier.territoire,
        quartier=dossier.quartier,
        avenue=dossier.avenue,
        rue=dossier.rue,
        num_parcelle=dossier.num_parcelle,
        bureau_gupec=dossier.bureau_gupec,
        nature_demandeur=dossier.nature_demandeur,
        num_susr=dossier.num_susr,
        num_plan_cadastral=dossier.num_plan_cadastral,
        type_construction=dossier.type_construction,
        usage=dossier.usage,
        niveaux=dossier.niveaux,
        duree_travaux=dossier.duree_travaux,
        duree_unite=dossier.duree_unite,
        auteur_projet=dossier.auteur_projet,
        num_immatriculation=dossier.num_immatriculation,
        description=dossier.description,
        types_permis=[{"id": t.id, "code": t.code, "nom": t.nom, "description": t.description} for t in types_permis],
        montant_taxes=float(dossier.montant_taxes),
        montant_paye=float(dossier.montant_paye)
    )


@router.patch("/dossiers/{dossier_id}/", response_model=DossierResponse)
async def update_dossier(
        dossier_id: int,
        request: DossierUpdateRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    dossier = db.query(Dossier).filter(
        Dossier.id == dossier_id,
        Dossier.user_id == current_user.id
    ).first()

    if not dossier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier non trouvé"
        )

    # Mise à jour des champs
    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dossier, field, value)

    db.commit()
    db.refresh(dossier)

    return await _dossier_to_response(dossier, db)


@router.post("/dossiers/{dossier_id}/soumettre/")
async def submit_dossier(
        dossier_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    dossier = db.query(Dossier).filter(
        Dossier.id == dossier_id,
        Dossier.user_id == current_user.id
    ).first()

    if not dossier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier non trouvé"
        )

    if dossier.statut != "brouillon":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les dossiers en brouillon peuvent être soumis"
        )

    # Générer un numéro de dossier
    import random
    import string
    code = ''.join(random.choices(string.digits, k=6))
    dossier.numero_dossier = f"GUPEC/DP/IT/{code}/{dossier.commune}/{datetime.now().year}"
    dossier.statut = "soumis"
    dossier.statut_display = "Soumis"
    dossier.date_soumission = datetime.now()

    db.commit()
    db.refresh(dossier)

    return {"message": "Dossier soumis avec succès", "numero_dossier": dossier.numero_dossier}


@router.post("/dossiers/{dossier_id}/upload_document/")
async def upload_document(
        dossier_id: int,
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    dossier = db.query(Dossier).filter(
        Dossier.id == dossier_id,
        Dossier.user_id == current_user.id
    ).first()

    if not dossier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier non trouvé"
        )

    # Créer le dossier d'upload
    upload_dir = f"uploads/dossiers/{dossier_id}"
    os.makedirs(upload_dir, exist_ok=True)

    # Sauvegarder le fichier
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Déterminer le type de document
    document_type = "technique" if "technique" in file.filename.lower() else "administratif"

    new_document = Document(
        dossier_id=dossier_id,
        type=document_type,
        nom_fichier=file.filename,
        chemin_fichier=file_path
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return DocumentUploadResponse(
        id=new_document.id,
        dossier_id=new_document.dossier_id,
        type=new_document.type,
        nom_fichier=new_document.nom_fichier,
        date_upload=new_document.date_upload
    )


async def _dossier_to_response(dossier, db):
    types_permis = db.query(TypePermis).join(
        dossier_types_permis,
        TypePermis.id == dossier_types_permis.c.type_permis_id
    ).filter(dossier_types_permis.c.dossier_id == dossier.id).all()

    return DossierResponse(
        id=dossier.id,
        numero_dossier=dossier.numero_dossier,
        statut=dossier.statut,
        statut_display=dossier.statut_display,
        date_creation=dossier.date_creation,
        commune=dossier.commune,
        territoire=dossier.territoire,
        types_permis=[{"id": t.id, "code": t.code, "nom": t.nom, "description": t.description} for t in types_permis],
        montant_taxes=float(dossier.montant_taxes),
        montant_paye=float(dossier.montant_paye)
    )