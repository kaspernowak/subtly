from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
from app.api import deps
from app.core.translation.service import TranslationService, TranslationError, QuotaExceededError
from app.models import User
import tempfile
import os
from pathlib import Path

router = APIRouter(prefix="/translation", tags=["translation"])

@router.post("/translate/")
async def translate_subtitles(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    file: UploadFile = File(...),
    target_language: str
) -> Any:
    """
    Translate subtitle file to target language.
    """
    if not file.filename or not file.filename.endswith('.srt'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload an SRT file."
        )
    
    try:
        # Create temporary file to store uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.srt') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Initialize translation service
        translation_service = TranslationService(db)
        
        try:
            # Process translation
            output_path = await translation_service.translate_srt(
                user=current_user,
                file_path=temp_file_path,
                target_lang=target_language
            )
            
            # Read translated content
            with open(output_path, 'rb') as f:
                translated_content = f.read()
            
            # Clean up temporary files
            os.unlink(temp_file_path)
            os.unlink(output_path)
            
            # Return translated content
            return {
                "filename": Path(file.filename).stem + f".{target_language.lower()}.srt",
                "content": translated_content
            }
            
        except QuotaExceededError as e:
            raise HTTPException(
                status_code=402,  # Payment Required
                detail=str(e)
            )
        except TranslationError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing translation: {str(e)}"
        )

@router.get("/usage/")
def get_usage_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user's translation usage statistics.
    """
    if not current_user.subscription:
        return {
            "status": "no_subscription",
            "characters_used": 0,
            "characters_limit": 0,
            "subscription_type": None
        }
    
    return {
        "status": "active" if current_user.subscription.is_active else "inactive",
        "characters_used": current_user.subscription.characters_used,
        "characters_limit": current_user.subscription.plan.characters_per_month,
        "subscription_type": current_user.subscription.plan.type
    }

@router.get("/history/")
def get_translation_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Get user's translation history.
    """
    return {
        "translations": current_user.translations[skip:skip + limit],
        "total": len(current_user.translations)
    }
