"""
MCP Tools Package

This package contains all the callable tools exposed by the MCP server.
Each tool module provides specific capabilities for AI assistants.
"""

from .notion_tool import (
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
    duplicate_notion_page
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
from .comprehensive_page_manager import (
    create_notion_page_comprehensive,
    get_page_hierarchy_comprehensive,
    extract_page_properties_comprehensive,
    update_page_property_comprehensive,
    move_page_comprehensive,
    analyze_page_structure_intelligent_tool
)
from .content_extraction_tool import (
    extract_page_content,
    extract_hierarchy_with_content,
    analyze_page_content_semantic
)
from .working_reorganization_tool import (
    reorganize_notion_pages_intelligent,
    extract_pages_with_full_content,
    create_reorganization_plan_from_content
)
from .cleanup_tool import (
    analyze_workspace_cleanup,
    execute_workspace_cleanup,
    fix_emoji_consistency
)

from .wiki_management_tool import (
    create_notion_wiki,
    verify_notion_page,
    remove_notion_page_verification,
    undo_notion_wiki,
    get_all_verified_pages
)

__all__ = [
    # Notion tools
    'update_notion_page',
    'query_notion_database',
    'create_notion_database',
    'get_database_schema',
    # Advanced Notion tools
    'upload_file_to_notion',
    'modify_database_schema',
    'delete_notion_page',
    'restore_notion_page',
    'move_notion_page',
    'duplicate_notion_page',
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
    # Comprehensive Page Management tools
    'create_notion_page_comprehensive',
    'get_page_hierarchy_comprehensive',
    'extract_page_properties_comprehensive',
    'update_page_property_comprehensive',
    'move_page_comprehensive',
    'analyze_page_structure_intelligent_tool',
    # Content Extraction tools
    'extract_page_content',
    'extract_hierarchy_with_content',
    'analyze_page_content_semantic',
    # Working Reorganization tools
    'reorganize_notion_pages_intelligent',
    'extract_pages_with_full_content',
    'create_reorganization_plan_from_content',
    # Cleanup tools
    'analyze_workspace_cleanup',
    'execute_workspace_cleanup',
    'fix_emoji_consistency',
    
    # Wiki management tools
    'create_notion_wiki',
    'verify_notion_page',
    'remove_notion_page_verification',
    'undo_notion_wiki',
    'get_all_verified_pages',
]

__version__ = '1.0.0'
