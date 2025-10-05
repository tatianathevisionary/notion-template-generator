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
from .update_tool import (
    generate_multi_format_update,
    create_update_template,
    validate_update_data
)
from .database_tool import (
    analyze_database,
    enhance_database,
    export_database_structure,
    compare_databases
)

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
    'create_update_template',
    'validate_update_data',
    # Database tools
    'analyze_database',
    'enhance_database',
    'export_database_structure',
    'compare_databases',
]

__version__ = '1.0.0'
