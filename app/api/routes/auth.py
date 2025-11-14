from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserOut
from app.schemas.auth import RegisterSchema, LoginSchema, TokenSchema
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, get_current_user
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import blacklist_token

security_scheme = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password), role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login",response_model=TokenSchema)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    return TokenSchema(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id))
    )

@router.post("/refresh", response_model=TokenSchema)
def refresh(refresh_token:str, db: Session = Depends(get_db)):
    user_id = decode_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    # Optionally: check if user still exists / active
    user = db.query(User).get(int(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or not found")
    return TokenSchema(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id))
    )

@router.get("/me", response_model=UserOut)
def me(current = Depends(get_current_user)):
    return current

@router.post("/logout")
def logout(creds: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = creds.credentials
    # Blacklist for remaining lifetime of token
    expires_in = 900  # e.g. 15 minutes if that's your access token expiry
    blacklist_token(token, expires_in)
    return {"message": "Successfully logged out"}
