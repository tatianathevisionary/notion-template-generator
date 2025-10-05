#!/usr/bin/env python3
"""
Notion Template Generator MCP Server

This MCP server exposes prompts (knowledge base) and tools (capabilities) for
AI assistants to help with Notion automation, content generation, and research.

Based on Model Context Protocol (MCP) specification.
Resources: https://modelcontextprotocol.io/

Server Capabilities:
- Prompts: 12 strategic knowledge documents about Notion, APIs, and workflows
- Tools: 15+ callable functions for Notion API, web research, updates, and database operations
"""

import sys
import logging
from pathlib import Path
from typing import Any, Dict, Optional, List

# Configure logging to stderr (NEVER stdout for STDIO servers)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("FastMCP not installed. Run: pip install 'mcp[cli]'")
    sys.exit(1)

# Import our tools
from tools import (
    # Notion tools
    update_notion_page,
    query_notion_database,
    create_notion_database,
    get_database_schema,
    # Advanced Notion tools
    upload_file_to_notion,
    modify_database_schema,
    delete_notion_page,
    restore_notion_page,
    move_notion_page,
    duplicate_notion_page,
    # Research tools
    search_web,
    analyze_content,
    # Update tools
    generate_multi_format_update,
    create_update_template,
    validate_update_data,
    # Database tools
    analyze_database,
    enhance_database,
    export_database_structure,
    compare_databases
)

# Initialize FastMCP server
mcp = FastMCP("notion-template-generator")

# Get prompts directory
PROMPTS_DIR = Path(__file__).parent / "prompts"


# ============================================================================
# PROMPTS (Knowledge Base)
# ============================================================================
# These provide AI assistants with strategic context and documentation

@mcp.prompt()
def agents_guide() -> str:
    """AI Assistant Rules & Commands for the Notion Template Generator project."""
    try:
        return (PROMPTS_DIR / "agents.prompt").read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error loading agents prompt: {e}")
        return f"Error loading prompt: {e}"


