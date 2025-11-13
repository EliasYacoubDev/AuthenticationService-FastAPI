from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    role: str = "user"
    is_active: bool = True

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True