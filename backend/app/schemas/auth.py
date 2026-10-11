from pydantic import BaseModel, EmailStr, Field

# ==========================================
# REGISTER
# ==========================================

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    # Registration requires at least 8 characters. Login intentionally has no
    # minimum-length validation so existing accounts with shorter passwords
    # can continue to authenticate.
    password: str = Field(min_length=8, max_length=128)

# ==========================================
# LOGIN
# ==========================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ==========================================
# TOKEN RESPONSE
# ==========================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
