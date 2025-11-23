"""
Authentication endpoints for user registration and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import TokenOut
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    """
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
    """
    Authenticates a user and returns an access token.
    """
    print(f"LOGIN ATTEMPT: {form.username}")
    user = get_user_by_email(db, form.username)
    
    if not user:
        print(f"LOGIN FAILED: User {form.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    if not verify_password(form.password, user.password_hash):
        print(f"LOGIN FAILED: Password mismatch for {form.username}")
        # Debug: print hash comparison (be careful in prod logs, but useful for debugging now)
        # print(f"Stored hash: {user.password_hash}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    print(f"LOGIN SUCCESS: {form.username}")
    role_data = {"id": user.role.id, "name": user.role.name} if user.role else None
    token = create_access_token(subject=user.email, extra={"role": role_data})
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    """
    Returns the current authenticated user.
    """
    return current
