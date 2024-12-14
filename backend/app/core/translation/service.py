from typing import List, Tuple, Optional
import deepl
import pysrt
from pathlib import Path
import os
from datetime import datetime
from sqlmodel import Session
from app.models import User, TranslationHistory, UserSubscription
from app.core.config import settings

class TranslationError(Exception):
    """Base exception for translation errors"""
    pass

class QuotaExceededError(TranslationError):
    """Raised when user has exceeded their translation quota"""
    pass

class TranslationService:
    def __init__(self, db: Session):
        self.db = db
        self.translator = self._get_translator()

    def _get_translator(self) -> deepl.Translator:
        """Get DeepL translator instance"""
        api_key = settings.DEEPL_API_KEY
        if not api_key:
            raise ValueError("DeepL API key not configured")
        return deepl.Translator(api_key)

    def check_user_quota(self, user: User, char_count: int) -> bool:
        """Check if user has enough quota for translation"""
        if not user.subscription or not user.subscription.is_active:
            raise QuotaExceededError("No active subscription")
        
        if user.subscription.characters_used + char_count > user.subscription.plan.characters_per_month:
            raise QuotaExceededError("Monthly character limit exceeded")
        
        return True

    def update_usage(self, user: User, char_count: int):
        """Update user's character usage"""
        if user.subscription:
            user.subscription.characters_used += char_count
            self.db.add(user.subscription)
            self.db.commit()

    def create_translation_record(self, user: User, filename: str, 
                                source_lang: str, target_lang: str, 
                                char_count: int) -> TranslationHistory:
        """Create a record of translation attempt"""
        record = TranslationHistory(
            user_id=user.id,
            file_name=filename,
            source_language=source_lang,
            target_language=target_lang,
            characters_count=char_count,
            status="in_progress"
        )
        self.db.add(record)
        self.db.commit()
        return record

    def update_translation_status(self, record_id: str, status: str):
        """Update translation record status"""
        record = self.db.get(TranslationHistory, record_id)
        if record:
            record.status = status
            self.db.add(record)
            self.db.commit()

    def is_sentence_start(self, text: str) -> bool:
        """Check if text appears to start a new sentence."""
        if not text:
            return False
        text = text.lstrip()
        return (text[0].isupper() if text else False) and not any(
            text.startswith(char) for char in ['♪', '[', '(', ',', ';', ':', 'and', 'or', 'but']
        )

    def is_sentence_end(self, text: str) -> bool:
        """Check if text appears to end a sentence."""
        if not text:
            return False
        text = text.rstrip()
        if text.endswith('...'):
            return False
        return text.endswith(('.', '!', '?', '"', '"'))

    def should_connect_subtitles(self, current_text: str, next_text: str) -> bool:
        """Determine if two subtitles should be connected based on content"""
        if not current_text or not next_text:
            return False
        
        current_text = current_text.strip()
        next_text = next_text.strip()
        
        if current_text.endswith('...') and next_text[0].islower():
            return True
        
        if current_text.endswith('...') and next_text.startswith('...'):
            remaining_text = next_text[3:].lstrip()
            return remaining_text and remaining_text[0].islower()
        
        connectors = ('and', 'or', 'but', 'because', 'so', 'yet', 'for', 'nor', 'while')
        next_words = next_text.split()
        if next_words and next_words[0].lower() in connectors and next_words[0].islower():
            return True
        
        return False

    def find_connected_subtitles(self, subs: list, start_idx: int) -> tuple[int, str]:
        """Find a group of subtitles that form a complete sentence"""
        if start_idx >= len(subs):
            return start_idx, ""
        
        combined_parts = []
        current_idx = start_idx
        
        if current_idx > 0 and not self.is_sentence_start(subs[start_idx].text) and not self.should_connect_subtitles(subs[current_idx-1].text, subs[current_idx].text):
            return start_idx, ""
        
        while current_idx < len(subs):
            current_text = subs[current_idx].text.strip()
            combined_parts.append(current_text)
            
            if current_idx < len(subs) - 1:
                next_text = subs[current_idx + 1].text
                if self.should_connect_subtitles(current_text, next_text):
                    current_idx += 1
                    continue
            
            if current_idx == len(subs) - 1 or self.is_sentence_end(current_text):
                break
                
            current_idx += 1
            if current_idx < len(subs) and self.is_sentence_start(subs[current_idx].text) and not self.should_connect_subtitles(subs[current_idx-1].text, subs[current_idx].text):
                current_idx -= 1
                break
        
        return current_idx, " ".join(combined_parts)

    def preserve_formatting(self, original_text: str, translated_text: str) -> str:
        """Preserve capitalization and special endings from original text"""
        if not original_text or not translated_text:
            return translated_text
            
        # Preserve capitalization
        if original_text[0].isupper():
            translated_text = translated_text[0].upper() + translated_text[1:]
        
        # Preserve special endings
        if original_text.endswith('...'):
            if not translated_text.endswith('...'):
                translated_text = translated_text.rstrip('.') + '...'
        
        return translated_text

    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate single piece of text."""
        if not text.strip():
            return text
            
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text

    def translate_srt(self, user: User, file_path: str, target_lang: str) -> str:
        """Translate SRT file while preserving formatting and context"""
        try:
            subs = pysrt.open(file_path)
            total_chars = sum(len(sub.text) for sub in subs)
            
            # Check quota before processing
            self.check_user_quota(user, total_chars)
            
            # Process subtitles in batches of connected sentences
            idx = 0
            while idx < len(subs):
                end_idx, combined_text = self.find_connected_subtitles(subs, idx)
                if combined_text:
                    # Translate the combined text
                    translated_text = self.translator.translate_text(
                        combined_text,
                        target_lang=target_lang
                    ).text
                    
                    # Split translation back to subtitles
                    parts = translated_text.split()
                    words_per_sub = len(combined_text.split()) // (end_idx - idx + 1)
                    
                    for sub_idx in range(idx, end_idx + 1):
                        start = (sub_idx - idx) * words_per_sub
                        end = start + words_per_sub if sub_idx < end_idx else None
                        sub_text = " ".join(parts[start:end])
                        subs[sub_idx].text = self.preserve_formatting(
                            subs[sub_idx].text,
                            sub_text
                        )
                
                idx = end_idx + 1
            
            # Save translated file
            output_path = Path(file_path).with_suffix('.translated.srt')
            subs.save(str(output_path), encoding='utf-8')
            
            # Update usage statistics
            self.update_usage(user, total_chars)
            
            # Create translation record
            self.create_translation_record(
                user=user,
                filename=Path(file_path).name,
                source_lang='auto',
                target_lang=target_lang,
                char_count=total_chars
            )
            
            return str(output_path)
            
        except Exception as e:
            raise TranslationError(f"Translation failed: {str(e)}")
