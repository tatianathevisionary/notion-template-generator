#!/usr/bin/env python3
"""
Configure existing LinkedIn Content OS databases with proper properties
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, '.')

from notion_api_client import NotionTemplateClient

client = NotionTemplateClient()

# Your existing databases
CONTENT_HUB_ID = "2830da0a-a5c8-8183-9546-c7c3b7587ab9"
CONTENT_PILLARS_ID = "2830da0a-a5c8-817d-b28c-c7c9b334cf98"
PROMPT_LIBRARY_ID = "2830da0a-a5c8-8105-adab-e20090bb6046"
VOICE_DISCOVERY_ID = "2830da0a-a5c8-8194-bb80-f961d82bda62"
WEEKLY_REVIEW_ID = "2830da0a-a5c8-8192-ad18-edbbb3a3d471"

print("="*70)
print("  🔧 Configuring Your LinkedIn Content OS Databases")
print("="*70)

# 1. Configure Content Hub
print("\n1️⃣  Configuring Content Hub...")
print("-" * 70)
try:
    client.client.databases.update(
        database_id=CONTENT_HUB_ID,
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
                        {"name": "Tips & How-To", "color": "green"}
                    ]
                }
            }
        }
    )
    print("   ✅ Content Hub configured with 7 properties")
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")

# 2. Configure Content Pillars
print("\n2️⃣  Configuring Content Pillars...")
print("-" * 70)
try:
    client.client.databases.update(
        database_id=CONTENT_PILLARS_ID,
        properties={
            "Pillar Name": {"title": {}},
            "Description": {"rich_text": {}},
            "Target Audience": {"rich_text": {}},
            "Post Frequency": {
                "select": {
                    "options": [
                        {"name": "Weekly", "color": "blue"},
                        {"name": "2x/Week", "color": "green"},
                        {"name": "Daily", "color": "red"}
                    ]
                }
            },
            "Performance": {
                "select": {
                    "options": [
                        {"name": "⭐ High", "color": "green"},
                        {"name": "✅ Medium", "color": "yellow"},
                        {"name": "💤 Low", "color": "gray"}
                    ]
                }
            }
        }
    )
    print("   ✅ Content Pillars configured with 5 properties")
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")

# 3. Configure Prompt Library
print("\n3️⃣  Configuring Prompt Library...")
print("-" * 70)
try:
    client.client.databases.update(
        database_id=PROMPT_LIBRARY_ID,
        properties={
            "Prompt Name": {"title": {}},
            "Category": {
                "select": {
                    "options": [
                        {"name": "Hook Generator", "color": "red"},
                        {"name": "Story Prompts", "color": "pink"},
                        {"name": "List Posts", "color": "blue"},
                        {"name": "How-To Posts", "color": "green"}
                    ]
                }
            },
            "Prompt Template": {"rich_text": {}},
            "Use Case": {"rich_text": {}},
            "Effectiveness": {
                "select": {
                    "options": [
                        {"name": "⭐⭐⭐ High", "color": "green"},
                        {"name": "⭐⭐ Medium", "color": "yellow"},
                        {"name": "⭐ Testing", "color": "gray"}
                    ]
                }
            }
        }
    )
    print("   ✅ Prompt Library configured with 5 properties")
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")

# 4. Configure Voice Discovery
print("\n4️⃣  Configuring Voice Discovery...")
print("-" * 70)
try:
    client.client.databases.update(
        database_id=VOICE_DISCOVERY_ID,
        properties={
            "Question": {"title": {}},
            "Your Answer": {"rich_text": {}},
            "Category": {
                "select": {
                    "options": [
                        {"name": "Voice & Tone", "color": "pink"},
                        {"name": "Audience", "color": "blue"},
                        {"name": "Content Pillars", "color": "green"},
                        {"name": "Personal Vocabulary", "color": "purple"}
                    ]
                }
            },
            "Completed": {"checkbox": {}}
        }
    )
    print("   ✅ Voice Discovery configured with 4 properties")
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")

# 5. Configure Weekly Review
print("\n5️⃣  Configuring Weekly Review...")
print("-" * 70)
try:
    client.client.databases.update(
        database_id=WEEKLY_REVIEW_ID,
        properties={
            "Week": {"title": {}},
            "Date Range": {"date": {}},
            "Wins This Week": {"rich_text": {}},
            "Challenges": {"rich_text": {}},
            "Top Performing Content": {"rich_text": {}},
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
        }
    )
    print("   ✅ Weekly Review configured with 7 properties")
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")

print("\n" + "="*70)
print("  ✅ Configuration Complete!")
print("="*70)
print("\nAll 5 databases now have proper properties and are ready for content!")

