from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.auth_dependency import get_current_user
from app.core.security import decode_access_token
from app.database.session import get_db
from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.user import (
    ChangePasswordOTPVerifyRequest,
    ChangePasswordRequest,
    OTPRequest,
    OTPVerifyRequest,
    PasswordResetRequest,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.otp_service import (
    normalize_mobile_number,
    request_otp,
    verify_otp,
)
from app.services.user_service import (
    change_password,
    create_user,
    login_user,
    reset_password,
)
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
# =========================================================
# REGISTRATION OTP
# =========================================================
@router.post("/registration/request-otp")
def request_registration_otp(
    otp_data: OTPRequest,
    db: Session = Depends(get_db),
):
    mobile_number = normalize_mobile_number(otp_data.mobile_number)
    # Do not allow a mobile number already linked to a user.
    existing_user = (
        db.query(User.id)
        .filter(User.mobile_number == mobile_number)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail=(
                "This mobile number is already "
                "associated with an account."
            ),
        )
    return request_otp(db, mobile_number, "registration")
# =========================================================
# FORGOT PASSWORD — REQUEST OTP
# =========================================================
@router.post("/forgot-password/request-otp")
def request_forgot_password_otp(
    otp_data: OTPRequest,
    db: Session = Depends(get_db),
):
    mobile_number = normalize_mobile_number(otp_data.mobile_number)
    # Only allow recovery for active accounts whose
    # mobile numbers have already been verified.
    user = (
        db.query(User)
        .filter(
            User.mobile_number == mobile_number,
            User.is_mobile_verified.is_(True),
            User.is_active.is_(True),
        )
        .first()
    )
    # Use the same response for unknown and unverified numbers to
    # reduce account enumeration.
    generic_response = {
        "success": True,
        "message": (
            "If an active account with this verified "
            "mobile number exists, an OTP has been sent."
        ),
    }
    if user is None:
        return generic_response
    # Provider/configuration/rate-limit failures are handled by OTP service.
    request_otp(db, mobile_number, "forgot_password")
    return generic_response
# =========================================================
# FORGOT PASSWORD — VERIFY OTP
# =========================================================
@router.post("/forgot-password/verify-otp")
def verify_forgot_password_otp(
    otp_data: OTPVerifyRequest,
    db: Session = Depends(get_db),
):
    return verify_otp(
        db,
        otp_data.mobile_number,
        "forgot_password",
        otp_data.otp,
    )
# =========================================================
# RESET PASSWORD
# =========================================================
@router.post("/reset-password")
def reset_user_password(
    reset_data: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    return reset_password(
        db,
        reset_data.mobile_number,
        reset_data.verification_token,
        reset_data.new_password,
    )
@router.post("/registration/verify-otp")
def verify_registration_otp(
    otp_data: OTPVerifyRequest,
    db: Session = Depends(get_db),
):
    return verify_otp(
        db,
        otp_data.mobile_number,
        "registration",
        otp_data.otp,
    )
@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user)
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(db, user.username, user.password)
# =========================================================
# CHANGE PASSWORD — REQUEST OTP
# =========================================================
@router.post("/change-password/request-otp")
def request_change_password_otp(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (
        not current_user.mobile_number
        or not current_user.is_mobile_verified
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "A verified mobile number is required "
                "before changing the password with OTP."
            ),
        )
    return request_otp(
        db,
        current_user.mobile_number,
        "change_password",
    )
# =========================================================
# CHANGE PASSWORD — VERIFY OTP
# =========================================================
@router.post("/change-password/verify-otp")
def verify_change_password_otp(
    otp_data: ChangePasswordOTPVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (
        not current_user.mobile_number
        or not current_user.is_mobile_verified
    ):
        raise HTTPException(
            status_code=400,
            detail="A verified mobile number is required.",
        )
    return verify_otp(
        db,
        current_user.mobile_number,
        "change_password",
        otp_data.otp,
    )
@router.post("/change-password")
def change_user_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_password(
        db,
        current_user.id,
        password_data.current_password,
        password_data.new_password,
        password_data.verification_token,
    )
# =========================================================
# LOGOUT — REVOKE THE CURRENT LOGIN SESSION
# =========================================================
@router.post("/logout")
def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Decode the token after the authentication dependency has validated
    # the user's active session.
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token.",
        )
    session_id = payload.get("session_id")
    if not isinstance(session_id, str):
        raise HTTPException(
            status_code=401,
            detail="Invalid login session.",
        )
    # Find and lock this user's active session.
    user_session = (
        db.query(UserSession)
        .filter(
            UserSession.session_id == session_id,
            UserSession.user_id == current_user.id,
            UserSession.revoked_at.is_(None),
        )
        .with_for_update()
        .first()
    )
    if user_session is None:
        raise HTTPException(
            status_code=401,
            detail="Login session is already invalid.",
        )
    # Revoke the session on the server.
    user_session.revoked_at = datetime.utcnow()
    db.commit()
    return {
        "success": True,
        "message": "Logged out successfully.",
    }
