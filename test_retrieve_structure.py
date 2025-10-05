#!/usr/bin/env python3
"""
Test Script: Retrieve Database Structure from Notion

This demonstrates the new capability to retrieve and inspect
database structures using the 2025-09-03 API.
"""

from notion_api_client import NotionTemplateClient
import json
from typing import Dict, Any


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def format_property_info(prop_name: str, prop_data: Dict[str, Any]) -> str:
    """Format property information for display."""
    prop_type = prop_data.get("type", "unknown")
    
    info = f"  📌 {prop_name} ({prop_type})"
    
    # Add type-specific details
    if prop_type == "select" and "select" in prop_data:
        options = prop_data["select"].get("options", [])
        if options:
            option_names = [opt["name"] for opt in options]
            info += f"\n      Options: {', '.join(option_names)}"
    
    elif prop_type == "multi_select" and "multi_select" in prop_data:
        options = prop_data["multi_select"].get("options", [])
        if options:
            option_names = [opt["name"] for opt in options]
            info += f"\n      Options: {', '.join(option_names)}"
    
    elif prop_type == "number" and "number" in prop_data:
        number_format = prop_data["number"].get("format", "number")
        info += f"\n      Format: {number_format}"
    
    return info


def retrieve_and_display_structure(database_id: str):
    """
    Retrieve and display the structure of a Notion database.
    
    This demonstrates:
    1. Getting database metadata
    2. Listing data sources
    3. Retrieving data source schema
    4. Displaying property information
    """
    
    print_section("Initializing Notion Client")
    client = NotionTemplateClient()
    print(f"✅ Client initialized with API version: {client.api_version}")
    
    # Step 1: Get Database
    print_section("Step 1: Retrieve Database Metadata")
    try:
        database = client.get_database(database_id)
        
        # Display database info
        title = database.get("title", [{}])[0].get("text", {}).get("content", "Untitled")
        print(f"📊 Database Name: {title}")
        print(f"🆔 Database ID: {database['id']}")
        print(f"📅 Created: {database.get('created_time', 'N/A')}")
        print(f"✏️  Last Edited: {database.get('last_edited_time', 'N/A')}")
        
        # Display parent info
        parent = database.get("parent", {})
        parent_type = parent.get("type", "unknown")
        print(f"📂 Parent Type: {parent_type}")
        
        # Icon and cover
        if database.get("icon"):
            icon_emoji = database["icon"].get("emoji", "N/A")
            print(f"🎨 Icon: {icon_emoji}")
        
        if database.get("cover"):
            print(f"🖼️  Has Cover: Yes")
        
    except Exception as e:
        print(f"❌ Error retrieving database: {e}")
        return
    
    # Step 2: List Data Sources
    print_section("Step 2: List Data Sources")
    data_sources = database.get("data_sources", [])
    
    if not data_sources:
        print("⚠️  No data sources found (database may be from old API version)")
        return
    
    print(f"📊 Found {len(data_sources)} data source(s):\n")
    
    for idx, ds in enumerate(data_sources, 1):
        print(f"  {idx}. {ds['name']}")
        print(f"     ID: {ds['id']}")
    
    # Step 3: Retrieve Data Source Schema
    print_section("Step 3: Retrieve Data Source Schema")
    
    for idx, ds_info in enumerate(data_sources, 1):
        data_source_id = ds_info["id"]
        data_source_name = ds_info["name"]
        
        print(f"\n📋 Data Source {idx}: {data_source_name}")
        print(f"   ID: {data_source_id}\n")
        
        try:
            data_source = client.retrieve_data_source(data_source_id)
            
            # Display properties
            properties = data_source.get("properties", {})
            print(f"   Properties ({len(properties)} total):\n")
            
            for prop_name, prop_data in properties.items():
                print(format_property_info(prop_name, prop_data))
            
            # Display parent info
            ds_parent = data_source.get("parent", {})
            ds_parent_type = ds_parent.get("type", "unknown")
            print(f"\n   📂 Parent Type: {ds_parent_type}")
            
            # Display database parent (grandparent)
            db_parent = data_source.get("database_parent", {})
            if db_parent:
                db_parent_type = db_parent.get("type", "unknown")
                print(f"   📂 Database Parent Type: {db_parent_type}")
        
        except Exception as e:
            print(f"   ❌ Error retrieving data source: {e}")
    
    # Step 4: Save to JSON
    print_section("Step 4: Export Structure to JSON")
    
    output_file = f"database_structure_{database_id[:8]}.json"
    
    try:
        structure = {
            "database": {
                "id": database["id"],
                "title": title,
                "created_time": database.get("created_time"),
                "last_edited_time": database.get("last_edited_time"),
                "parent": database.get("parent"),
                "icon": database.get("icon"),
                "cover": database.get("cover"),
            },
            "data_sources": []
        }
        
        for ds_info in data_sources:
            data_source_id = ds_info["id"]
            data_source = client.retrieve_data_source(data_source_id)
            
            structure["data_sources"].append({
                "id": data_source_id,
                "name": ds_info["name"],
                "properties": data_source.get("properties", {}),
                "parent": data_source.get("parent"),
                "database_parent": data_source.get("database_parent"),
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Structure exported to: {output_file}")
        print(f"📄 File size: {len(json.dumps(structure))} bytes")
    
    except Exception as e:
        print(f"❌ Error exporting structure: {e}")
    
    print_section("Complete!")
    print("✅ All database structure retrieved successfully!")


def main():
    """Main function."""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   Notion Database Structure Retrieval Test              ║
║   API Version: 2025-09-03                                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("This script demonstrates the new capability to retrieve")
    print("complete database structures from Notion.\n")
    
    # Get database ID from user
    database_id = input("Enter your Notion Database ID: ").strip()
    
    if not database_id:
        print("❌ No database ID provided. Exiting.")
        return
    
    # Remove any hyphens and validate length
    database_id = database_id.replace("-", "")
    if len(database_id) != 32:
        print(f"⚠️  Warning: Database ID should be 32 characters (got {len(database_id)})")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            return
    
    # Retrieve and display structure
    retrieve_and_display_structure(database_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
