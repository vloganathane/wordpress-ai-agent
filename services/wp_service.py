"""WordPress REST API service."""
import requests
from typing import Dict, List, Optional, Any
import mimetypes
from config import Config

class WordPressService:
    """WordPress REST API client."""
    
    def __init__(self):
        if not Config.validate_wp_config():
            raise ValueError("WordPress configuration missing. Check .env file.")
        
        self.base_url = Config.WP_URL.rstrip('/') + '/wp-json/wp/v2'
        self.auth = (Config.WP_USERNAME, Config.WP_PASSWORD)
        self.session = requests.Session()
        self.session.auth = self.auth
    
    def create_post(self, title: str, content: str, status: str = "draft",
                   excerpt: str = "", categories: List[int] = None,
                   tags: List[int] = None) -> Dict[str, Any]:
        """Create a new post."""
        data = {
            "title": title,
            "content": content,
            "status": status,
            "excerpt": excerpt
        }
        
        if categories:
            data["categories"] = categories
        if tags:
            data["tags"] = tags
            
        response = self.session.post(f"{self.base_url}/posts", json=data)
        response.raise_for_status()
        return response.json()
    
    def update_post(self, post_id: int, **kwargs) -> Dict[str, Any]:
        """Update an existing post."""
        response = self.session.post(f"{self.base_url}/posts/{post_id}", json=kwargs)
        response.raise_for_status()
        return response.json()
    
    def delete_post(self, post_id: int) -> Dict[str, Any]:
        """Delete a post."""
        response = self.session.delete(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()
    
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post."""
        response = self.session.get(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()
    
    def upload_media(self, file_path: str, title: str = "", 
                    description: str = "") -> Dict[str, Any]:
        """Upload media file."""
        mime_type, _ = mimetypes.guess_type(file_path)
        
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_path, f, mime_type or 'application/octet-stream')
            }
            
            data = {}
            if title:
                data['title'] = title
            if description:
                data['description'] = description
                
            response = self.session.post(
                f"{self.base_url}/media",
                files=files,
                data=data
            )
            
        response.raise_for_status()
        return response.json()
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories."""
        response = self.session.get(f"{self.base_url}/categories")
        response.raise_for_status()
        return response.json()
    
    def create_category(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new category."""
        data = {"name": name, "description": description}
        response = self.session.post(f"{self.base_url}/categories", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get site users."""
        response = self.session.get(f"{self.base_url}/users")
        response.raise_for_status()
        return response.json()