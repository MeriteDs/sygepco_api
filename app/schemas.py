from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ========== Auth ==========
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: int
    email: str
    username: str
    role: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


# ========== User/Profile ==========
class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    postnom: Optional[str] = None
    genre: Optional[str] = None
    phone: Optional[str] = None
    commune: Optional[str] = None
    adresse: Optional[str] = None
    type_personne: Optional[str] = 'Physique'
    raison_sociale: Optional[str] = None
    sigle: Optional[str] = None
    forme_juridique: Optional[str] = None
    nif: Optional[str] = None
    rccm: Optional[str] = None
    id_nationale: Optional[str] = None
    secteur_activite: Optional[str] = None
    representant: Optional[str] = None
    fonction_representant: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    postnom: Optional[str] = None
    genre: Optional[str] = None
    phone: Optional[str] = None
    commune: Optional[str] = None
    adresse: Optional[str] = None
    type_personne: Optional[str] = None
    raison_sociale: Optional[str] = None
    sigle: Optional[str] = None
    forme_juridique: Optional[str] = None
    nif: Optional[str] = None
    rccm: Optional[str] = None
    id_nationale: Optional[str] = None
    secteur_activite: Optional[str] = None
    representant: Optional[str] = None
    fonction_representant: Optional[str] = None


# ========== Types de permis ==========
class TypePermisResponse(BaseModel):
    id: int
    code: str
    nom: str
    description: Optional[str] = None


# ========== Dossiers ==========
class DossierCreateRequest(BaseModel):
    types_permis_ids: List[int] = Field(default_factory=list)


class DossierUpdateRequest(BaseModel):
    # Localisation
    nature_demandeur: Optional[str] = None
    bureau_gupec: Optional[str] = None
    ville: Optional[str] = None
    commune: Optional[str] = None
    quartier: Optional[str] = None
    avenue: Optional[str] = None
    rue: Optional[str] = None
    num_parcelle: Optional[str] = None

    # Détails techniques
    num_susr: Optional[str] = None
    num_plan_cadastral: Optional[str] = None
    type_construction: Optional[str] = None
    usage: Optional[str] = None
    niveaux: Optional[int] = None
    duree_travaux: Optional[str] = None
    duree_unite: Optional[str] = None
    auteur_projet: Optional[str] = None
    num_immatriculation: Optional[str] = None
    description: Optional[str] = None


class DossierResponse(BaseModel):
    id: int
    numero_dossier: Optional[str] = None
    statut: str
    statut_display: str
    date_creation: datetime
    commune: Optional[str] = None
    territoire: Optional[str] = None
    types_permis: List[TypePermisResponse] = []
    montant_taxes: float = 0.0
    montant_paye: float = 0.0


class DossierDetailResponse(DossierResponse):
    quartier: Optional[str] = None
    avenue: Optional[str] = None
    rue: Optional[str] = None
    num_parcelle: Optional[str] = None
    bureau_gupec: Optional[str] = None
    nature_demandeur: Optional[str] = None
    num_susr: Optional[str] = None
    num_plan_cadastral: Optional[str] = None
    type_construction: Optional[str] = None
    usage: Optional[str] = None
    niveaux: Optional[int] = None
    duree_travaux: Optional[str] = None
    duree_unite: Optional[str] = None
    auteur_projet: Optional[str] = None
    num_immatriculation: Optional[str] = None
    description: Optional[str] = None


# ========== Documents ==========
class DocumentUploadResponse(BaseModel):
    id: int
    dossier_id: int
    type: str
    nom_fichier: str
    date_upload: datetime


# ========== Metadata ==========
class MetadataResponse(BaseModel):
    types_permis: List[TypePermisResponse]
    bureaux: List[str]


# ========== Pagination ==========
class PaginatedResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[DossierResponse]