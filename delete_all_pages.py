#!/usr/bin/env python3
"""
Delete All Notion Pages
Clean up the entire workspace to start fresh
"""

import os
import sys
from pathlib import Path

# Add core system to path
sys.path.insert(0, str(Path(__file__).parent / "02_Core_System"))

def delete_all_pages():
    """Delete all pages in the Notion workspace."""
    
    print("🗑️ DELETING ALL NOTION PAGES")
    print("=" * 35)
    
    try:
        from notion_api_client import NotionTemplateClient
        
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("NOTION_API_KEY")
        parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
        
        if not api_key or not parent_page_id:
            print("❌ Missing environment variables!")
            return False
        
        client = NotionTemplateClient(api_key=api_key)
        
        # Step 1: Get all child pages
        print("\n1️⃣ FINDING ALL PAGES TO DELETE")
        print("-" * 35)
        
        try:
            blocks_response = client.client.blocks.children.list(block_id=parent_page_id)
            pages_to_delete = []
            
            for block in blocks_response.get('results', []):
                if block.get('type') == 'child_page':
                    page_id = block.get('id')
                    page_title = block.get('child_page', {}).get('title', 'Untitled')
                    pages_to_delete.append({
                        'id': page_id,
                        'title': page_title
                    })
                    print(f"📄 Found page: {page_title}")
            
            print(f"✅ Found {len(pages_to_delete)} pages to delete")
            
        except Exception as e:
            print(f"❌ Error finding pages: {e}")
            return False
        
        # Step 2: Delete all pages
        print("\n2️⃣ DELETING ALL PAGES")
        print("-" * 25)
        
        deleted_count = 0
        
        for page in pages_to_delete:
            try:
                # Archive the page (Notion doesn't allow permanent deletion via API)
                client.client.pages.update(
                    page_id=page['id'],
                    archived=True
                )
                print(f"✅ Archived: {page['title']}")
                deleted_count += 1
                
            except Exception as e:
                print(f"❌ Failed to delete {page['title']}: {e}")
        
        # Step 3: Get all databases and delete them
        print("\n3️⃣ DELETING ALL DATABASES")
        print("-" * 30)
        
        try:
            # Search for data sources (databases)
            search_response = client.client.search(
                query="",
                filter={"property": "object", "value": "data_source"}
            )
            
            databases_to_delete = []
            for ds in search_response.get('results', []):
                ds_id = ds.get('id')
                ds_name = ds.get('name', 'Untitled')
                databases_to_delete.append({
                    'id': ds_id,
                    'name': ds_name
                })
                print(f"📊 Found database: {ds_name}")
            
            print(f"✅ Found {len(databases_to_delete)} databases to delete")
            
            # Delete databases by archiving their pages
            for db in databases_to_delete:
                try:
                    # Get the database page and archive it
                    db_page = client.client.databases.retrieve(database_id=db['id'])
                    if db_page.get('id'):
                        client.client.pages.update(
                            page_id=db_page['id'],
                            archived=True
                        )
                        print(f"✅ Archived database: {db['name']}")
                        
                except Exception as e:
                    print(f"❌ Failed to delete database {db['name']}: {e}")
            
        except Exception as e:
            print(f"❌ Error finding databases: {e}")
        
        # Step 4: Clear main page content
        print("\n4️⃣ CLEARING MAIN PAGE CONTENT")
        print("-" * 35)
        
        try:
            # Get all blocks from the main page
            blocks_response = client.client.blocks.children.list(block_id=parent_page_id)
            
            # Delete all blocks except the title
            blocks_to_delete = []
            for block in blocks_response.get('results', []):
                if block.get('type') != 'child_page':  # Don't delete child pages, they're already archived
                    blocks_to_delete.append(block.get('id'))
            
            # Delete blocks
            for block_id in blocks_to_delete:
                try:
                    client.client.blocks.delete(block_id=block_id)
                    print(f"✅ Deleted block: {block_id}")
                except Exception as e:
                    print(f"❌ Failed to delete block {block_id}: {e}")
            
            print("✅ Main page content cleared")
            
        except Exception as e:
            print(f"❌ Error clearing main page: {e}")
        
        # Final Summary
        print("\n🎉 CLEANUP COMPLETE!")
        print("=" * 25)
        print(f"✅ Archived {deleted_count} pages")
        print(f"✅ Archived {len(databases_to_delete)} databases")
        print("✅ Cleared main page content")
        
        print("\n📄 Your Notion workspace is now clean!")
        print("You can now rebuild it with a proper structure.")
        
        return True
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False

if __name__ == "__main__":
    delete_all_pages()