@mcp.prompt()
def api_migration_guide() -> str:
    """Notion API 2025-09-03 Migration Guide - critical for data sources architecture."""
    try:
        return (PROMPTS_DIR / "api_migration.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def block_types_reference() -> str:
    """Complete reference of all 15 major Notion block types with examples."""
    try:
        return (PROMPTS_DIR / "block_types_showcase.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def system_guide() -> str:
    """Complete system guide covering all features and workflows."""
    try:
        return (PROMPTS_DIR / "complete_system_guide.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def content_creation_guide() -> str:
    """Guidelines for creating engaging Notion content with rich elements."""
    try:
        return (PROMPTS_DIR / "content_guide.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def linkedin_content_os_guide() -> str:
    """Complete guide for LinkedIn Content OS - 12 pages, 5 databases, 300+ blocks."""
    try:
        return (PROMPTS_DIR / "linkedin_guide.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def quickstart() -> str:
    """Quick start guide for getting up and running quickly."""
    try:
        return (PROMPTS_DIR / "quickstart.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def project_overview() -> str:
    """High-level project overview, features, and architecture."""
    try:
        return (PROMPTS_DIR / "readme.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def success_stories() -> str:
    """Implementation examples and success stories."""
    try:
        return (PROMPTS_DIR / "success_stories.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def update_system_guide() -> str:
    """Multi-format update generation system (Document, Slack, LinkedIn, Blog)."""
    try:
        return (PROMPTS_DIR / "update_system.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def session_summary() -> str:
    """Detailed session summary of recent development work."""
    try:
        return (PROMPTS_DIR / "session_summary.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


@mcp.prompt()
def weekly_update_example() -> str:
    """Example of a high-quality weekly update for reference."""
    try:
        return (PROMPTS_DIR / "weekly_update_example.prompt").read_text(encoding='utf-8')
    except Exception as e:
        return f"Error loading prompt: {e}"


# ============================================================================
# TOOLS (Callable Functions)
# ============================================================================
# These enable AI assistants to take actions

# --- Notion Tools ---

@mcp.tool()
def update_page(
    page_id: str,
    content: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a Notion page with new content blocks.
    
    Args:
        page_id: The ID of the Notion page to update
        content: Dictionary containing blocks (format: {"children": [block1, block2...]})
        api_key: Optional Notion API key (defaults to NOTION_API_KEY env var)
    """
    return update_notion_page(page_id, content, api_key)


@mcp.tool()
def query_database(
    database_id: str,
    filter_conditions: Optional[Dict[str, Any]] = None,
    sorts: Optional[list] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query a Notion database with optional filters and sorting.
    
    Args:
        database_id: The ID of the database to query
        filter_conditions: Optional filter criteria (Notion API format)
        sorts: Optional sort criteria
        api_key: Optional Notion API key
    """
    return query_notion_database(database_id, filter_conditions, sorts, api_key)


@mcp.tool()
def create_database(
    title: str,
    properties: Dict[str, Any],
    parent_page_id: Optional[str] = None,
    icon: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new Notion database with specified schema.
    
    Args:
        title: Name of the database
        properties: Database schema (property definitions)
        parent_page_id: Optional parent page ID (must be full UUID format)
        icon: Optional emoji or file icon
        api_key: Optional Notion API key
    """
    return create_notion_database(title, properties, parent_page_id, icon, None, api_key)


@mcp.tool()
def get_schema(
    database_id: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve the complete schema of a Notion database.
    
    Args:
        database_id: The ID of the database
        api_key: Optional Notion API key
    """
    return get_database_schema(database_id, api_key)


# --- Research Tools ---

@mcp.tool()
def web_search(
    query: str,
    max_results: int = 10,
    search_type: str = "general"
) -> Dict[str, Any]:
    """
    Perform web search to gather information.
    
    Args:
        query: The search query string
        max_results: Maximum number of results (default: 10)
        search_type: Type of search ("general", "technical", "news", "academic")
    """
    return search_web(query, max_results, search_type)


@mcp.tool()
def analyze_text(
    content: str,
    analysis_type: str = "general",
    extract_key_points: bool = True
) -> Dict[str, Any]:
    """
    Analyze text content for insights and key points.
    
    Args:
        content: The text content to analyze
        analysis_type: Type of analysis ("general", "technical", "sentiment", "summary")
        extract_key_points: Whether to extract key points (default: True)
    """
    return analyze_content(content, analysis_type, extract_key_points)


# --- Update Tools ---

@mcp.tool()
def generate_update(
    project_name: str,
    update_data: Dict[str, Any],
    formats: Optional[list] = None,
    output_dir: str = "."
) -> Dict[str, Any]:
    """
    Generate updates in multiple formats (document, slack, linkedin, blog).
    
    Args:
        project_name: Name of the project
        update_data: Structured update data (see create_update_template for format)
        formats: List of formats to generate (default: all)
        output_dir: Directory to save outputs
    """
    return generate_multi_format_update(project_name, update_data, formats, output_dir)


@mcp.tool()
def get_update_template() -> Dict[str, Any]:
    """
    Get the template structure for update data with examples and tips.
    """
    return create_update_template()


@mcp.tool()
def validate_update(update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate update data structure before generating updates.
    
    Args:
        update_data: The update data to validate
    """
    return validate_update_data(update_data)


# --- Database Tools ---

@mcp.tool()
def analyze_db(
    database_id: str,
    include_content_analysis: bool = True,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze a Notion database to understand its structure and content.
    
    Args:
        database_id: The ID of the database to analyze
        include_content_analysis: Whether to analyze existing content (default: True)
        api_key: Optional Notion API key
    """
    return analyze_database(database_id, include_content_analysis, api_key)


@mcp.tool()
def enhance_db(
    database_id: str,
    enhancement_type: str = "template",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enhance a Notion database by adding rich content pages.
    
    Args:
        database_id: The ID of the database to enhance
        enhancement_type: Type ("template", "best_practices", "examples", "all")
        api_key: Optional Notion API key
    """
    return enhance_database(database_id, enhancement_type, None, api_key)


@mcp.tool()
def export_db_structure(
    database_id: str,
    output_file: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Export complete database structure to JSON file.
    
    Args:
        database_id: The ID of the database to export
        output_file: Optional file path (default: auto-generated)
        api_key: Optional Notion API key
    """
    return export_database_structure(database_id, output_file, api_key)


@mcp.tool()
def compare_dbs(
    database_id_1: str,
    database_id_2: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compare two Notion databases to identify similarities and differences.
    
    Args:
        database_id_1: First database ID
        database_id_2: Second database ID
        api_key: Optional Notion API key
    """
    return compare_databases(database_id_1, database_id_2, api_key)


# --- Advanced Notion Tools ---

@mcp.tool()
def upload_file(
    file_path: str,
    file_name: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Upload a file to Notion and return the file ID for use in blocks.
    
    Args:
        file_path: Path to the file to upload
        file_name: Optional custom name for the file
        api_key: Optional Notion API key
    """
    return upload_file_to_notion(file_path, file_name, api_key)


@mcp.tool()
def modify_database(
    database_id: str,
    add_properties: Optional[Dict[str, Any]] = None,
    remove_properties: Optional[List[str]] = None,
    modify_properties: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Modify database schema by adding, removing, or modifying properties.
    
    Args:
        database_id: ID of the database to modify
        add_properties: New properties to add
        remove_properties: Property names to remove
        modify_properties: Properties to modify
        api_key: Optional Notion API key
    """
    return modify_database_schema(database_id, add_properties, remove_properties, modify_properties, api_key)


@mcp.tool()
def delete_page(
    page_id: str,
    permanent: bool = False,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a page (move to trash or permanently delete).
    
    Args:
        page_id: ID of the page to delete
        permanent: If True, permanently delete (not supported by Notion API)
        api_key: Optional Notion API key
    """
    return delete_notion_page(page_id, permanent, api_key)


@mcp.tool()
def restore_page(
    page_id: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Restore a page from trash.
    
    Args:
        page_id: ID of the page to restore
        api_key: Optional Notion API key
    """
    return restore_notion_page(page_id, api_key)


@mcp.tool()
def move_page(
    page_id: str,
    new_parent_id: str,
    new_parent_type: str = "page_id",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Move a page to a new parent.
    
    Args:
        page_id: ID of the page to move
        new_parent_id: ID of the new parent (page or database)
        new_parent_type: Type of new parent ("page_id" or "database_id")
        api_key: Optional Notion API key
    """
    return move_notion_page(page_id, new_parent_id, new_parent_type, api_key)


@mcp.tool()
def duplicate_page(
    page_id: str,
    new_title: Optional[str] = None,
    new_parent_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Duplicate a page with all its content.
    
    Args:
        page_id: ID of the page to duplicate
        new_title: Optional new title for the duplicated page
        new_parent_id: Optional new parent ID (uses same parent if not provided)
        api_key: Optional Notion API key
    """
    return duplicate_notion_page(page_id, new_title, new_parent_id, api_key)


# ============================================================================
# SERVER INITIALIZATION
# ============================================================================

def main():
    """Run the MCP server."""
    logger.info("Starting Notion Template Generator MCP Server")
    logger.info(f"Prompts directory: {PROMPTS_DIR}")
    logger.info(f"Available prompts: {len([f for f in PROMPTS_DIR.glob('*.prompt')])}")
    logger.info("Initializing server with STDIO transport...")
    
    # Run the server with STDIO transport
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()

