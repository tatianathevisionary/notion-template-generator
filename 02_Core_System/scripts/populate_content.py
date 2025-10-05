#!/usr/bin/env python3
"""
Populate LinkedIn Content OS databases with sample content
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
print("  📝 Populating LinkedIn Content OS with Sample Content")
print("="*70)

# 1. Add Content Pillars
print("\n1️⃣  Adding Content Pillars...")
print("-" * 70)

pillars = [
    {
        "name": "Personal Story",
        "description": "Authentic stories from your journey, lessons learned, and vulnerable moments that connect with your audience",
        "audience": "Founders, Content Creators, Entrepreneurs",
        "frequency": "Weekly",
        "performance": "⭐ High"
    },
    {
        "name": "Industry Insights",
        "description": "Thought leadership content about trends, analysis, and predictions in your industry",
        "audience": "Executives, Product Managers, Business Leaders",
        "frequency": "2x/Week",
        "performance": "✅ Medium"
    },
    {
        "name": "Tips & How-To",
        "description": "Actionable advice, frameworks, and step-by-step guides that provide immediate value",
        "audience": "Content Creators, Founders, Professionals",
        "frequency": "2x/Week",
        "performance": "⭐ High"
    }
]

for pillar in pillars:
    try:
        client.client.pages.create(
            parent={"database_id": CONTENT_PILLARS_ID},
            properties={
                "Pillar Name": {"title": [{"text": {"content": pillar["name"]}}]},
                "Description": {"rich_text": [{"text": {"content": pillar["description"]}}]},
                "Target Audience": {"rich_text": [{"text": {"content": pillar["audience"]}}]},
                "Post Frequency": {"select": {"name": pillar["frequency"]}},
                "Performance": {"select": {"name": pillar["performance"]}}
            }
        )
        print(f"   ✅ Added: {pillar['name']}")
    except Exception as e:
        print(f"   ❌ Failed to add {pillar['name']}: {str(e)}")

# 2. Add Prompts
print("\n2️⃣  Adding Prompt Library...")
print("-" * 70)

prompts = [
    {
        "name": "Contrarian Opinion Hook",
        "category": "Hook Generator",
        "template": "Everyone says [common belief]. But here's what they're missing: [your contrarian take]. This is why [explanation].",
        "use_case": "Start posts that challenge conventional wisdom and spark debate",
        "effectiveness": "⭐⭐⭐ High"
    },
    {
        "name": "Personal Story Framework",
        "category": "Story Prompts",
        "template": "Context: [Set the scene]\\nChallenge: [The problem you faced]\\nChoice: [What you decided to do]\\nConsequence: [What happened]\\nLesson: [What you learned]",
        "use_case": "Share authentic experiences that resonate with your audience",
        "effectiveness": "⭐⭐⭐ High"
    },
    {
        "name": "3-Step How-To",
        "category": "How-To Posts",
        "template": "Want to [achieve result]? Here's exactly how:\\n\\n1. [Step 1 with specific action]\\n2. [Step 2 with specific action]\\n3. [Step 3 with specific action]\\n\\nBonus tip: [Additional insight]",
        "use_case": "Provide quick, actionable value that readers can implement immediately",
        "effectiveness": "⭐⭐ Medium"
    },
    {
        "name": "List Post Generator",
        "category": "List Posts",
        "template": "[Number] [things/lessons/mistakes] about [topic]:\\n\\n→ [Item 1]\\n→ [Item 2]\\n→ [Item 3]\\n\\nWhich one resonates most with you?",
        "use_case": "Create scannable, shareable content that drives engagement",
        "effectiveness": "⭐⭐⭐ High"
    }
]

for prompt in prompts:
    try:
        client.client.pages.create(
            parent={"database_id": PROMPT_LIBRARY_ID},
            properties={
                "Prompt Name": {"title": [{"text": {"content": prompt["name"]}}]},
                "Category": {"select": {"name": prompt["category"]}},
                "Prompt Template": {"rich_text": [{"text": {"content": prompt["template"]}}]},
                "Use Case": {"rich_text": [{"text": {"content": prompt["use_case"]}}]},
                "Effectiveness": {"select": {"name": prompt["effectiveness"]}}
            }
        )
        print(f"   ✅ Added: {prompt['name']}")
    except Exception as e:
        print(f"   ❌ Failed to add {prompt['name']}: {str(e)}")

# 3. Add Content Ideas
print("\n3️⃣  Adding Content Hub Ideas...")
print("-" * 70)

ideas = [
    {
        "title": "My biggest mistake as a founder (and how I fixed it)",
        "status": "💡 Idea",
        "pillar": "Personal Story",
        "draft": "",
        "approved": False
    },
    {
        "title": "5 AI tools every content creator needs in 2025",
        "status": "✍️ Drafting",
        "pillar": "Tips & How-To",
        "draft": "",
        "approved": False
    },
    {
        "title": "Why most LinkedIn advice is wrong (contrarian take)",
        "status": "👀 For Review",
        "pillar": "Industry Insights",
        "draft": "Everyone tells you to 'post daily' on LinkedIn.\\n\\nBut that's terrible advice.\\n\\nHere's why:\\n\\nQuality > Quantity\\nConsistency > Intensity\\nValue > Volume\\n\\nPost when you have something worth saying.\\nNot just to feed the algorithm.",
        "approved": False
    }
]

for idea in ideas:
    try:
        props = {
            "Post Idea": {"title": [{"text": {"content": idea["title"]}}]},
            "Status": {"select": {"name": idea["status"]}},
            "Content Pillar": {"select": {"name": idea["pillar"]}},
            "Approved": {"checkbox": idea["approved"]}
        }
        
        if idea["draft"]:
            props["Draft"] = {"rich_text": [{"text": {"content": idea["draft"]}}]}
        
        client.client.pages.create(
            parent={"database_id": CONTENT_HUB_ID},
            properties=props
        )
        print(f"   ✅ Added: {idea['title']}")
    except Exception as e:
        print(f"   ❌ Failed to add {idea['title']}: {str(e)}")

# 4. Add Voice Discovery Questions
print("\n4️⃣  Adding Voice Discovery Workbook...")
print("-" * 70)

questions = [
    {
        "question": "What 3 adjectives describe your authentic voice?",
        "category": "Voice & Tone",
        "answer": ""
    },
    {
        "question": "Who is your ideal reader? Describe them in detail.",
        "category": "Audience",
        "answer": ""
    },
    {
        "question": "What 3-5 topics will you be known for?",
        "category": "Content Pillars",
        "answer": ""
    },
    {
        "question": "What phrases or words do you use that are uniquely yours?",
        "category": "Personal Vocabulary",
        "answer": ""
    }
]

for q in questions:
    try:
        client.client.pages.create(
            parent={"database_id": VOICE_DISCOVERY_ID},
            properties={
                "Question": {"title": [{"text": {"content": q["question"]}}]},
                "Category": {"select": {"name": q["category"]}},
                "Your Answer": {"rich_text": [{"text": {"content": q["answer"]}}]},
                "Completed": {"checkbox": False}
            }
        )
        print(f"   ✅ Added: {q['question'][:50]}...")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")

print("\n" + "="*70)
print("  ✅ Content Population Complete!")
print("="*70)

print("\n📊 Added Sample Data:")
print("   • Content Pillars: 3 strategic pillars")
print("   • Prompt Library: 4 tested prompts")
print("   • Content Hub: 3 post ideas (different stages)")
print("   • Voice Discovery: 4 workbook questions")
print("\n🎉 Your LinkedIn Content OS is ready for user testing!")
print("\n💡 Open your databases in Notion to see all the content!")

