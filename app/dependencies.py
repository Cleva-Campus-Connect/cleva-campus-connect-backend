import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.security import decode_access_token
from app.database import supabase

from app.config import settings

bearer = HTTPBearer()
jwks_client = jwt.PyJWKClient(settings.supabase_jwks_url)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer))-> dict:
    token = credentials.credentials
    try:
        key = jwks_client.get_signing_key_from_jwt(token).key
        payload = jwt.decode(token, key, algorithms=["ES256", "RS256"], audience = "authenticated",)
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token" )

    result = (
        supabase.table("users")
        .select("*").eq("auth_id", payload["sub"])
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=403, detail="No account found")

    user = result.data[0]
    if user["status"] != "active":
        raise HTTPException(status_code=403, detail="User account is disabled")
    return user

def require_role(*allowed_role: str):
    def checker(user:dict = Depends(get_current_user))->dict:
        if user["role"] not in allowed_role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")
        return user

    return checker