import hashlib
import os
import datetime
import jwt
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from db.Mongodb import get_users_collection

router = APIRouter(prefix="/auth", tags=["Auth"])

JWT_SECRET = os.getenv("JWT_SECRET", "hireprep_ai_super_secret_jwt_key_2026")
JWT_ALGORITHM = "HS256"


# ── Password Hashing Helpers ──
def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}:{pwd_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, expected_hash = stored_hash.split(':')
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return hmac_compare(pwd_hash, expected_hash)
    except Exception:
        return False


def hmac_compare(a: str, b: str) -> bool:
    import hmac
    return hmac.compare_digest(a, b)


def create_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please sign in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Please sign in again.")


# ── Request / Response Models ──
class SignUpRequest(BaseModel):
    full_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ── Routes ──
@router.post("/signup")
async def signup(req: SignUpRequest):
    users_col = get_users_collection()
    
    # Check if user already exists
    existing = await users_col.find_one({"email": req.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    user_doc = {
        "full_name": req.full_name.strip(),
        "email": req.email.lower().strip(),
        "password": hash_password(req.password),
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    result = await users_col.insert_one(user_doc)
    user_id = str(result.inserted_id)
    token = create_token(user_id, req.email.lower())
    
    return {
        "message": "User registered successfully",
        "access_token": token,
        "user": {
            "id": user_id,
            "full_name": user_doc["full_name"],
            "email": user_doc["email"]
        }
    }


@router.post("/login")
async def login(req: LoginRequest):
    users_col = get_users_collection()
    user = await users_col.find_one({"email": req.email.lower()})
    
    if not user or not verify_password(req.password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    user_id = str(user["_id"])
    token = create_token(user_id, user["email"])
    
    return {
        "message": "Signed in successfully",
        "access_token": token,
        "user": {
            "id": user_id,
            "full_name": user.get("full_name", ""),
            "email": user["email"]
        }
    }


@router.get("/me")
async def get_me(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    
    users_col = get_users_collection()
    from bson import ObjectId
    user = await users_col.find_one({"_id": ObjectId(payload["sub"])})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return {
        "user": {
            "id": str(user["_id"]),
            "full_name": user.get("full_name", ""),
            "email": user.get("email", "")
        }
    }
