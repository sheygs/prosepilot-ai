from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class ContentItem:
    """Model representing generated content"""
    timestamp: str
    prompt: str
    content_type: str
    tone: str
    response: str

    @classmethod
    def create_from_generation(cls, prompt, content_type, tone, response):
        """Create a new content item from generation results"""
        return cls(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            prompt=prompt,
            content_type=content_type,
            tone=tone,
            response=response
        )
