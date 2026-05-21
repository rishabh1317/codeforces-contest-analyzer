from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/{handle}", response_model=schemas.UserResponse)
def get_user(handle: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.handle == handle).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
