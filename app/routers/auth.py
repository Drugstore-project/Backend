from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import LoginInput, TokenOut
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Suporta tanto JSON quanto form-url-encoded estilo OAuth2 (Swagger usa form)
@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),  # usa campos: username, password
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(subject=user.email, extra={"role": user.role})
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current = Depends(get_current_user)):
    return current
