"""AI content generation service."""
import requests
from typing import Optional
from config import Config

class AIService:
    """AI content generation service supporting multiple providers."""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self._setup_client()
    
    def _setup_client(self):
        """Setup AI client based on provider."""
        if self.provider == "openai":
            try:
                import openai
                if not Config.OPENAI_API_KEY:
                    raise ValueError("OpenAI API key not found")
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            except ImportError:
                raise ImportError("openai package not installed")
                
        elif self.provider == "anthropic":
            try:
                import anthropic
                if not Config.ANTHROPIC_API_KEY:
                    raise ValueError("Anthropic API key not found")
                self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            except ImportError:
                raise ImportError("anthropic package not installed")
                
        elif self.provider == "ollama":
            self.ollama_url = Config.OLLAMA_URL
            if not self.ollama_url:
                raise ValueError("Ollama URL not configured")
    
    def generate_content(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate content using the configured AI provider."""
        if self.provider == "openai":
            return self._generate_openai(prompt, max_tokens)
        elif self.provider == "anthropic":
            return self._generate_anthropic(prompt, max_tokens)
        elif self.provider == "ollama":
            return self._generate_ollama(prompt, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _generate_openai(self, prompt: str, max_tokens: int) -> str:
        """Generate content using OpenAI."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    
    def _generate_anthropic(self, prompt: str, max_tokens: int) -> str:
        """Generate content using Anthropic."""
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    
    def _generate_ollama(self, prompt: str, max_tokens: int) -> str:
        """Generate content using Ollama."""
        data = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens}
        }
        
        response = requests.post(f"{self.ollama_url}/api/generate", json=data)
        response.raise_for_status()
        return response.json()["response"].strip()
    
    def generate_title(self, topic: str) -> str:
        """Generate a blog post title."""
        prompt = f"Generate a compelling blog post title about: {topic}"
        return self.generate_content(prompt, max_tokens=50)
    
    def generate_excerpt(self, content: str) -> str:
        """Generate an excerpt from content."""
        prompt = f"Create a brief excerpt (2-3 sentences) from this content:\n\n{content[:500]}"
        return self.generate_content(prompt, max_tokens=100)
    
    def generate_article(self, topic: str, tone: str = "professional") -> str:
        """Generate a full article."""
        prompt = f"Write a {tone} blog post about: {topic}. Include an introduction, main points, and conclusion."
        return self.generate_content(prompt, max_tokens=1500)