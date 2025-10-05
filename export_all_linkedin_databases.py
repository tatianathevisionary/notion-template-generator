#!/usr/bin/env python3
"""
Export All LinkedIn Content OS Databases

Exports complete structure of all databases in the LinkedIn Content OS.
"""

from notion_api_client import NotionTemplateClient
import json
import time
from datetime import datetime

# All your database IDs
DATABASES = {
    "Content Hub": "2830da0a-a5c8-8161-8619-f6b7fe525036",
    "Content Pillars": "2830da0a-a5c8-81e9-b0c3-f34424468ef2",
    "Voice Discovery": "2830da0a-a5c8-81c3-aa05-d39ee7302302",
    "Prompt Library": "2830da0a-a5c8-8105-adab-e20090bb6046",
    "Weekly Review": "2830da0a-a5c8-8192-ad18-edbbb3a3d471"
}

def main():
    print("=" * 60)
    print("  Exporting All LinkedIn Content OS Databases")
    print("=" * 60)
    
    client = NotionTemplateClient()
    all_structures = {}
    
    for db_name, db_id in DATABASES.items():
        print(f"\n📊 Processing: {db_name}...")
        
        try:
            # Get database
            database = client.get_database(db_id)
            
            # Get data source
            data_source_id = database["data_sources"][0]["id"]
            data_source = client.retrieve_data_source(data_source_id)
            
            # Store structure
            all_structures[db_name] = {
                "database": {
                    "id": db_id,
                    "created_time": database.get("created_time"),
                    "last_edited_time": database.get("last_edited_time"),
                },
                "data_source": {
                    "id": data_source_id,
                    "properties": data_source.get("properties", {})
                }
            }
            
            print(f"   ✅ Exported {len(data_source.get('properties', {}))} properties")
            
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"linkedin_content_os_structure_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_structures, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ All structures exported to: {filename}")
    print(f"📄 Total databases: {len(all_structures)}")

if __name__ == "__main__":
    main()
