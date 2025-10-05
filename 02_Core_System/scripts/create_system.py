#!/usr/bin/env python3
"""
Create LinkedIn Content OS in Notion using MCP tools
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, '.')

from tools import create_notion_database
from notion_api_client import NotionTemplateClient

print("="*70)
print("  🚀 Creating LinkedIn Content OS in Notion")
print("="*70)

parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
created_databases = []

# Database 1: Content Hub (Main Database)
print("\n1️⃣  Creating Content Hub Database...")
print("-" * 70)

content_hub_result = create_notion_database(
    title="📝 Content Hub",
    properties={
        "Post Idea": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "💡 Idea", "color": "gray"},
                    {"name": "✍️ Drafting", "color": "yellow"},
                    {"name": "👀 For Review", "color": "orange"},
                    {"name": "✅ Approved", "color": "green"},
                    {"name": "🚀 Published", "color": "blue"}
                ]
            }
        },
        "Draft": {"rich_text": {}},
        "Approved": {"checkbox": {}},
        "Publish Date": {"date": {}},
        "Content Pillar": {
            "select": {
                "options": [
                    {"name": "Personal Story", "color": "pink"},
                    {"name": "Industry Insights", "color": "blue"},
                    {"name": "Tips & How-To", "color": "green"},
                    {"name": "Leadership", "color": "purple"},
                    {"name": "Behind the Scenes", "color": "orange"}
                ]
            }
        },
        "Engagement Score": {"number": {"format": "number"}},
        "Tags": {"multi_select": {"options": [
            {"name": "Viral Potential", "color": "red"},
            {"name": "Thought Leadership", "color": "blue"},
            {"name": "Community Building", "color": "green"}
        ]}}
    },
    icon={"type": "emoji", "emoji": "📝"}
)

if content_hub_result.get("status") == "success":
    print(f"✅ Content Hub Created!")
    print(f"   ID: {content_hub_result.get('database_id')}")
    print(f"   URL: {content_hub_result.get('url')}")
    created_databases.append(("Content Hub", content_hub_result))
else:
    print(f"❌ Failed: {content_hub_result.get('error')}")

# Database 2: Content Pillars
print("\n2️⃣  Creating Content Pillars Database...")
print("-" * 70)

pillars_result = create_notion_database(
    title="🎯 Content Pillars",
    properties={
        "Pillar Name": {"title": {}},
        "Description": {"rich_text": {}},
        "Target Audience": {"multi_select": {"options": [
            {"name": "Founders", "color": "blue"},
            {"name": "Content Creators", "color": "green"},
            {"name": "Product Managers", "color": "purple"},
            {"name": "Executives", "color": "red"}
        ]}},
        "Post Frequency": {
            "select": {
                "options": [
                    {"name": "Weekly", "color": "blue"},
                    {"name": "2x/Week", "color": "green"},
                    {"name": "Daily", "color": "red"}
                ]
            }
        },
        "Key Topics": {"multi_select": {"options": []}},
        "Performance": {
            "select": {
                "options": [
                    {"name": "⭐ High", "color": "green"},
                    {"name": "✅ Medium", "color": "yellow"},
                    {"name": "💤 Low", "color": "gray"}
                ]
            }
        }
    },
    icon={"type": "emoji", "emoji": "🎯"}
)

if pillars_result.get("status") == "success":
    print(f"✅ Content Pillars Created!")
    print(f"   ID: {pillars_result.get('database_id')}")
    print(f"   URL: {pillars_result.get('url')}")
    created_databases.append(("Content Pillars", pillars_result))
else:
    print(f"❌ Failed: {pillars_result.get('error')}")

# Database 3: Prompt Library
print("\n3️⃣  Creating Prompt Library Database...")
print("-" * 70)

prompts_result = create_notion_database(
    title="💡 Prompt Library",
    properties={
        "Prompt Name": {"title": {}},
        "Category": {
            "select": {
                "options": [
                    {"name": "Hook Generator", "color": "red"},
                    {"name": "Story Prompts", "color": "pink"},
                    {"name": "List Posts", "color": "blue"},
                    {"name": "Contrarian Takes", "color": "purple"},
                    {"name": "How-To Posts", "color": "green"},
                    {"name": "Engagement Hooks", "color": "orange"}
                ]
            }
        },
        "Prompt Template": {"rich_text": {}},
        "Use Case": {"rich_text": {}},
        "Example Output": {"rich_text": {}},
        "Effectiveness": {
            "select": {
                "options": [
                    {"name": "⭐⭐⭐ High", "color": "green"},
                    {"name": "⭐⭐ Medium", "color": "yellow"},
                    {"name": "⭐ Testing", "color": "gray"}
                ]
            }
        }
    },
    icon={"type": "emoji", "emoji": "💡"}
)

if prompts_result.get("status") == "success":
    print(f"✅ Prompt Library Created!")
    print(f"   ID: {prompts_result.get('database_id')}")
    print(f"   URL: {prompts_result.get('url')}")
    created_databases.append(("Prompt Library", prompts_result))
else:
    print(f"❌ Failed: {prompts_result.get('error')}")

# Database 4: Analytics & Growth
print("\n4️⃣  Creating Analytics & Growth Tracker...")
print("-" * 70)

analytics_result = create_notion_database(
    title="📈 Analytics & Growth",
    properties={
        "Week Of": {"title": {}},
        "Date": {"date": {}},
        "Follower Count": {"number": {"format": "number"}},
        "Total Impressions": {"number": {"format": "number"}},
        "Total Engagement": {"number": {"format": "number"}},
        "Engagement Rate": {"number": {"format": "percent"}},
        "Posts Published": {"number": {"format": "number"}},
        "Top Performing Post": {"rich_text": {}},
        "Key Insights": {"rich_text": {}},
        "Next Week Goals": {"rich_text": {}}
    },
    icon={"type": "emoji", "emoji": "📈"}
)

if analytics_result.get("status") == "success":
    print(f"✅ Analytics & Growth Created!")
    print(f"   ID: {analytics_result.get('database_id')}")
    print(f"   URL: {analytics_result.get('url')}")
    created_databases.append(("Analytics & Growth", analytics_result))
else:
    print(f"❌ Failed: {analytics_result.get('error')}")

# Database 5: Weekly Review Template
print("\n5️⃣  Creating Weekly Review Database...")
print("-" * 70)

review_result = create_notion_database(
    title="📊 Weekly Review",
    properties={
        "Week": {"title": {}},
        "Date Range": {"date": {}},
        "Wins This Week": {"rich_text": {}},
        "Challenges": {"rich_text": {}},
        "Top Performing Content": {"rich_text": {}},
        "Lessons Learned": {"rich_text": {}},
        "Goals for Next Week": {"rich_text": {}},
        "Energy Level": {
            "select": {
                "options": [
                    {"name": "🔥 High", "color": "red"},
                    {"name": "✅ Good", "color": "green"},
                    {"name": "😐 Medium", "color": "yellow"},
                    {"name": "😴 Low", "color": "gray"}
                ]
            }
        }
    },
    icon={"type": "emoji", "emoji": "📊"}
)

if review_result.get("status") == "success":
    print(f"✅ Weekly Review Created!")
    print(f"   ID: {review_result.get('database_id')}")
    print(f"   URL: {review_result.get('url')}")
    created_databases.append(("Weekly Review", review_result))
else:
    print(f"❌ Failed: {review_result.get('error')}")

print("\n" + "="*70)
print(f"  ✅ LinkedIn Content OS Created! ({len(created_databases)} databases)")
print("="*70)

print("\n📊 Your New Databases:\n")
for i, (name, result) in enumerate(created_databases, 1):
    print(f"{i}. {name}")
    print(f"   🔗 {result.get('url')}")
    print(f"   🆔 {result.get('database_id')}")
    print()

print("="*70)
print("🎉 READY FOR USER TESTING!")
print("="*70)
print("\nNext Steps:")
print("1. ✅ Open your databases in Notion")
print("2. ✅ Test adding content to Content Hub")
print("3. ✅ Define your first Content Pillar")
print("4. ✅ Add prompts to the Prompt Library")
print("5. ✅ Log your first weekly analytics")
print("\n💡 All databases are in your LinkedIn Content OS parent page!")

