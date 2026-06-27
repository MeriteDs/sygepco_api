from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Table d'association
dossier_types_permis = Table(
    'dossier_types_permis',
    Base.metadata,
    Column('dossier_id', Integer, ForeignKey('dossiers.id')),
    Column('type_permis_id', Integer, ForeignKey('types_permis.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(50), default='assujetti')
    first_name = Column(String(100))
    last_name = Column(String(100))
    postnom = Column(String(100))
    genre = Column(String(20))
    phone = Column(String(20))
    commune = Column(String(100))
    adresse = Column(String(255))
    type_personne = Column(String(50), default='Physique')

    # Personne morale
    raison_sociale = Column(String(255))
    sigle = Column(String(50))
    forme_juridique = Column(String(100))
    nif = Column(String(50))
    rccm = Column(String(50))
    id_nationale = Column(String(50))
    secteur_activite = Column(String(255))
    representant = Column(String(255))
    fonction_representant = Column(String(255))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    dossiers = relationship("Dossier", back_populates="user")


class TypePermis(Base):
    __tablename__ = "types_permis"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True)
    nom = Column(String(100))
    description = Column(Text)

    dossiers = relationship("Dossier", secondary=dossier_types_permis, back_populates="types_permis")


class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    numero_dossier = Column(String(100), unique=True, nullable=True)
    statut = Column(String(50), default='brouillon')
    statut_display = Column(String(100), default='Brouillon')
    date_creation = Column(DateTime, server_default=func.now())
    date_soumission = Column(DateTime, nullable=True)

    # Localisation
    commune = Column(String(100))
    territoire = Column(String(100))
    quartier = Column(String(100))
    avenue = Column(String(100))
    rue = Column(String(100))
    num_parcelle = Column(String(50))
    bureau_gupec = Column(String(255))
    nature_demandeur = Column(String(50), default='Propriétaire')

    # Détails techniques
    num_susr = Column(String(50))
    num_plan_cadastral = Column(String(50))
    type_construction = Column(String(100))
    usage = Column(String(100))
    niveaux = Column(Integer, default=0)
    duree_travaux = Column(String(50))
    duree_unite = Column(String(20), default='Mois')
    auteur_projet = Column(String(255))
    num_immatriculation = Column(String(50))
    description = Column(Text)

    # Finances
    montant_taxes = Column(Float, default=0.0)
    montant_paye = Column(Float, default=0.0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", back_populates="dossiers")
    types_permis = relationship("TypePermis", secondary=dossier_types_permis, back_populates="dossiers")
    documents = relationship("Document", back_populates="dossier")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"))
    type = Column(String(50))
    nom_fichier = Column(String(255))
    chemin_fichier = Column(String(255))
    date_upload = Column(DateTime, server_default=func.now())

    dossier = relationship("Dossier", back_populates="documents")