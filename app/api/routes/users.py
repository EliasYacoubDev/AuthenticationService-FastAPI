from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import get_current_user
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def get_me(user = Depends(get_current_user)):
    return user

@router.get("/admin")
def admin_only(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return {"message": f"Welcome, admin {user.email.split("@")[0]}!"}
