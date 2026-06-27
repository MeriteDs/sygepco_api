from app.database import SessionLocal, engine, Base
from app.models import User, TypePermis, Dossier, Document
from app.auth import get_password_hash


def init_database():
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

    db = SessionLocal()

    # Insérer les types de permis
    print("Insertion des types de permis...")
    types_permis = [
        {"code": "CONST", "nom": "Le Permis de Construire", "description": "Pour la construction d'un bâtiment"},
        {"code": "CLOT", "nom": "Clôture", "description": "Pour la construction d'une clôture"},
        {"code": "DEMOLI", "nom": "Le Permis de Démolition", "description": "Pour la démolition d'un bâtiment"},
        {"code": "POURSUI", "nom": "Poursuivre une construction", "description": "Pour poursuivre une construction"},
        {"code": "TRANS", "nom": "Le Permis de Transformer", "description": "Pour transformer un bâtiment"},
    ]

    for type_data in types_permis:
        exists = db.query(TypePermis).filter(TypePermis.code == type_data["code"]).first()
        if not exists:
            new_type = TypePermis(**type_data)
            db.add(new_type)
            print(f"  Ajouté: {type_data['nom']}")

    # Créer un utilisateur de test
    print("Création de l'utilisateur de test...")
    test_user = db.query(User).filter(User.email == "elienobis@gmail.com").first()
    if not test_user:
        user = User(
            username="nobis",
            email="elienobis@gmail.com",
            password=get_password_hash("password123"),
            role="assujetti",
            first_name="Elie",
            last_name="NOBIARBO",
            postnom="NOBIS",
            genre="Masculin",
            phone="+243828888888",
            commune="MBUNYA",
            adresse="Shari, Lumumba"
        )
        db.add(user)
        print("  Utilisateur de test créé: elienobis@gmail.com / password123")

    # Ajouter des dossiers de test
    print("Création des dossiers de test...")
    user = db.query(User).filter(User.email == "elienobis@gmail.com").first()
    if user:
        # Récupérer les types de permis
        type_const = db.query(TypePermis).filter(TypePermis.code == "CONST").first()
        type_clot = db.query(TypePermis).filter(TypePermis.code == "CLOT").first()
        type_demoli = db.query(TypePermis).filter(TypePermis.code == "DEMOLI").first()

        # Dossier 1 - Soumis
        dossier1 = Dossier(
            user_id=user.id,
            numero_dossier="GUPEC/DP/IT/001/MAMB/2026",
            statut="soumis",
            statut_display="Soumis",
            commune="MBUNYA",
            territoire="Bunia",
            types_permis=[type_const] if type_const else []
        )
        db.add(dossier1)

        # Dossier 2 - Brouillon
        dossier2 = Dossier(
            user_id=user.id,
            statut="brouillon",
            statut_display="Brouillon",
            commune="Nyakasanza",
            territoire="Bunia",
            types_permis=[type_const] if type_const else []
        )
        db.add(dossier2)

        # Dossier 3 - En vérification
        dossier3 = Dossier(
            user_id=user.id,
            numero_dossier="GUPEC/DP/IT/006/BIA/2026",
            statut="en_verification",
            statut_display="En vérification",
            commune="Nyakasanza",
            territoire="Bunia",
            types_permis=[type_demoli] if type_demoli else [],
            montant_taxes=323.75,
            montant_paye=323.75
        )
        db.add(dossier3)

        print("  3 dossiers de test créés")

    db.commit()
    db.close()
    print("\n✅ Base de données initialisée avec succès !")
    print("📝 Identifiants de test:")
    print("   Email: elienobis@gmail.com")
    print("   Mot de passe: password123")
    print("   API disponible sur: http://localhost:8000")
    print("   Documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    init_database()