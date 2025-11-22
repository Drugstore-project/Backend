"""
Endpoints for user management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud.user import create_user, list_users, get_user, update_user, delete_user
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user (admin only usually, but open for now).
    """
    try:
        return create_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserOut)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """
    Returns the current authenticated user.
    """
    return current_user

@router.get("/", response_model=list[UserOut])
def list_users_endpoint(
    db: Session = Depends(get_db),
):
    """
    Lists all users.
    """
    return list_users(db)

@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a specific user by ID.
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    """
    Updates a user's information.
    """
    user = update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user.
    """
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
