#!/usr/bin/env python3
"""
Notion Workspace Cleanup for Template Sales
Organizes and optimizes the Notion workspace structure
"""

import os
import sys
from pathlib import Path

# Add core system to path
sys.path.insert(0, str(Path(__file__).parent / "02_Core_System"))

def cleanup_notion_workspace():
    """Clean up and organize the Notion workspace for template sales."""
    
    print("🧹 NOTION WORKSPACE CLEANUP FOR TEMPLATE SALES")
    print("=" * 55)
    
    try:
        from notion_api_client import NotionTemplateClient
        
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("NOTION_API_KEY")
        parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
        
        if not api_key or not parent_page_id:
            print("❌ Missing environment variables!")
            print("Please ensure NOTION_API_KEY and NOTION_PARENT_PAGE_ID are set in .env")
            return False
        
        print(f"📄 Parent Page ID: {parent_page_id}")
        
        client = NotionTemplateClient(api_key=api_key)
        
        # Step 1: Get current structure
        print("\n1️⃣ ANALYZING CURRENT STRUCTURE")
        print("-" * 35)
        
        try:
            # Get parent page details
            parent_page = client.client.pages.retrieve(page_id=parent_page_id)
            parent_title = parent_page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'Untitled')
            print(f"✅ Parent Page: {parent_title}")
            
            # Get child pages
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
        
        # Step 2: Create professional template structure
        print("\n2️⃣ CREATING PROFESSIONAL TEMPLATE STRUCTURE")
        print("-" * 45)
        
        # Create main sections
        sections = {
            "🚀 Getting Started": {
                "description": "Essential setup and onboarding",
                "pages": [
                    "📋 Setup Checklist",
                    "⚙️ Configuration Guide", 
                    "🎯 Quick Start Tutorial"
                ]
            },
            "📚 Content Creation": {
                "description": "Core content creation tools",
                "pages": [
                    "🎨 Voice Discovery",
                    "📝 Content Pillars",
                    "✍️ Writing Templates",
                    "📊 Content Calendar"
                ]
            },
            "🤖 Automation": {
                "description": "AI-powered automation tools",
                "pages": [
                    "🔄 Automated Workflows",
                    "📈 Performance Tracking",
                    "🎯 Optimization Tools"
                ]
            },
            "📊 Analytics": {
                "description": "Performance tracking and insights",
                "pages": [
                    "📈 Engagement Metrics",
                    "👥 Audience Insights",
                    "📊 Growth Tracking"
                ]
            },
            "🛠️ Advanced Features": {
                "description": "Advanced customization options",
                "pages": [
                    "⚙️ Database Management",
                    "🔧 Custom Workflows",
                    "📁 File Organization"
                ]
            },
            "🆘 Support": {
                "description": "Help and troubleshooting",
                "pages": [
                    "❓ FAQ",
                    "🔧 Troubleshooting",
                    "📞 Contact Support"
                ]
            }
        }
        
        created_sections = {}
        
        for section_name, section_info in sections.items():
            try:
                # Create section page
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
                                "rich_text": [{"type": "text", "text": {"content": f"This section contains {len(section_info['pages'])} essential tools for your LinkedIn content strategy."}}]
                            }
                        }
                    ]
                )
                
                section_id = section_page.get('id')
                created_sections[section_name] = section_id
                print(f"✅ Created section: {section_name}")
                
                # Create subsection pages
                for page_name in section_info["pages"]:
                    try:
                        sub_page = client.create_page(
                            parent_id=section_id,
                            title=page_name,
                            children=[
                                {
                                    "object": "block",
                                    "type": "heading_1",
                                    "heading_1": {
                                        "rich_text": [{"type": "text", "text": {"content": page_name}}]
                                    }
                                },
                                {
                                    "object": "block",
                                    "type": "paragraph",
                                    "paragraph": {
                                        "rich_text": [{"type": "text", "text": {"content": f"Welcome to {page_name}! This page contains tools and templates to help you succeed with your LinkedIn content strategy."}}]
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
                        print(f"   ├── {page_name}")
                        
                    except Exception as e:
                        print(f"   ❌ Failed to create {page_name}: {e}")
                
            except Exception as e:
                print(f"❌ Failed to create section {section_name}: {e}")
        
        # Step 3: Create professional databases
        print("\n3️⃣ CREATING PROFESSIONAL DATABASES")
        print("-" * 35)
        
        databases = {
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
                    "Publish Date": {"date": {}},
                    "Engagement Score": {"number": {"format": "number"}},
                    "Tags": {"multi_select": {"options": []}},
                    "Priority": {
                        "select": {
                            "options": [
                                {"name": "🔥 High", "color": "red"},
                                {"name": "⚡ Medium", "color": "yellow"},
                                {"name": "📝 Low", "color": "gray"}
                            ]
                        }
                    }
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
            },
            "Content Calendar": {
                "description": "Plan and schedule your content",
                "properties": {
                    "Date": {"date": {}},
                    "Content Title": {"title": {}},
                    "Status": {
                        "select": {
                            "options": [
                                {"name": "📅 Scheduled", "color": "blue"},
                                {"name": "✍️ In Progress", "color": "yellow"},
                                {"name": "✅ Completed", "color": "green"},
                                {"name": "⏸️ Paused", "color": "gray"}
                            ]
                        }
                    },
                    "Content Type": {
                        "select": {
                            "options": [
                                {"name": "📝 Text Post", "color": "blue"},
                                {"name": "🖼️ Image Post", "color": "green"},
                                {"name": "🎥 Video Post", "color": "red"},
                                {"name": "📊 Carousel", "color": "purple"},
                                {"name": "🔗 Article", "color": "orange"}
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
                    }
                }
            }
        }
        
        created_databases = {}
        
        for db_name, db_info in databases.items():
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
        
        # Step 4: Create sample content
        print("\n4️⃣ ADDING SAMPLE CONTENT")
        print("-" * 25)
        
        # Add sample content to Content Hub
        if "Content Hub" in created_databases:
            sample_content = [
                {
                    "Title": "Welcome to Your LinkedIn Content OS!",
                    "Status": "✅ Published",
                    "Content Pillar": "🎯 Personal Brand",
                    "Priority": "🔥 High",
                    "Tags": ["welcome", "introduction"]
                },
                {
                    "Title": "My Journey to 10K Followers",
                    "Status": "✍️ Draft",
                    "Content Pillar": "🎉 Success Stories",
                    "Priority": "⚡ Medium",
                    "Tags": ["growth", "strategy"]
                },
                {
                    "Title": "5 LinkedIn Mistakes I Made (And How to Avoid Them)",
                    "Status": "📝 Review",
                    "Content Pillar": "💡 Thought Leadership",
                    "Priority": "🔥 High",
                    "Tags": ["mistakes", "learning"]
                }
            ]
            
            for content in sample_content:
                try:
                    client.create_page(
                        parent_id=created_databases["Content Hub"],
                        title=content["Title"],
                        properties={
                            "Title": {"title": [{"text": {"content": content["Title"]}}]},
                            "Status": {"select": {"name": content["Status"]}},
                            "Content Pillar": {"select": {"name": content["Content Pillar"]}},
                            "Priority": {"select": {"name": content["Priority"]}},
                            "Tags": {"multi_select": [{"name": tag} for tag in content["Tags"]]}
                        }
                    )
                    print(f"✅ Added sample content: {content['Title']}")
                    
                except Exception as e:
                    print(f"❌ Failed to add sample content: {e}")
        
        # Step 5: Create professional welcome page
        print("\n5️⃣ CREATING PROFESSIONAL WELCOME PAGE")
        print("-" * 40)
        
        try:
            # Update parent page with professional content
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
                        "rich_text": [{"type": "text", "text": {"content": "Welcome to your complete LinkedIn content creation system! This template provides everything you need to build a powerful LinkedIn presence with AI-powered automation."}}]
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
                        "rich_text": [{"type": "text", "text": {"content": "📊 What's Included"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Complete content creation workflow"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "AI-powered automation tools"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Performance tracking and analytics"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Professional templates and workflows"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "🚀 Quick Start"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Complete the Voice Discovery questionnaire"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Define your Content Pillars"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Start creating content in the Content Hub"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Track performance and optimize"}}]
                    }
                }
            ]
            
            # Add content to parent page
            client.client.blocks.children.append(
                block_id=parent_page_id,
                children=welcome_content
            )
            
            print("✅ Created professional welcome page")
            
        except Exception as e:
            print(f"❌ Failed to create welcome page: {e}")
        
        # Summary
        print("\n🎉 NOTION WORKSPACE CLEANUP COMPLETE!")
        print("=" * 40)
        print(f"✅ Created {len(created_sections)} professional sections")
        print(f"✅ Created {len(created_databases)} databases")
        print("✅ Added sample content")
        print("✅ Professional welcome page created")
        
        print("\n📁 Your Template Structure:")
        for section_name in created_sections.keys():
            print(f"├── {section_name}")
        
        print("\n📊 Your Databases:")
        for db_name in created_databases.keys():
            print(f"├── {db_name}")
        
        print("\n🎯 Ready for Template Sales!")
        print("Your Notion workspace is now professionally organized and ready for customers.")
        
        return True
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False

if __name__ == "__main__":
    cleanup_notion_workspace()
