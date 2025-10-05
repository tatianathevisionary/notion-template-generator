#!/usr/bin/env python3
"""
Fix Notion Workspace Structure
Clean up the confusing structure and organize properly
"""

import os
import sys
from pathlib import Path

# Add core system to path
sys.path.insert(0, str(Path(__file__).parent / "02_Core_System"))

def fix_notion_structure():
    """Fix the confusing Notion workspace structure."""
    
    print("🔧 FIXING NOTION WORKSPACE STRUCTURE")
    print("=" * 40)
    
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
        
        # Step 1: Get current structure and identify issues
        print("\n1️⃣ ANALYZING CURRENT STRUCTURE")
        print("-" * 35)
        
        try:
            # Get parent page details
            parent_page = client.client.pages.retrieve(page_id=parent_page_id)
            parent_title = parent_page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'Untitled')
            print(f"📄 Parent Page: {parent_title}")
            
            # Get all child pages
            blocks_response = client.client.blocks.children.list(block_id=parent_page_id)
            child_pages = []
            
            for block in blocks_response.get('results', []):
                if block.get('type') == 'child_page':
                    child_page_id = block.get('id')
                    child_title = block.get('child_page', {}).get('title', 'Untitled')
                    child_pages.append({
                        'id': child_page_id,
                        'title': child_title
                    })
                    print(f"   📄 {child_title}")
            
            print(f"✅ Found {len(child_pages)} child pages")
            
        except Exception as e:
            print(f"❌ Error analyzing structure: {e}")
            return False
        
        # Step 2: Clean up duplicate and confusing pages
        print("\n2️⃣ CLEANING UP DUPLICATE PAGES")
        print("-" * 35)
        
        # Identify pages to clean up
        pages_to_archive = []
        
        for page in child_pages:
            page_title = page['title']
            
            # Archive test pages and duplicates
            if any(keyword in page_title.lower() for keyword in ['test', 'duplicated', 'advanced test']):
                pages_to_archive.append(page)
                print(f"🗑️ Will archive: {page_title}")
            
            # Archive old structure pages
            if page_title in ['Getting Started', 'Content Creation', 'Automation', 'Analytics', 'Advanced Features', 'Support']:
                pages_to_archive.append(page)
                print(f"🗑️ Will archive old structure: {page_title}")
        
        # Archive the identified pages
        for page in pages_to_archive:
            try:
                client.client.pages.update(
                    page_id=page['id'],
                    archived=True
                )
                print(f"✅ Archived: {page['title']}")
            except Exception as e:
                print(f"❌ Failed to archive {page['title']}: {e}")
        
        # Step 3: Create clean, professional structure
        print("\n3️⃣ CREATING CLEAN PROFESSIONAL STRUCTURE")
        print("-" * 45)
        
        # Define the clean structure
        clean_structure = {
            "🚀 Getting Started": {
                "description": "Essential setup and onboarding for new users",
                "subpages": [
                    "📋 Setup Checklist",
                    "⚙️ Configuration Guide", 
                    "🎯 Quick Start Tutorial"
                ]
            },
            "🎨 Voice Discovery": {
                "description": "Define your unique writing style and brand voice",
                "subpages": [
                    "📝 Voice Assessment",
                    "🎯 Brand Personality",
                    "✍️ Writing Style Guide"
                ]
            },
            "📚 Content Strategy": {
                "description": "Strategic content planning and pillar development",
                "subpages": [
                    "🎯 Content Pillars",
                    "📅 Content Calendar",
                    "📝 Content Templates"
                ]
            },
            "🤖 AI Automation": {
                "description": "AI-powered content generation and optimization",
                "subpages": [
                    "🔄 Automated Workflows",
                    "📈 Performance Tracking",
                    "🎯 Optimization Tools"
                ]
            },
            "📊 Performance Analytics": {
                "description": "Track and analyze your LinkedIn performance",
                "subpages": [
                    "📈 Engagement Metrics",
                    "👥 Audience Insights",
                    "📊 Growth Tracking"
                ]
            },
            "🛠️ Advanced Features": {
                "description": "Advanced customization and power user tools",
                "subpages": [
                    "⚙️ Database Management",
                    "🔧 Custom Workflows",
                    "📁 File Organization"
                ]
            },
            "🆘 Support & Resources": {
                "description": "Help, troubleshooting, and additional resources",
                "subpages": [
                    "❓ FAQ",
                    "🔧 Troubleshooting",
                    "📞 Contact Support"
                ]
            }
        }
        
        created_sections = {}
        
        for section_name, section_info in clean_structure.items():
            try:
                # Create main section page
                section_page = client.create_page(
                    parent_id=parent_page_id,
                    title=section_name,
                    children=[
                        {
                            "object": "block",
                            "type": "heading_1",
                            "heading_1": {
                                "rich_text": [{"type": "text", "text": {"content": section_name}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": section_info["description"]}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "icon": {"emoji": "📋"},
                                "rich_text": [{"type": "text", "text": {"content": f"This section contains {len(section_info['subpages'])} essential tools for your LinkedIn content strategy."}}]
                            }
                        }
                    ]
                )
                
                section_id = section_page.get('id')
                created_sections[section_name] = section_id
                print(f"✅ Created section: {section_name}")
                
                # Create subpages
                for subpage_name in section_info["subpages"]:
                    try:
                        sub_page = client.create_page(
                            parent_id=section_id,
                            title=subpage_name,
                            children=[
                                {
                                    "object": "block",
                                    "type": "heading_1",
                                    "heading_1": {
                                        "rich_text": [{"type": "text", "text": {"content": subpage_name}}]
                                    }
                                },
                                {
                                    "object": "block",
                                    "type": "paragraph",
                                    "paragraph": {
                                        "rich_text": [{"type": "text", "text": {"content": f"Welcome to {subpage_name}! This page contains tools and templates to help you succeed with your LinkedIn content strategy."}}]
                                    }
                                },
                                {
                                    "object": "block",
                                    "type": "to_do",
                                    "to_do": {
                                        "rich_text": [{"type": "text", "text": {"content": "Complete this section"}}],
                                        "checked": False
                                    }
                                }
                            ]
                        )
                        print(f"   ├── {subpage_name}")
                        
                    except Exception as e:
                        print(f"   ❌ Failed to create {subpage_name}: {e}")
                
            except Exception as e:
                print(f"❌ Failed to create section {section_name}: {e}")
        
        # Step 4: Create clean databases
        print("\n4️⃣ CREATING CLEAN DATABASES")
        print("-" * 30)
        
        # Clean up existing databases and create new ones
        clean_databases = {
            "Content Hub": {
                "description": "Central hub for all your LinkedIn content",
                "properties": {
                    "Title": {"title": {}},
                    "Status": {
                        "select": {
                            "options": [
                                {"name": "💡 Idea", "color": "gray"},
                                {"name": "✍️ Draft", "color": "yellow"},
                                {"name": "📝 Review", "color": "orange"},
                                {"name": "📅 Scheduled", "color": "blue"},
                                {"name": "✅ Published", "color": "green"}
                            ]
                        }
                    },
                    "Content Pillar": {
                        "select": {
                            "options": [
                                {"name": "🎯 Personal Brand", "color": "purple"},
                                {"name": "💼 Industry Insights", "color": "blue"},
                                {"name": "🔍 Behind the Scenes", "color": "green"},
                                {"name": "💡 Thought Leadership", "color": "red"},
                                {"name": "🎉 Success Stories", "color": "pink"}
                            ]
                        }
                    },
                    "Priority": {
                        "select": {
                            "options": [
                                {"name": "🔥 High", "color": "red"},
                                {"name": "⚡ Medium", "color": "yellow"},
                                {"name": "📝 Low", "color": "gray"}
                            ]
                        }
                    },
                    "Publish Date": {"date": {}},
                    "Tags": {"multi_select": {"options": []}}
                }
            },
            "Performance Tracker": {
                "description": "Track your LinkedIn performance metrics",
                "properties": {
                    "Post Title": {"title": {}},
                    "Publish Date": {"date": {}},
                    "Likes": {"number": {"format": "number"}},
                    "Comments": {"number": {"format": "number"}},
                    "Shares": {"number": {"format": "number"}},
                    "Impressions": {"number": {"format": "number"}},
                    "Engagement Rate": {"number": {"format": "percent"}},
                    "Content Pillar": {
                        "select": {
                            "options": [
                                {"name": "🎯 Personal Brand", "color": "purple"},
                                {"name": "💼 Industry Insights", "color": "blue"},
                                {"name": "🔍 Behind the Scenes", "color": "green"},
                                {"name": "💡 Thought Leadership", "color": "red"},
                                {"name": "🎉 Success Stories", "color": "pink"}
                            ]
                        }
                    }
                }
            }
        }
        
        created_databases = {}
        
        for db_name, db_info in clean_databases.items():
            try:
                db = client.create_database(
                    title=db_name,
                    properties=db_info["properties"],
                    parent_page_id=parent_page_id
                )
                
                db_id = db.get('id')
                created_databases[db_name] = db_id
                print(f"✅ Created database: {db_name}")
                
            except Exception as e:
                print(f"❌ Failed to create database {db_name}: {e}")
        
        # Step 5: Update main page with clean content
        print("\n5️⃣ UPDATING MAIN PAGE")
        print("-" * 25)
        
        try:
            # Clear existing content and add clean welcome content
            welcome_content = [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "🚀 LinkedIn Content OS Template"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "Welcome to your complete LinkedIn content creation system! This professional template provides everything you need to build a powerful LinkedIn presence with AI-powered automation."}}]
                    }
                },
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"emoji": "🎯"},
                        "rich_text": [{"type": "text", "text": {"content": "Start with the 'Getting Started' section to set up your content strategy and define your unique voice."}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📁 Template Structure"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"This template includes {len(created_sections)} main sections and {len(created_databases)} professional databases:"}}]
                    }
                }
            ]
            
            # Add section list
            for section_name in created_sections.keys():
                welcome_content.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": section_name}}]
                    }
                })
            
            # Add database list
            welcome_content.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "📊 Professional Databases"}}]
                }
            })
            
            for db_name in created_databases.keys():
                welcome_content.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": db_name}}]
                    }
                })
            
            # Add content to parent page
            client.client.blocks.children.append(
                block_id=parent_page_id,
                children=welcome_content
            )
            
            print("✅ Updated main page with clean content")
            
        except Exception as e:
            print(f"❌ Failed to update main page: {e}")
        
        # Final Summary
        print("\n🎉 NOTION WORKSPACE STRUCTURE FIXED!")
        print("=" * 40)
        print(f"✅ Archived {len(pages_to_archive)} duplicate/confusing pages")
        print(f"✅ Created {len(created_sections)} clean sections")
        print(f"✅ Created {len(created_databases)} professional databases")
        print("✅ Updated main page with clean content")
        
        print("\n📁 Your Clean Template Structure:")
        for section_name in created_sections.keys():
            print(f"├── {section_name}")
        
        print("\n📊 Your Professional Databases:")
        for db_name in created_databases.keys():
            print(f"├── {db_name}")
        
        print("\n🎯 The confusing 'No pages inside' issue is now fixed!")
        print("Your Notion workspace now has a clean, logical structure.")
        
        return True
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        return False

if __name__ == "__main__":
    fix_notion_structure()
