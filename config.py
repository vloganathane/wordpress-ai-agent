"""Configuration management for WordPress AI Agent."""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # WordPress settings
    WP_URL: str = os.getenv("WP_URL", "")
    WP_USERNAME: str = os.getenv("WP_USERNAME", "")
    WP_PASSWORD: str = os.getenv("WP_PASSWORD", "")
    
    # AI service settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    
    @classmethod
    def validate_wp_config(cls) -> bool:
        """Validate WordPress configuration."""
        return bool(cls.WP_URL and cls.WP_USERNAME and cls.WP_PASSWORD)
    
    @classmethod
    def get_ai_config(cls, provider: str) -> Optional[str]:
        """Get AI provider configuration."""
        if provider == "openai":
            return cls.OPENAI_API_KEY
        elif provider == "anthropic":
            return cls.ANTHROPIC_API_KEY
        elif provider == "ollama":
            return cls.OLLAMA_URL
        return None