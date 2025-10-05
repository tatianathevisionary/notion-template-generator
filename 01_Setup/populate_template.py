#!/usr/bin/env python3
"""
LinkedIn Content OS Template - Population Script
Populates Notion workspace with the complete template
"""

import os
import sys
from pathlib import Path

# Add core system to path
sys.path.insert(0, str(Path(__file__).parent.parent / "02_Core_System"))

def main():
    print("🚀 LinkedIn Content OS Template Population")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Please run setup.py first to create your configuration.")
        sys.exit(1)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("NOTION_API_KEY")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    
    if not api_key or not parent_page_id:
        print("❌ Missing required environment variables!")
        print("Please check your .env file and ensure NOTION_API_KEY and NOTION_PARENT_PAGE_ID are set.")
        sys.exit(1)
    
    print("✅ Environment variables loaded")
    print(f"📄 Parent Page ID: {parent_page_id}")
    
    try:
        # Import the core system
        from notion_api_client import NotionTemplateClient
        
        print("🔧 Initializing Notion client...")
        client = NotionTemplateClient(api_key=api_key)
        
        print("📊 Creating template structure...")
        
        # Create main welcome page
        welcome_page = client.create_page(
            parent_id=parent_page_id,
            title="🚀 LinkedIn Content OS - Welcome",
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "Welcome to Your LinkedIn Content OS!"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "This is your complete LinkedIn content creation system. Follow the steps below to get started."}}]
                    }
                },
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"emoji": "🎯"},
                        "rich_text": [{"type": "text", "text": {"content": "Start with Voice Discovery to define your unique content style and tone."}}]
                    }
                }
            ]
        )
        
        print(f"✅ Created welcome page: {welcome_page.get('id')}")
        
        # Create voice discovery page
        voice_discovery = client.create_page(
            parent_id=welcome_page.get('id'),
            title="📚 Day 1: Foundation",
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "Voice Discovery"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "Define your unique writing voice, tone, and persona. This foundation will guide all your content creation."}}]
                    }
                }
            ]
        )
        
        print(f"✅ Created voice discovery page: {voice_discovery.get('id')}")
        
        # Create content pillars page
        content_pillars = client.create_page(
            parent_id=welcome_page.get('id'),
            title="📚 Day 2: Voice Discovery",
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "Content Pillars"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "Define your 3-5 main content themes. These pillars will guide your content strategy and ensure consistency."}}]
                    }
                }
            ]
        )
        
        print(f"✅ Created content pillars page: {content_pillars.get('id')}")
        
        # Create content hub database
        content_hub_properties = {
            "Title": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "gray"},
                        {"name": "Review", "color": "yellow"},
                        {"name": "Scheduled", "color": "blue"},
                        {"name": "Published", "color": "green"}
                    ]
                }
            },
            "Content Pillar": {
                "select": {
                    "options": [
                        {"name": "Personal Brand", "color": "purple"},
                        {"name": "Industry Insights", "color": "blue"},
                        {"name": "Behind the Scenes", "color": "green"},
                        {"name": "Thought Leadership", "color": "red"}
                    ]
                }
            },
            "Publish Date": {"date": {}},
            "Engagement": {"number": {"format": "number"}},
            "Tags": {"multi_select": {"options": []}}
        }
        
        content_hub = client.create_database(
            title="Content Hub",
            properties=content_hub_properties,
            parent_page_id=parent_page_id
        )
        
        print(f"✅ Created content hub database: {content_hub.get('id')}")
        
        print("\n🎉 Template population complete!")
        print("=" * 35)
        print("✅ Welcome page created")
        print("✅ Voice discovery setup")
        print("✅ Content pillars configured")
        print("✅ Content hub database ready")
        
        print("\n📚 Next Steps:")
        print("1. Complete the voice discovery questionnaire")
        print("2. Define your content pillars")
        print("3. Start creating content in the Content Hub")
        print("4. Schedule and track your posts")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")
        print("Please check your Notion API key and permissions.")
        sys.exit(1)

if __name__ == "__main__":
    main()
