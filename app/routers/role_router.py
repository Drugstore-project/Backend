from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud.role_crud as role_crud
import schemas.role as role_schema

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=role_schema.RoleOut)
def create_role(role: role_schema.RoleCreate, db: Session = Depends(get_db)):
    return role_crud.create_role(db, role)

@router.get("/", response_model=list[role_schema.RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return role_crud.get_roles(db)
