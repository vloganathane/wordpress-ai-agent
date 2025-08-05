"""Media-related commands."""
from .base_command import BaseCommand
from services.wp_service import WordPressService

class UploadMediaCommand(BaseCommand):
    """Command to upload media files."""
    
    def __init__(self, file_path: str, title: str = "", description: str = ""):
        self.file_path = file_path
        self.title = title
        self.description = description
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute media upload."""
        return self.wp_service.upload_media(
            self.file_path,
            self.title,
            self.description
        )
```

## 11. commands/site_commands.py
```python
"""Site management commands."""
from .base_command import BaseCommand
from services.wp_service import WordPressService

class GetCategoriesCommand(BaseCommand):
    """Command to get site categories."""
    
    def __init__(self):
        self.wp_service = WordPressService()
        
    def execute(self) -> list:
        """Execute get categories."""
        return self.wp_service.get_categories()

class CreateCategoryCommand(BaseCommand):
    """Command to create a category."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.wp_service = WordPressService()
        
    def execute(self) -> dict:
        """Execute category creation."""
        return self.wp_service.create_category(self.name, self.description)

class GetUsersCommand(BaseCommand):
    """Command to get site users."""
    
    def __init__(self):
        self.wp_service = WordPressService()
        
    def execute(self) -> list:
        """Execute get users."""
        return self.wp_service.get_users()