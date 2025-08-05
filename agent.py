"""WordPress AI Agent CLI."""
import typer
from typing import Optional
from commands.post_commands import (
    CreatePostCommand, EditPostCommand, PublishPostCommand, 
    DeletePostCommand, SchedulePostCommand
)
from commands.media_commands import UploadMediaCommand
from commands.site_commands import GetCategoriesCommand, CreateCategoryCommand, GetUsersCommand

app = typer.Typer(help="WordPress AI Agent - Manage your WordPress site with AI")

class Agent:
    """Central agent to dispatch commands."""
    
    @staticmethod
    def execute_command(command) -> any:
        """Execute a command and handle errors."""
        try:
            result = command.execute()
            return result
        except Exception as e:
            typer.echo(f"❌ Error: {str(e)}", err=True)
            raise typer.Exit(1)

@app.command()
def create_post(
    topic: str,
    ai: Optional[str] = typer.Option(None, help="AI provider: openai, anthropic, ollama"),
    status: str = typer.Option("draft", help="Post status: draft, publish"),
    tone: str = typer.Option("professional", help="Content tone")
):
    """Create a new WordPress post."""
    command = CreatePostCommand(topic, ai, status, tone)
    result = Agent.execute_command(command)
    
    typer.echo(f"✅ Post created successfully!")
    typer.echo(f"📝 ID: {result['id']}")
    typer.echo(f"📋 Title: {result['title']['rendered']}")
    typer.echo(f"🔗 URL: {result['link']}")

@app.command()
def edit_post(
    post_id: int,
    title: Optional[str] = typer.Option(None, help="New title"),
    content: Optional[str] = typer.Option(None, help="New content"),
    status: Optional[str] = typer.Option(None, help="New status")
):
    """Edit an existing post."""
    updates = {}
    if title:
        updates['title'] = title
    if content:
        updates['content'] = content
    if status:
        updates['status'] = status
    
    if not updates:
        typer.echo("❌ No updates provided")
        raise typer.Exit(1)
    
    command = EditPostCommand(post_id, **updates)
    result = Agent.execute_command(command)
    
    typer.echo(f"✅ Post {post_id} updated successfully!")
    typer.echo(f"📋 Title: {result['title']['rendered']}")

@app.command()
def publish_post(post_id: int):
    """Publish a draft post."""
    command = PublishPostCommand(post_id)
    result = Agent.execute_command(command)
    
    typer.echo(f"✅ Post {post_id} published successfully!")
    typer.echo(f"🔗 URL: {result['link']}")

@app.command()
def delete_post(post_id: int):
    """Delete a post."""
    command = DeletePostCommand(post_id)
    Agent.execute_command(command)
    
    typer.echo(f"✅ Post {post_id} deleted successfully!")

@app.command()
def schedule_post(post_id: int, date: str):
    """Schedule a post for future publishing."""
    command = SchedulePostCommand(post_id, date)
    result = Agent.execute_command(command)
    
    typer.echo(f"✅ Post {post_id} scheduled for {date}")
    typer.echo(f"🔗 URL: {result['link']}")

@app.command()
def upload_media(
    file_path: str,
    title: Optional[str] = typer.Option("", help="Media title"),
    description: Optional[str] = typer.Option("", help="Media description")
):
    """Upload a media file."""
    command = UploadMediaCommand(file_path, title, description)
    result = Agent.execute_command(command)
    
    typer.echo(f"✅ Media uploaded successfully!")
    typer.echo(f"📁 ID: {result['id']}")
    typer.echo(f"🔗 URL: {result['source_url']}")

@app.command()
def list_categories():
    """List all site categories."""
    command = GetCategoriesCommand()
    categories = Agent.execute_command(command)
    
    typer.echo("📂 Site Categories:")
    for cat in categories:
        typer.echo(f"  • {cat['name']} (ID: {cat['id']}) - {cat['count']} posts")

@app.command()
def create_category(name: str, description: str = ""):
    """Create a new category."""
    command = CreateCategoryCommand(name, description)
    result = Agent.execute_command(command)
    
    typer.echo(f"✅ Category '{name}' created successfully!")
    typer.echo(f"📁 ID: {result['id']}")

@app.command()
def list_users():
    """List site users."""
    command = GetUsersCommand()
    users = Agent.execute_command(command)
    
    typer.echo("👥 Site Users:")
    for user in users:
        typer.echo(f"  • {user['name']} ({user['slug']}) - ID: {user['id']}")

if __name__ == "__main__":
    app()