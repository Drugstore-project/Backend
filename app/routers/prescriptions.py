from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.prescription import Prescription
from app.models.order import OrderItem
from app.schemas.prescription import PrescriptionResponse
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=PrescriptionResponse)
def upload_prescription(
    order_item_id: int = Form(...),
    doctor_name: str = Form(...),
    crm: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate CRM (Simple check)
    if not crm or len(crm) < 4:
        raise HTTPException(status_code=400, detail="Invalid CRM")

    # Check if order item exists
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")

    # Check if prescription already exists
    if order_item.prescription:
        raise HTTPException(status_code=400, detail="Prescription already exists for this item")

    # Save file
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "txt"
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create prescription record
    db_prescription = Prescription(
        order_item_id=order_item_id,
        doctor_name=doctor_name,
        crm=crm,
        file_path=file_path
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)

    return db_prescription

@router.post("/validate-crm")
def validate_crm(crm: str = Form(...)):
    # Mock validation
    if not crm or len(crm) < 4:
         raise HTTPException(status_code=400, detail="Invalid CRM")
    return {"valid": True, "crm": crm}
