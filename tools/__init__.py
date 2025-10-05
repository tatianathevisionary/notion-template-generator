"""
MCP Tools Package

This package contains all the callable tools exposed by the MCP server.
Each tool module provides specific capabilities for AI assistants.
"""

from .notion_tool import (
    update_notion_page,
    query_notion_database,
    create_notion_database,
    get_database_schema
)
from .research_tool import search_web, analyze_content
from .update_tool import generate_multi_format_update
from .database_tool import analyze_database, enhance_database

__all__ = [
    # Notion tools
    'update_notion_page',
    'query_notion_database',
    'create_notion_database',
    'get_database_schema',
    # Research tools
    'search_web',
    'analyze_content',
    # Update tools
    'generate_multi_format_update',
    # Database tools
    'analyze_database',
    'enhance_database',
]

__version__ = '1.0.0'
