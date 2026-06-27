from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, LoginResponse, RegisterRequest
from app.auth import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/api/mobile", tags=["auth"])


@router.post("/login/", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    token = create_access_token(data={"sub": str(user.id)})

    return LoginResponse(
        token=token,
        user_id=user.id,
        email=user.email,
        username=user.username,
        role=user.role
    )


@router.post("/register/", response_model=LoginResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )

    # Vérifier si le username existe déjà
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom d'utilisateur est déjà utilisé"
        )

    hashed_password = get_password_hash(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        password=hashed_password,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        role="assujetti"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})

    return LoginResponse(
        token=token,
        user_id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        role=new_user.role
    )