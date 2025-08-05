"""Base command interface."""
from abc import ABC, abstractmethod
from typing import Any

class BaseCommand(ABC):
    """Abstract base command class."""
    
    @abstractmethod
    def execute(self) -> Any:
        """Execute the command."""
        pass
```

## 9. commands/post_commands.py
```python
"""Post-related commands."""
from typing import List, Optional
from .base_command import BaseCommand
from services.wp_service import WordPressService
from services.ai_service import AIService

class CreatePostCommand(BaseCommand):
    """Command to create a new post."""
    
    def __init__(self, topic: str, ai_provider: Optional[str] = None,
                 status: str = "draft", tone: str = "professional"):
        self.topic = topic
        self.ai_provider = ai_provider
        self.status = status
        self.tone = tone
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute post creation."""
        if self.ai_provider:
            ai_service = AIService(self.ai_provider)
            title = ai_service.generate_title(self.topic)
            content = ai_service.generate_article(self.topic, self.tone)
            excerpt = ai_service.generate_excerpt(content)
        else:
            title = self.topic
            content = f"Content for: {self.topic}"
            excerpt = ""
            
        return self.wp_service.create_post(
            title=title,
            content=content,
            excerpt=excerpt,
            status=self.status
        )

class EditPostCommand(BaseCommand):
    """Command to edit an existing post."""
    
    def __init__(self, post_id: int, **kwargs):
        self.post_id = post_id
        self.updates = kwargs
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute post edit."""
        return self.wp_service.update_post(self.post_id, **self.updates)

class PublishPostCommand(BaseCommand):
    """Command to publish a post."""
    
    def __init__(self, post_id: int):
        self.post_id = post_id
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute post publishing."""
        return self.wp_service.update_post(self.post_id, status="publish")

class DeletePostCommand(BaseCommand):
    """Command to delete a post."""
    
    def __init__(self, post_id: int):
        self.post_id = post_id
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute post deletion."""
        return self.wp_service.delete_post(self.post_id)

class SchedulePostCommand(BaseCommand):
    """Command to schedule a post."""
    
    def __init__(self, post_id: int, date: str):
        self.post_id = post_id
        self.date = date
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute post scheduling."""
        return self.wp_service.update_post(
            self.post_id, 
            status="future", 
            date=self.date
        )