# backend/app/core/auth.py
import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwk, jwt
import json
import time
from app.config import get_settings

settings = get_settings()
security = HTTPBearer()

class CognitoAuth:
    def __init__(self):
        self.user_pool_id = settings.cognito_user_pool_id
        self.app_client_id = settings.cognito_app_client_id
        self.region = settings.aws_region
        self.jwks_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        self.jwks = None
        self._fetch_jwks()
    
    def _fetch_jwks(self):
        """Fetch JSON Web Key Set from Cognito"""
        try:
            response = requests.get(self.jwks_url)
            response.raise_for_status()
            self.jwks = response.json()
            print(f"✅ Successfully fetched JWKS from Cognito")
        except Exception as e:
            print(f"❌ Failed to fetch JWKS: {e}")
            self.jwks = None
    
    def _get_signing_key(self, kid: str) -> Optional[Dict]:
        """Get signing key from JWKS by key ID"""
        if not self.jwks:
            self._fetch_jwks()
        if not self.jwks:
            return None
        
        for key in self.jwks.get("keys", []):
            if key.get("kid") == kid:
                return key
        return None
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token from Cognito and extract user information"""
        try:
            # Get token header to find key ID
            headers = jwt.get_unverified_header(token)
            kid = headers.get("kid")
            
            if not kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Token missing key ID"
                )
            
            # Get signing key
            signing_key = self._get_signing_key(kid)
            if not signing_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Unable to find signing key"
                )
            
            # Construct public key
            public_key = jwk.construct(signing_key)
            
            # Verify and decode token
            payload = jwt.decode(
                token, 
                public_key.to_pem(), 
                algorithms=["RS256"],
                audience=self.app_client_id,
                issuer=f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}"
            )
            
            # Check token expiration
            if payload.get("exp", 0) < time.time():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Token expired"
                )
            
            return payload
            
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Invalid token: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Token validation failed: {str(e)}"
            )

# Global instance
cognito_auth = CognitoAuth()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    FastAPI dependency to get current authenticated user from JWT token
    Returns user information extracted from Cognito token
    """
    token = credentials.credentials
    payload = cognito_auth.verify_token(token)
    
    return {
        "cognito_sub": payload.get("sub"),
        "email": payload.get("email"),
        "username": payload.get("username"),
        "email_verified": payload.get("email_verified", False),
        "token_payload": payload
    }