"""
Database Tool

Provides database analysis and enhancement capabilities for Notion databases.
Leverages existing notion_enhancer.py functionality.
"""

import sys
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from notion_api_client import NotionTemplateClient
except ImportError:
    NotionTemplateClient = None
    print("Warning: notion_api_client not found. Database tools will operate in placeholder mode.")


def analyze_database(
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
        
    Returns:
        Dictionary with comprehensive database analysis
        
    Example:
        >>> analyze_database(database_id="abc123")
        {
            "status": "success",
            "database_id": "abc123",
            "title": "My Database",
            "properties": {...},
            "property_count": 5,
            "content_analysis": {...}
        }
    """
    if NotionTemplateClient is None:
        return {
            "status": "placeholder",
            "message": "Notion client not available. Would analyze database.",
            "database_id": database_id,
            "include_content_analysis": include_content_analysis
        }
    
    try:
        client = NotionTemplateClient(api_key=api_key)
        
        # Get database metadata
        database = client.get_database(database_id)
        title = database.get("title", [{}])[0].get("plain_text", "Untitled")
        
        # Get data source information
        data_source_id = client.get_data_source_id(database_id)
        data_source = client.retrieve_data_source(data_source_id)
        
        # Extract properties
        properties = data_source.get("schema", {}).get("properties", {})
        
        # Analyze property types
        property_analysis = {}
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get("type", "unknown")
            property_analysis[prop_name] = {
                "type": prop_type,
                "id": prop_data.get("id"),
                "config": prop_data.get(prop_type, {})
            }
        
        analysis = {
            "status": "success",
            "database_id": database_id,
            "title": title,
            "url": database.get("url"),
            "data_source_id": data_source_id,
            "properties": property_analysis,
            "property_count": len(properties),
            "property_types": list(set(p["type"] for p in property_analysis.values())),
            "icon": database.get("icon"),
            "cover": database.get("cover")
        }
        
        # Content analysis if requested
        if include_content_analysis:
            try:
                # Query database to get page count
                results = client.query_database(
                    database_id=database_id,
                    data_source_id=data_source_id
                )
                
                analysis["content_analysis"] = {
                    "total_pages": len(results) if isinstance(results, list) else 0,
                    "sample_available": len(results) > 0 if isinstance(results, list) else False
                }
            except Exception as e:
                analysis["content_analysis"] = {
                    "error": str(e),
                    "message": "Could not retrieve content analysis"
                }
        
        return analysis
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_id": database_id
        }


def enhance_database(
    database_id: str,
    enhancement_type: str = "template",
    custom_content: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enhance a Notion database by adding rich content pages.
    
    Args:
        database_id: The ID of the database to enhance
        enhancement_type: Type of enhancement ("template", "best_practices", "examples", "all")
        custom_content: Optional custom content to add
        api_key: Optional Notion API key
        
    Returns:
        Dictionary with enhancement results
        
    Example:
        >>> enhance_database(
        ...     database_id="abc123",
        ...     enhancement_type="best_practices"
        ... )
        {
            "status": "success",
            "pages_created": 3,
            "blocks_added": 150
        }
    """
    if NotionTemplateClient is None:
        return {
            "status": "placeholder",
            "message": "Notion client not available. Would enhance database.",
            "database_id": database_id,
            "enhancement_type": enhancement_type
        }
    
    try:
        client = NotionTemplateClient(api_key=api_key)
        
        # Get database analysis first
        analysis = analyze_database(database_id, include_content_analysis=False, api_key=api_key)
        
        if analysis["status"] != "success":
            return analysis
        
        # Prepare enhancement content based on type
        pages_to_create = []
        
        if enhancement_type in ["template", "all"]:
            pages_to_create.append({
                "type": "template",
                "title": "📝 Templates & Frameworks",
                "description": "Pre-built templates for common use cases"
            })
        
        if enhancement_type in ["best_practices", "all"]:
            pages_to_create.append({
                "type": "best_practices",
                "title": "✨ Best Practices",
                "description": "Guidelines for optimal usage"
            })
        
        if enhancement_type in ["examples", "all"]:
            pages_to_create.append({
                "type": "examples",
                "title": "💡 Examples",
                "description": "Real-world examples and case studies"
            })
        
        # Add custom content if provided
        if custom_content:
            pages_to_create.append({
                "type": "custom",
                "title": custom_content.get("title", "Custom Content"),
                "description": custom_content.get("description", ""),
                "content": custom_content.get("content", [])
            })
        
        return {
            "status": "placeholder",
            "message": "Enhancement functionality not yet fully implemented.",
            "database_id": database_id,
            "database_title": analysis.get("title"),
            "enhancement_type": enhancement_type,
            "planned_pages": len(pages_to_create),
            "page_types": [p["type"] for p in pages_to_create],
            "note": "In production, would create rich content pages with templates, best practices, examples, etc."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_id": database_id
        }


def export_database_structure(
    database_id: str,
    output_file: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Export complete database structure to JSON.
    
    Args:
        database_id: The ID of the database to export
        output_file: Optional file path to save JSON (default: auto-generated)
        api_key: Optional Notion API key
        
    Returns:
        Dictionary with export results and structure
    """
    analysis = analyze_database(database_id, include_content_analysis=True, api_key=api_key)
    
    if analysis["status"] != "success":
        return analysis
    
    # Generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = analysis.get("title", "database").lower().replace(" ", "_")
        output_file = f"{safe_title}_structure_{timestamp}.json"
    
    try:
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "database_id": database_id,
            "output_file": output_file,
            "structure": analysis
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_id": database_id,
            "structure": analysis  # Return structure even if file save fails
        }


def compare_databases(
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
        
    Returns:
        Dictionary with comparison results
    """
    # Analyze both databases
    db1_analysis = analyze_database(database_id_1, include_content_analysis=False, api_key=api_key)
    db2_analysis = analyze_database(database_id_2, include_content_analysis=False, api_key=api_key)
    
    if db1_analysis["status"] != "success" or db2_analysis["status"] != "success":
        return {
            "status": "error",
            "message": "Failed to analyze one or both databases",
            "db1": db1_analysis,
            "db2": db2_analysis
        }
    
    # Compare properties
    props1 = set(db1_analysis["properties"].keys())
    props2 = set(db2_analysis["properties"].keys())
    
    common_props = props1.intersection(props2)
    unique_to_db1 = props1 - props2
    unique_to_db2 = props2 - props1
    
    return {
        "status": "success",
        "database_1": {
            "id": database_id_1,
            "title": db1_analysis["title"],
            "property_count": db1_analysis["property_count"]
        },
        "database_2": {
            "id": database_id_2,
            "title": db2_analysis["title"],
            "property_count": db2_analysis["property_count"]
        },
        "comparison": {
            "common_properties": list(common_props),
            "common_count": len(common_props),
            "unique_to_db1": list(unique_to_db1),
            "unique_to_db2": list(unique_to_db2),
            "similarity_score": len(common_props) / max(len(props1), len(props2)) if max(len(props1), len(props2)) > 0 else 0
        }
    }

