from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings
from app.core import security
from app.api.deps import SessionDep
from app import crud
from datetime import timedelta

router = APIRouter(tags=["oauth"])

# Initialize OAuth instance
oauth = OAuth()

# Configure OAuth providers
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@router.get("/login/{provider}")
async def oauth_login(provider: str, request: Request):
    """Redirect to OAuth provider login page"""
    if provider not in ['github']:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    
    # Store redirect URL in session for after login
    redirect_uri = str(request.url_for(f'oauth_callback'))
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)

@router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    request: Request,
    session: SessionDep,
    error: Optional[str] = None
):
    """Handle OAuth callback"""
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    if provider not in ['github']:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")

    # Get OAuth token
    token = await oauth.create_client(provider).authorize_access_token(request)
    
    if provider == 'github':
        # Get user info from GitHub
        resp = await oauth.github.get('user', token=token)
        profile = resp.json()
        emails_resp = await oauth.github.get('user/emails', token=token)
        emails = emails_resp.json()
        primary_email = next(email['email'] for email in emails if email['primary'])
        
        # Get or create user
        user = crud.get_user_by_email(session, email=primary_email)
        if not user:
            user = crud.create_user(
                session,
                email=primary_email,
                password=None,  # OAuth users don't have a password
                full_name=profile.get('name'),
                is_active=True,
                github_id=str(profile['id'])
            )
        
        # Generate JWT token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        frontend_url = f"{settings.FRONTEND_URL}/oauth-callback?token={access_token}"
        return RedirectResponse(url=frontend_url)
