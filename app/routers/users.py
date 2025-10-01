from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, list_users
from app.core.deps import require_roles

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, payload)

@router.get("/", response_model=list[UserOut])
def list_users_endpoint(
    db: Session = Depends(get_db),
    _admin = Depends(require_roles("admin"))  # só admin enxerga lista
):
    return list_users(db)
