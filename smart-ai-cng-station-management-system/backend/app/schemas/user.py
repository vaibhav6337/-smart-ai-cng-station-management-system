from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: str = "MANAGER"
    is_active: bool = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    mobile_number: str = Field(..., min_length=8, max_length=20)
    verification_token: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class OTPRequest(BaseModel):
    mobile_number: str = Field(..., min_length=8, max_length=20)


class OTPVerifyRequest(OTPRequest):
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, max_length=128)
    verification_token: str = Field(..., min_length=1)


class ChangePasswordOTPVerifyRequest(BaseModel):
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PasswordResetRequest(BaseModel):
    mobile_number: str = Field(..., min_length=8, max_length=20)
    verification_token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, max_length=128)
