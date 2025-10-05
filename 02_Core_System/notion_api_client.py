"""
Notion API Client Wrapper

This module provides a clean interface for interacting with the Notion API.
It handles authentication, error handling, and common operations like creating
databases, pages, and blocks.

Note: This file is named 'notion_api_client.py' (not 'notion_client.py') to avoid
      conflicts with the installed 'notion-client' package.
"""

import os
from typing import Dict, List, Any, Optional
from notion_client import Client
from notion_client.errors import APIResponseError
from dotenv import load_dotenv


class NotionTemplateClient:
    """
    A wrapper around the Notion SDK client that provides helper methods
    for creating templates programmatically.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_version: str = "2025-09-03"):
        """
        Initialize the Notion client.
        
        Args:
            api_key: Notion API key. If not provided, will load from environment.
            api_version: Notion API version (default: "2025-09-03")
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Notion API key not found. Set NOTION_API_KEY in .env file or pass as parameter."
            )
        
        # Initialize Notion client with API version
        self.client = Client(auth=self.api_key, notion_version=api_version)
        self.api_version = api_version
        
        # Get parent page ID from environment
        self.parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
        if not self.parent_page_id:
            raise ValueError(
                "Parent page ID not found. Set NOTION_PARENT_PAGE_ID in .env file."
            )
    
    def create_database(
        self,
        title: str,
        properties: Dict[str, Any],
        parent_page_id: Optional[str] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new database in Notion with API version 2025-09-03.
        
        Args:
            title: The title of the database
            properties: Dictionary defining the database schema (data source properties)
            parent_page_id: Optional parent page ID (uses default if not provided)
            icon: Optional icon for the database
            cover: Optional cover for the database
        
        Returns:
            The created database object (includes data_sources array)
        
        Example:
            properties = {
                "Name": {"title": {}},
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Not Started", "color": "gray"},
                            {"name": "In Progress", "color": "blue"},
                            {"name": "Complete", "color": "green"}
                        ]
                    }
                }
            }
        """
        parent_id = parent_page_id or self.parent_page_id
        
        # Build request body according to 2025-09-03 API
        request_body = {
            "parent": {"type": "page_id", "page_id": parent_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "initial_data_source": {
                "properties": properties
            }
        }
        
        if icon:
            request_body["icon"] = icon
        if cover:
            request_body["cover"] = cover
        
        try:
            response = self.client.databases.create(**request_body)
            print(f"✅ Successfully created database: {title}")
            
            # Store data source info for easy access
            if "data_sources" in response and len(response["data_sources"]) > 0:
                data_source = response["data_sources"][0]
                print(f"   📊 Data source ID: {data_source['id']}")
                print(f"   📊 Data source name: {data_source['name']}")
            
            return response
        
        except APIResponseError as e:
            print(f"❌ Error creating database '{title}': {e}")
            raise
    
    def create_page(
        self,
        parent_id: str,
        title: str,
        properties: Optional[Dict[str, Any]] = None,
        children: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new page in Notion.
        
        Args:
            parent_id: ID of parent database or page
            title: Page title
            properties: Page properties (for database pages)
            children: List of block objects to add as page content
        
        Returns:
            The created page object
        """
        # Determine parent type based on ID format
        if len(parent_id) == 32 and '-' not in parent_id:
            # This is a page ID (32 chars, no dashes) - create sub-page
            parent_obj = {"type": "page_id", "page_id": parent_id}
            # For sub-pages, use simple title property
            page_properties = {"title": [{"text": {"content": title}}]}
        else:
            # This is a database ID (with dashes) - create database page
            parent_obj = {"database_id": parent_id}
            # For database pages, use the database's title property
            page_properties = properties or {"Title": {"title": [{"text": {"content": title}}]}}
        
        page_data = {
            "parent": parent_obj,
            "properties": page_properties
        }
        
        if children:
            page_data["children"] = children
        
        try:
            response = self.client.pages.create(**page_data)
            print(f"✅ Successfully created page: {title}")
            return response
        
        except APIResponseError as e:
            print(f"❌ Error creating page '{title}': {e}")
            raise
    
    def create_page_in_database(
        self,
        database_id: str,
        properties: Dict[str, Any],
        children: Optional[List[Dict[str, Any]]] = None,
        data_source_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new page (row) in a database with properties and content.
        Uses data_source_id for 2025-09-03 API.
        
        Args:
            database_id: ID of the parent database (used if data_source_id not provided)
            properties: Page properties matching the database schema
            children: Optional list of block objects for page content
            data_source_id: Optional data source ID (auto-fetched if not provided)
        
        Returns:
            The created page object
        """
        # Get data_source_id if not provided
        if not data_source_id:
            data_source_id = self.get_data_source_id(database_id)
        
        # Use data_source_id as parent for 2025-09-03 API
        page_data = {
            "parent": {"type": "data_source_id", "data_source_id": data_source_id},
            "properties": properties
        }
        
        if children:
            page_data["children"] = children
        
        try:
            response = self.client.pages.create(**page_data)
            # Extract title from properties for logging
            title = "Untitled"
            if "Name" in properties and "title" in properties["Name"]:
                title_array = properties["Name"]["title"]
                if title_array and len(title_array) > 0:
                    title = title_array[0].get("text", {}).get("content", "Untitled")
            print(f"    ✅ Created page: {title}")
            return response
        
        except APIResponseError as e:
            print(f"    ❌ Error creating page: {e}")
            raise
    
    def append_blocks(
        self,
        block_id: str,
        children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Append blocks to an existing page or block.
        
        Args:
            block_id: ID of the parent block or page
            children: List of block objects to append
        
        Returns:
            The response from the API
        """
        try:
            response = self.client.blocks.children.append(
                block_id=block_id,
                children=children
            )
            print(f"✅ Successfully appended {len(children)} blocks")
            return response
        
        except APIResponseError as e:
            print(f"❌ Error appending blocks: {e}")
            raise
    
    def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Retrieve a database by ID (returns data_sources in 2025-09-03).
        
        Args:
            database_id: The database ID
        
        Returns:
            The database object with data_sources array
        """
        try:
            response = self.client.databases.retrieve(database_id=database_id)
            if "data_sources" in response:
                print(f"📊 Database has {len(response['data_sources'])} data source(s)")
            return response
        except APIResponseError as e:
            print(f"❌ Error retrieving database: {e}")
            raise
    
    def get_data_source_id(self, database_id: str, index: int = 0) -> str:
        """
        Get the data source ID for a database (helper method for 2025-09-03 API).
        
        Args:
            database_id: The database ID
            index: Index of the data source (default: 0 for first/primary data source)
        
        Returns:
            The data source ID
        """
        try:
            database = self.get_database(database_id)
            data_sources = database.get("data_sources", [])
            
            if not data_sources:
                raise ValueError(f"No data sources found for database {database_id}")
            
            if index >= len(data_sources):
                raise ValueError(f"Data source index {index} out of range (database has {len(data_sources)} sources)")
            
            return data_sources[index]["id"]
        
        except APIResponseError as e:
            print(f"❌ Error getting data source ID: {e}")
            raise
    
    def retrieve_data_source(self, data_source_id: str) -> Dict[str, Any]:
        """
        Retrieve a data source by ID (2025-09-03 API).
        
        Args:
            data_source_id: The data source ID
        
        Returns:
            The data source object with properties schema
        """
        try:
            # Use the new data sources endpoint
            response = self.client.request(
                method="GET",
                path=f"data_sources/{data_source_id}"
            )
            return response
        except APIResponseError as e:
            print(f"❌ Error retrieving data source: {e}")
            raise
    
    def query_database(
        self,
        database_id: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        data_source_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Query a database with optional filters (uses data sources in 2025-09-03).
        
        Args:
            database_id: The database ID (used if data_source_id not provided)
            filter_conditions: Optional filter object
            data_source_id: Optional data source ID (auto-fetched if not provided)
        
        Returns:
            List of page objects matching the query
        """
        # Get data_source_id if not provided
        if not data_source_id:
            data_source_id = self.get_data_source_id(database_id)
        
        try:
            # Use the new data sources query endpoint
            query_body = {}
            if filter_conditions:
                query_body["filter"] = filter_conditions
            
            response = self.client.request(
                method="POST",
                path=f"data_sources/{data_source_id}/query",
                body=query_body
            )
            return response.get("results", [])
        except APIResponseError as e:
            print(f"❌ Error querying database: {e}")
            raise
    
    def update_data_source(
        self,
        data_source_id: str,
        properties: Optional[Dict[str, Any]] = None,
        title: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Update a data source's schema or title (2025-09-03 API).
        
        Args:
            data_source_id: The data source ID
            properties: Updated properties schema
            title: Updated title
        
        Returns:
            The updated data source object
        """
        try:
            update_body = {}
            if properties:
                update_body["properties"] = properties
            if title:
                update_body["title"] = title
            
            response = self.client.request(
                method="PATCH",
                path=f"data_sources/{data_source_id}",
                body=update_body
            )
            print(f"✅ Successfully updated data source")
            return response
        except APIResponseError as e:
            print(f"❌ Error updating data source: {e}")
            raise


# Helper functions for all Notion block types

def heading_1(text: str, color: str = "default", is_toggleable: bool = False) -> Dict[str, Any]:
    """Create a heading 1 block with optional color and toggle."""
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color,
            "is_toggleable": is_toggleable
        }
    }


def heading_2(text: str, color: str = "default", is_toggleable: bool = False) -> Dict[str, Any]:
    """Create a heading 2 block with optional color and toggle."""
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color,
            "is_toggleable": is_toggleable
        }
    }


def heading_3(text: str, color: str = "default", is_toggleable: bool = False) -> Dict[str, Any]:
    """Create a heading 3 block with optional color and toggle."""
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color,
            "is_toggleable": is_toggleable
        }
    }


def paragraph(text: str, color: str = "default") -> Dict[str, Any]:
    """Create a paragraph block with optional color."""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color
        }
    }


def bullet_list_item(text: str, color: str = "default") -> Dict[str, Any]:
    """Create a bulleted list item block."""
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color
        }
    }


def numbered_list_item(text: str, color: str = "default") -> Dict[str, Any]:
    """Create a numbered list item block."""
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color
        }
    }


def to_do(text: str, checked: bool = False, color: str = "default") -> Dict[str, Any]:
    """Create a to-do (checkbox) block."""
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "checked": checked,
            "color": color
        }
    }


def toggle(text: str, color: str = "default") -> Dict[str, Any]:
    """Create a toggle block."""
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color
        }
    }


def callout(text: str, icon: str = "💡", color: str = "default") -> Dict[str, Any]:
    """Create a callout block with emoji icon and color."""
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"emoji": icon},
            "color": color
        }
    }


def quote(text: str, color: str = "default") -> Dict[str, Any]:
    """Create a quote block."""
    return {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "color": color
        }
    }


def code(code_text: str, language: str = "python") -> Dict[str, Any]:
    """Create a code block with syntax highlighting."""
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": code_text}}],
            "language": language,
            "caption": []
        }
    }


def table_of_contents(color: str = "default") -> Dict[str, Any]:
    """Create a table of contents block."""
    return {
        "object": "block",
        "type": "table_of_contents",
        "table_of_contents": {
            "color": color
        }
    }


def divider() -> Dict[str, Any]:
    """Create a divider block."""
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }


def bookmark(url: str, caption: str = "") -> Dict[str, Any]:
    """Create a bookmark block."""
    caption_array = [{"type": "text", "text": {"content": caption}}] if caption else []
    return {
        "object": "block",
        "type": "bookmark",
        "bookmark": {
            "url": url,
            "caption": caption_array
        }
    }


def image(url: str, caption: str = "", is_external: bool = True) -> Dict[str, Any]:
    """
    Create an image block.
    
    Args:
        url: URL of the image (external) or file upload ID
        caption: Optional caption for the image
        is_external: True for external URL, False for file upload
    
    Supported external types: .bmp, .gif, .heic, .jpeg, .jpg, .png, .svg, .tif, .tiff
    """
    caption_array = [{"type": "text", "text": {"content": caption}}] if caption else []
    
    if is_external:
        return {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": url},
                "caption": caption_array
            }
        }
    else:
        # For file uploads
        return {
            "object": "block",
            "type": "image",
            "image": {
                "type": "file_upload",
                "file_upload": {"id": url},  # url is actually the file_upload_id here
                "caption": caption_array
            }
        }


def video(url: str, caption: str = "", is_external: bool = True) -> Dict[str, Any]:
    """
    Create a video block.
    
    Args:
        url: URL of the video or file upload ID
        caption: Optional caption for the video
        is_external: True for external URL, False for file upload
    
    Supported types: .mp4, .mov, .avi, .mkv, .wmv, YouTube/Vimeo URLs
    """
    caption_array = [{"type": "text", "text": {"content": caption}}] if caption else []
    
    if is_external:
        return {
            "object": "block",
            "type": "video",
            "video": {
                "type": "external",
                "external": {"url": url},
                "caption": caption_array
            }
        }
    else:
        return {
            "object": "block",
            "type": "video",
            "video": {
                "type": "file_upload",
                "file_upload": {"id": url},
                "caption": caption_array
            }
        }


def audio(url: str, caption: str = "", is_external: bool = True) -> Dict[str, Any]:
    """
    Create an audio block.
    
    Args:
        url: URL of the audio file or file upload ID
        caption: Optional caption for the audio
        is_external: True for external URL, False for file upload
    
    Supported types: .mp3, .wav, .ogg, .oga, .m4a
    """
    caption_array = [{"type": "text", "text": {"content": caption}}] if caption else []
    
    if is_external:
        return {
            "object": "block",
            "type": "audio",
            "audio": {
                "type": "external",
                "external": {"url": url},
                "caption": caption_array
            }
        }
    else:
        return {
            "object": "block",
            "type": "audio",
            "audio": {
                "type": "file_upload",
                "file_upload": {"id": url},
                "caption": caption_array
            }
        }


def file(url: str, name: str = "", caption: str = "", is_external: bool = True) -> Dict[str, Any]:
    """
    Create a file block.
    
    Args:
        url: URL of the file or file upload ID
        name: Name of the file as displayed in Notion
        caption: Optional caption for the file
        is_external: True for external URL, False for file upload
    """
    caption_array = [{"type": "text", "text": {"content": caption}}] if caption else []
    
    if is_external:
        return {
            "object": "block",
            "type": "file",
            "file": {
                "type": "external",
                "external": {"url": url},
                "caption": caption_array,
                "name": name
            }
        }
    else:
        return {
            "object": "block",
            "type": "file",
            "file": {
                "type": "file_upload",
                "file_upload": {"id": url},
                "caption": caption_array,
                "name": name
            }
        }


def pdf(url: str, caption: str = "", is_external: bool = True) -> Dict[str, Any]:
    """
    Create a PDF block.
    
    Args:
        url: URL of the PDF file or file upload ID
        caption: Optional caption for the PDF
        is_external: True for external URL, False for file upload
    """
    caption_array = [{"type": "text", "text": {"content": caption}}] if caption else []
    
    if is_external:
        return {
            "object": "block",
            "type": "pdf",
            "pdf": {
                "type": "external",
                "external": {"url": url},
                "caption": caption_array
            }
        }
    else:
        return {
            "object": "block",
            "type": "pdf",
            "pdf": {
                "type": "file_upload",
                "file_upload": {"id": url},
                "caption": caption_array
            }
        }


def embed(url: str) -> Dict[str, Any]:
    """
    Create an embed block for embedding external content.
    
    Args:
        url: URL to embed (website, service, etc.)
    
    Note: Notion uses iFramely for validation. Not all URLs may render correctly.
    """
    return {
        "object": "block",
        "type": "embed",
        "embed": {
            "url": url
        }
    }


def breadcrumb() -> Dict[str, Any]:
    """Create a breadcrumb block (navigation trail)."""
    return {
        "object": "block",
        "type": "breadcrumb",
        "breadcrumb": {}
    }


def table(table_width: int, has_column_header: bool = False, has_row_header: bool = False) -> Dict[str, Any]:
    """
    Create a table block.
    
    Args:
        table_width: Number of columns (cannot be changed after creation)
        has_column_header: Whether first row is a header
        has_row_header: Whether first column is a header
    
    Note: Must be created with at least one table_row child.
    """
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": has_column_header,
            "has_row_header": has_row_header
        }
    }


def table_row(cells: List[List[str]]) -> Dict[str, Any]:
    """
    Create a table row block.
    
    Args:
        cells: List of cell contents (strings). Length must match table_width.
               Each cell can contain multiple text objects.
    
    Example:
        table_row([["Cell 1"], ["Cell 2"], ["Cell 3"]])
    """
    formatted_cells = []
    for cell in cells:
        # Convert each cell (list of strings) to rich text objects
        rich_text_array = []
        for text in cell:
            rich_text_array.append({
                "type": "text",
                "text": {"content": text}
            })
        formatted_cells.append(rich_text_array)
    
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {
            "cells": formatted_cells
        }
    }


def column_list() -> Dict[str, Any]:
    """
    Create a column list block (container for columns).
    
    Note: Must have at least 2 column children when created.
    """
    return {
        "object": "block",
        "type": "column_list",
        "column_list": {}
    }


def column(width_ratio: Optional[float] = None) -> Dict[str, Any]:
    """
    Create a column block (must be child of column_list).
    
    Args:
        width_ratio: Optional width ratio (0-1). When omitted, equal widths are used.
                    All columns in a list should add up to 1.
    
    Note: Columns can contain any block type except other columns.
    """
    column_obj = {}
    if width_ratio is not None:
        column_obj["width_ratio"] = width_ratio
    
    return {
        "object": "block",
        "type": "column",
        "column": column_obj
    }


def equation(expression: str) -> Dict[str, Any]:
    """
    Create an equation block using KaTeX syntax.
    
    Args:
        expression: LaTeX/KaTeX equation expression
    
    Example:
        equation("e=mc^2")
        equation("\\frac{a}{b}")
    """
    return {
        "object": "block",
        "type": "equation",
        "equation": {
            "expression": expression
        }
    }


def synced_block(block_id: Optional[str] = None, children: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Create a synced block.
    
    Args:
        block_id: If provided, creates a duplicate synced to the original block.
                 If None, creates an original synced block.
        children: Child blocks (only for original synced blocks)
    
    Note: Original must be created before duplicates.
    """
    if block_id:
        # Duplicate synced block
        return {
            "object": "block",
            "type": "synced_block",
            "synced_block": {
                "synced_from": {
                    "type": "block_id",
                    "block_id": block_id
                }
            }
        }
    else:
        # Original synced block
        block = {
            "object": "block",
            "type": "synced_block",
            "synced_block": {
                "synced_from": None
            }
        }
        if children:
            block["synced_block"]["children"] = children
        return block


# ============================================================================
# ADVANCED CAPABILITIES: FILE UPLOADS, DATABASE MODIFICATIONS, PAGE MANAGEMENT
# ============================================================================

class AdvancedNotionClient(NotionTemplateClient):
    """
    Extended Notion client with advanced capabilities including:
    - File uploads
    - Database schema modifications
    - Page deletion and moving
    """
    
    def upload_file(self, file_path: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a file block with external file URL (Notion API doesn't support direct file uploads).
        
        Args:
            file_path: Path to the file (for reference only - file must be hosted externally)
            file_name: Optional custom name for the file
        
        Returns:
            Dictionary with file block information
        """
        from pathlib import Path
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_name = file_name or file_path.name
        file_size = file_path.stat().st_size
        
        # Notion API doesn't support direct file uploads
        # Files must be hosted externally and referenced via URL
        print(f"⚠️  Notion API doesn't support direct file uploads.")
        print(f"   File '{file_name}' ({file_size} bytes) must be hosted externally.")
        print(f"   Use external_file_block() with a public URL instead.")
        
        return {
            "status": "info",
            "message": "Notion API doesn't support direct file uploads. Use external_file_block() with a public URL.",
            "file_name": file_name,
            "file_size": file_size,
            "suggestion": "Host file externally and use external_file_block() with the URL"
        }
    
    def _get_content_type(self, file_extension: str) -> str:
        """Get MIME type for file extension."""
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.json': 'application/json'
        }
        return content_types.get(file_extension.lower(), 'application/octet-stream')
    
    def modify_database_schema(
        self,
        database_id: str,
        add_properties: Optional[Dict[str, Any]] = None,
        remove_properties: Optional[List[str]] = None,
        modify_properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Modify database schema by adding, removing, or modifying properties.
        
        Args:
            database_id: ID of the database to modify
            add_properties: New properties to add
            remove_properties: Property names to remove
            modify_properties: Properties to modify
        
        Returns:
            Dictionary with modification results
        """
        try:
            # Get current data source
            data_source_id = self.get_data_source_id(database_id)
            current_data_source = self.retrieve_data_source(data_source_id)
            current_properties = current_data_source.get("schema", {}).get("properties", {})
            
            # Create updated properties
            updated_properties = current_properties.copy()
            
            # Add new properties
            if add_properties:
                updated_properties.update(add_properties)
                print(f"➕ Adding {len(add_properties)} new properties")
            
            # Remove properties
            if remove_properties:
                for prop_name in remove_properties:
                    if prop_name in updated_properties:
                        del updated_properties[prop_name]
                        print(f"➖ Removing property: {prop_name}")
            
            # Modify properties
            if modify_properties:
                updated_properties.update(modify_properties)
                print(f"✏️ Modifying {len(modify_properties)} properties")
            
            # Update the data source
            response = self.update_data_source(
                data_source_id=data_source_id,
                properties=updated_properties
            )
            
            print(f"✅ Successfully modified database schema")
            return {
                "status": "success",
                "database_id": database_id,
                "data_source_id": data_source_id,
                "properties_added": len(add_properties) if add_properties else 0,
                "properties_removed": len(remove_properties) if remove_properties else 0,
                "properties_modified": len(modify_properties) if modify_properties else 0,
                "total_properties": len(updated_properties)
            }
            
        except Exception as e:
            print(f"❌ Error modifying database schema: {e}")
            raise
    
    def delete_page(self, page_id: str, permanent: bool = False) -> Dict[str, Any]:
        """
        Delete a page (move to trash or permanently delete).
        
        Args:
            page_id: ID of the page to delete
            permanent: If True, permanently delete (not implemented in Notion API)
        
        Returns:
            Dictionary with deletion results
        """
        try:
            if permanent:
                # Notion API doesn't support permanent deletion
                raise ValueError("Permanent deletion is not supported by Notion API")
            
            # Archive the page (move to trash)
            response = self.client.pages.update(
                page_id=page_id,
                archived=True
            )
            
            print(f"✅ Successfully moved page to trash")
            return {
                "status": "success",
                "page_id": page_id,
                "action": "archived",
                "message": "Page moved to trash (can be restored)"
            }
            
        except Exception as e:
            print(f"❌ Error deleting page: {e}")
            raise
    
    def restore_page(self, page_id: str) -> Dict[str, Any]:
        """
        Restore a page from trash.
        
        Args:
            page_id: ID of the page to restore
        
        Returns:
            Dictionary with restoration results
        """
        try:
            response = self.client.pages.update(
                page_id=page_id,
                archived=False
            )
            
            print(f"✅ Successfully restored page from trash")
            return {
                "status": "success",
                "page_id": page_id,
                "action": "restored",
                "message": "Page restored from trash"
            }
            
        except Exception as e:
            print(f"❌ Error restoring page: {e}")
            raise
    
    def move_page(
        self,
        page_id: str,
        new_parent_id: str,
        new_parent_type: str = "page_id"
    ) -> Dict[str, Any]:
        """
        Move a page to a new parent.
        
        Args:
            page_id: ID of the page to move
            new_parent_id: ID of the new parent (page or database)
            new_parent_type: Type of new parent ("page_id" or "database_id")
        
        Returns:
            Dictionary with move results
        """
        try:
            # Determine parent object structure
            if new_parent_type == "page_id":
                parent_obj = {"type": "page_id", "page_id": new_parent_id}
            elif new_parent_type == "database_id":
                parent_obj = {"database_id": new_parent_id}
            else:
                raise ValueError(f"Invalid parent type: {new_parent_type}")
            
            response = self.client.pages.update(
                page_id=page_id,
                parent=parent_obj
            )
            
            print(f"✅ Successfully moved page to new parent")
            return {
                "status": "success",
                "page_id": page_id,
                "new_parent_id": new_parent_id,
                "new_parent_type": new_parent_type,
                "message": "Page moved successfully"
            }
            
        except Exception as e:
            print(f"❌ Error moving page: {e}")
            raise
    
    def duplicate_page(
        self,
        page_id: str,
        new_title: Optional[str] = None,
        new_parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Duplicate a page with all its content.
        
        Args:
            page_id: ID of the page to duplicate
            new_title: Optional new title for the duplicated page
            new_parent_id: Optional new parent ID (uses same parent if not provided)
        
        Returns:
            Dictionary with duplication results
        """
        try:
            # Get the original page
            original_page = self.client.pages.retrieve(page_id=page_id)
            
            # Get the page content
            blocks_response = self.client.blocks.children.list(block_id=page_id)
            children = blocks_response.get('results', [])
            
            # Determine parent
            if new_parent_id:
                parent_obj = {"type": "page_id", "page_id": new_parent_id}
            else:
                parent_obj = original_page.get('parent', {})
            
            # Create new page
            new_page_data = {
                "parent": parent_obj,
                "properties": {
                    "title": [{"text": {"content": new_title or f"Copy of {original_page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'Untitled')}"}}]
                },
                "children": children
            }
            
            response = self.client.pages.create(**new_page_data)
            
            print(f"✅ Successfully duplicated page")
            return {
                "status": "success",
                "original_page_id": page_id,
                "new_page_id": response.get('id'),
                "new_title": new_title,
                "message": "Page duplicated successfully"
            }
            
        except Exception as e:
            print(f"❌ Error duplicating page: {e}")
            raise
