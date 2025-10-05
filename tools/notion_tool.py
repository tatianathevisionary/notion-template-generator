"""
Notion Integration Tool

Provides comprehensive Notion API operations for AI assistants including:
- Updating page content
- Querying databases
- Creating new databases
- Retrieving database schemas

All functions integrate with Notion API 2025-09-03 (data sources architecture).
"""

import os
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add parent directory to path to import notion_api_client
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from notion_api_client import NotionTemplateClient
except ImportError:
    NotionTemplateClient = None
    print("Warning: notion_api_client not found. Notion tools will operate in placeholder mode.")


def update_notion_page(
    page_id: str,
    content: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a Notion page with new content blocks.
    
    Args:
        page_id: The ID of the Notion page to update
        content: Dictionary containing the blocks to add (format: {"children": [block1, block2...]})
        api_key: Optional Notion API key (defaults to NOTION_API_KEY env var)
    
    Returns:
        Dictionary with status and updated page information
        
    Example:
        >>> update_notion_page(
        ...     page_id="abc123",
        ...     content={"children": [{"type": "paragraph", "paragraph": {"rich_text": [...]}}]}
        ... )
        {"status": "success", "page_id": "abc123", "blocks_added": 5}
    """
    if NotionTemplateClient is None:
        return {
            "status": "placeholder",
            "message": "Notion client not available. Would update page with content.",
            "page_id": page_id,
            "content_preview": str(content)[:200]
        }
    
    try:
        client = NotionTemplateClient(api_key=api_key)
        
        # Extract children blocks
        children = content.get("children", [])
        
        # Append blocks to page
        result = client.append_blocks(block_id=page_id, children=children)
        
        return {
            "status": "success",
            "page_id": page_id,
            "blocks_added": len(children),
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "page_id": page_id
        }


def query_notion_database(
    database_id: str,
    filter_conditions: Optional[Dict[str, Any]] = None,
    sorts: Optional[List[Dict[str, Any]]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query a Notion database with optional filters and sorting.
    
    Args:
        database_id: The ID of the database to query
        filter_conditions: Optional filter criteria (Notion API format)
        sorts: Optional sort criteria (Notion API format)
        api_key: Optional Notion API key
        
    Returns:
        Dictionary with query results
        
    Example:
        >>> query_notion_database(
        ...     database_id="xyz789",
        ...     filter_conditions={"property": "Status", "select": {"equals": "In Progress"}}
        ... )
        {"status": "success", "results": [...], "count": 10}
    """
    if NotionTemplateClient is None:
        return {
            "status": "placeholder",
            "message": "Notion client not available. Would query database.",
            "database_id": database_id,
            "filters": filter_conditions
        }
    
    try:
        client = NotionTemplateClient(api_key=api_key)
        
        # Get data source ID first (2025-09-03 API requirement)
        data_source_id = client.get_data_source_id(database_id)
        
        # Query the database
        results = client.query_database(
            database_id=database_id,
            filter_conditions=filter_conditions,
            sorts=sorts,
            data_source_id=data_source_id
        )
        
        return {
            "status": "success",
            "database_id": database_id,
            "data_source_id": data_source_id,
            "results": results,
            "count": len(results) if isinstance(results, list) else 0
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_id": database_id
        }


def create_notion_database(
    title: str,
    properties: Dict[str, Any],
    parent_page_id: Optional[str] = None,
    icon: Optional[Dict[str, Any]] = None,
    cover: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new Notion database with specified schema.
    
    Args:
        title: Name of the database
        properties: Database schema (property definitions)
        parent_page_id: Optional parent page ID (defaults to NOTION_PARENT_PAGE_ID env var)
        icon: Optional emoji or file icon
        cover: Optional cover image
        api_key: Optional Notion API key
        
    Returns:
        Dictionary with created database information
        
    Example:
        >>> create_notion_database(
        ...     title="Task Tracker",
        ...     properties={"Name": {"title": {}}, "Status": {"select": {"options": [...]}}}
        ... )
        {"status": "success", "database_id": "new123", "data_source_id": "ds456"}
    """
    if NotionTemplateClient is None:
        return {
            "status": "placeholder",
            "message": "Notion client not available. Would create database.",
            "title": title,
            "properties_count": len(properties)
        }
    
    try:
        client = NotionTemplateClient(api_key=api_key)
        
        # Create database
        response = client.create_database(
            title=title,
            properties=properties,
            parent_page_id=parent_page_id,
            icon=icon,
            cover=cover
        )
        
        return {
            "status": "success",
            "database_id": response.get("id"),
            "data_source_id": response.get("data_sources", [{}])[0].get("id"),
            "title": title,
            "url": response.get("url")
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "title": title
        }


def get_database_schema(
    database_id: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve the complete schema of a Notion database.
    
    Args:
        database_id: The ID of the database
        api_key: Optional Notion API key
        
    Returns:
        Dictionary with database schema information
        
    Example:
        >>> get_database_schema(database_id="abc123")
        {
            "status": "success",
            "database_id": "abc123",
            "data_sources": [...],
            "properties": {...},
            "title": "My Database"
        }
    """
    if NotionTemplateClient is None:
        return {
            "status": "placeholder",
            "message": "Notion client not available. Would retrieve schema.",
            "database_id": database_id
        }
    
    try:
        client = NotionTemplateClient(api_key=api_key)
        
        # Get database metadata
        database = client.get_database(database_id)
        
        # Get data source ID and retrieve its schema
        data_source_id = client.get_data_source_id(database_id)
        data_source = client.retrieve_data_source(data_source_id)
        
        return {
            "status": "success",
            "database_id": database_id,
            "title": database.get("title", [{}])[0].get("plain_text", "Untitled"),
            "data_sources": database.get("data_sources", []),
            "properties": data_source.get("schema", {}).get("properties", {}),
            "url": database.get("url")
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_id": database_id
        }


# Convenience functions for common operations
def list_database_properties(database_id: str, api_key: Optional[str] = None) -> List[str]:
    """Get a simple list of property names from a database."""
    schema = get_database_schema(database_id, api_key)
    if schema["status"] == "success":
        return list(schema["properties"].keys())
    return []


def get_database_url(database_id: str, api_key: Optional[str] = None) -> Optional[str]:
    """Get the URL of a Notion database."""
    schema = get_database_schema(database_id, api_key)
    return schema.get("url") if schema["status"] == "success" else None
