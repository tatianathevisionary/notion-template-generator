"""
LinkedIn Content OS - Notion Template Generator

Creates a complete LinkedIn Content creation system in Notion with:
1. Content Hub (Main database for posts)
2. Content Pillars (Strategic topics)
3. Voice Discovery (Persona & tone definition)
4. Prompt Library (AI prompts collection)
5. Weekly Review (Analytics & progress)
"""

import json
import os
from typing import Dict, Any
from notion_api_client import NotionTemplateClient
from notion_api_client import (
    heading_1, heading_2, heading_3, paragraph, bullet_list_item, numbered_list_item,
    to_do, toggle, callout, quote, code, table_of_contents, divider, bookmark
)


def create_content_hub(client: NotionTemplateClient) -> str:
    """
    Create the Content Hub database - the heart of the LinkedIn Content OS.
    
    Returns:
        Database ID of the created Content Hub
    """
    print("\n📝 Creating Content Hub...")
    
    # Define database properties
    properties = {
        "Post Idea": {
            "title": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "💡 Idea", "color": "gray"},
                    {"name": "✍️ Drafting", "color": "yellow"},
                    {"name": "👀 For Review", "color": "blue"},
                    {"name": "✅ Approved", "color": "green"},
                    {"name": "🚀 Published", "color": "purple"},
                    {"name": "📊 Analyzing", "color": "pink"}
                ]
            }
        },
        "Content Pillar": {
            "select": {
                "options": [
                    {"name": "AI for Entrepreneurs", "color": "blue"},
                    {"name": "Personal Brand", "color": "purple"},
                    {"name": "Product Management", "color": "orange"},
                    {"name": "Creator Economy", "color": "green"},
                    {"name": "Lessons Learned", "color": "pink"}
                ]
            }
        },
        "Draft": {
            "rich_text": {}
        },
        "Approved": {
            "checkbox": {}
        },
        "Publish Date": {
            "date": {}
        },
        "Engagement": {
            "number": {
                "format": "number"
            }
        },
        "Hook Type": {
            "select": {
                "options": [
                    {"name": "Story", "color": "blue"},
                    {"name": "Contrarian", "color": "red"},
                    {"name": "Question", "color": "yellow"},
                    {"name": "Statistic", "color": "green"},
                    {"name": "Pain Point", "color": "orange"}
                ]
            }
        },
        "Created": {
            "created_time": {}
        }
    }
    
    # Create database
    database = client.create_database(
        title="📝 Content Hub",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add comprehensive sample post
    print("  ✍️ Adding sample post...")
    page_properties = {
        "Post Idea": {
            "title": [{"type": "text", "text": {"content": "Example: Why AI Won't Replace You (But AI-Powered Creators Will)"}}]
        },
        "Status": {
            "select": {"name": "✅ Approved"}
        },
        "Content Pillar": {
            "select": {"name": "AI for Entrepreneurs"}
        },
        "Approved": {
            "checkbox": True
        },
        "Publish Date": {
            "date": {"start": "2025-10-10"}
        },
        "Hook Type": {
            "select": {"name": "Contrarian"}
        },
        "Engagement": {
            "number": 0
        }
    }
    
    # Rich text content for the post
    page_content = [
        table_of_contents(),
        divider(),
        
        # Main Overview
        heading_1("📝 Content Hub - Your Command Center", color="blue_background"),
        
        callout(
            "This is your central dashboard for ALL LinkedIn content. "
            "From ideation to publishing, everything flows through here.",
            icon="🎯",
            color="purple_background"
        ),
        
        divider(),
        
        # The Post Draft Section
        heading_2("✍️ Draft Content", color="blue_background"),
        paragraph("Here's your AI-generated (or manually written) post draft:"),
        
        quote(
            "Why AI Won't Replace You (But AI-Powered Creators Will)\n\n"
            "I see this debate everywhere:\n"
            "\"Will AI replace content creators?\"\n\n"
            "Wrong question.\n\n"
            "AI won't replace you.\n"
            "But creators who use AI will replace creators who don't.\n\n"
            "Here's why:\n\n"
            "1. AI removes the blank page problem\n"
            "2. AI handles research in seconds\n"
            "3. AI helps you post consistently\n\n"
            "But AI can't:\n"
            "→ Tell YOUR stories\n"
            "→ Have YOUR experiences\n"
            "→ Build YOUR relationships\n\n"
            "The future belongs to creators who use AI as their co-pilot, not their replacement.\n\n"
            "Are you using AI to accelerate your content? Or are you still doing everything manually?"
        ),
        
        divider(),
        
        # Hook Analysis
        heading_2("🎣 Hook Breakdown", color="orange_background"),
        callout(
            "Hook Type: Contrarian Opinion\n"
            "Why it works: Challenges a common assumption and reframes the debate",
            icon="✨",
            color="yellow_background"
        ),
        
        heading_3("Strong Elements:"),
        bullet_list_item("Opens with a question everyone's asking"),
        bullet_list_item("Immediately takes a contrarian stance"),
        bullet_list_item("Uses pattern interrupt: 'Wrong question'"),
        bullet_list_item("Provides clear value in numbered list"),
        bullet_list_item("Ends with engagement question"),
        
        divider(),
        
        # Content Structure
        heading_2("📐 Post Structure Analysis", color="purple_background"),
        
        heading_3("1. The Hook (First 2 lines)"),
        code(
            "\"Why AI Won't Replace You (But AI-Powered Creators Will)\"\n"
            "\"I see this debate everywhere:\"",
            language="markdown"
        ),
        paragraph("→ Scroll-stopping headline + relatable setup"),
        
        heading_3("2. The Twist"),
        paragraph("\"Wrong question.\" ← Pattern interrupt that forces re-engagement"),
        
        heading_3("3. The Reframe"),
        paragraph("New perspective: It's not AI vs. humans, it's AI-enabled vs. manual"),
        
        heading_3("4. The Value"),
        numbered_list_item("AI removes the blank page problem"),
        numbered_list_item("AI handles research in seconds"),
        numbered_list_item("AI helps you post consistently"),
        
        heading_3("5. The Call-to-Action"),
        paragraph("Ends with an engaging question to spark conversation"),
        
        divider(),
        
        # Optimization Tips
        heading_2("🎯 Optimization Checklist", color="green_background"),
        
        to_do("Check hook strength (does it stop the scroll?)", checked=True),
        to_do("Ensure value delivery in first 3 lines", checked=True),
        to_do("Add personal story or data point", checked=False),
        to_do("Include clear call-to-action", checked=True),
        to_do("Keep paragraphs short (2-3 lines max)", checked=True),
        to_do("Add strategic line breaks for readability", checked=True),
        to_do("End with engagement question", checked=True),
        
        divider(),
        
        # Publishing Workflow
        heading_2("🚀 Publishing Workflow", color="blue_background"),
        
        callout(
            "Follow this simple 3-step process:",
            icon="📋",
            color="blue_background"
        ),
        
        numbered_list_item("Review the draft above and make any edits directly in Notion"),
        numbered_list_item("Check the 'Approved' checkbox when ready"),
        numbered_list_item("Set your Publish Date - it will appear on your content calendar"),
        
        divider(),
        
        # Best Practices
        heading_2("💡 Pro Tips", color="yellow_background"),
        
        callout(
            "Best Posting Times: Tuesday-Thursday, 8-10 AM or 12-2 PM in your timezone",
            icon="⏰",
            color="gray_background"
        ),
        
        callout(
            "Engagement Hack: Respond to every comment within the first hour. "
            "LinkedIn's algorithm rewards early engagement!",
            icon="💬",
            color="green_background"
        ),
        
        callout(
            "Consistency > Perfection: Better to post 3 good posts per week than wait for 1 perfect post. "
            "Done is better than perfect!",
            icon="🔄",
            color="purple_background"
        ),
        
        divider(),
        
        # Analytics Section
        heading_2("📊 Post-Publish Actions", color="purple_background"),
        
        heading_3("Track These Metrics:"),
        bullet_list_item("Impressions (how many people saw it)"),
        bullet_list_item("Engagement rate (likes + comments / impressions)"),
        bullet_list_item("Comments (and their quality)"),
        bullet_list_item("Shares & reposts"),
        bullet_list_item("Profile views from this post"),
        
        paragraph("Add engagement numbers to the 'Engagement' property after 48 hours."),
        
        divider(),
        
        # Resources
        heading_2("📚 Helpful Resources"),
        
        toggle("Click to see related prompts and guides"),
        
        bookmark(
            "https://www.linkedin.com/help/linkedin/answer/a522735",
            "LinkedIn Best Practices Guide"
        ),
        
        divider(),
        
        # Final callout
        callout(
            "This template demonstrates the full Content Hub workflow: Draft → Review → Approve → Schedule → Publish → Analyze. "
            "Use this structure for every post to build a consistent, high-quality content habit!",
            icon="🎉",
            color="blue_background"
        )
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def create_content_pillars(client: NotionTemplateClient) -> str:
    """
    Create the Content Pillars database for strategic topic planning.
    
    Returns:
        Database ID of the created Content Pillars database
    """
    print("\n🎯 Creating Content Pillars...")
    
    properties = {
        "Pillar Name": {
            "title": {}
        },
        "Description": {
            "rich_text": {}
        },
        "Target Audience": {
            "rich_text": {}
        },
        "Post Frequency": {
            "select": {
                "options": [
                    {"name": "Daily", "color": "red"},
                    {"name": "3x per week", "color": "orange"},
                    {"name": "2x per week", "color": "yellow"},
                    {"name": "Weekly", "color": "green"},
                    {"name": "Bi-weekly", "color": "blue"}
                ]
            }
        },
        "Posts Created": {
            "number": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Active", "color": "green"},
                    {"name": "Planning", "color": "yellow"},
                    {"name": "Paused", "color": "gray"}
                ]
            }
        }
    }
    
    database = client.create_database(
        title="🎯 Content Pillars",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add sample pillar
    print("  📝 Adding sample content pillar...")
    page_properties = {
        "Pillar Name": {
            "title": [{"type": "text", "text": {"content": "AI for Entrepreneurs"}}]
        },
        "Description": {
            "rich_text": [{"type": "text", "text": {"content": "How entrepreneurs can leverage AI tools to scale their business"}}]
        },
        "Target Audience": {
            "rich_text": [{"type": "text", "text": {"content": "Solo founders, startup teams, creators building businesses"}}]
        },
        "Post Frequency": {
            "select": {"name": "3x per week"}
        },
        "Status": {
            "select": {"name": "Active"}
        },
        "Posts Created": {
            "number": 0
        }
    }
    
    page_content = [
        heading_1("🎯 Content Pillar Strategy", color="purple_background"),
        
        callout(
            "Content pillars are the 3-5 core topics you'll become known for on LinkedIn. "
            "They guide your content strategy and help you build authority in specific areas.",
            icon="🎯",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("📋 Pillar Overview: AI for Entrepreneurs"),
        
        paragraph("This pillar focuses on practical AI applications for business builders."),
        
        heading_3("Target Audience:"),
        bullet_list_item("Solo founders building tech products"),
        bullet_list_item("Startup teams (2-10 people)"),
        bullet_list_item("Creators monetizing their expertise"),
        bullet_list_item("Consultants & freelancers"),
        
        divider(),
        
        heading_2("💡 Content Ideas for This Pillar"),
        
        heading_3("AI Tools & Workflows:"),
        numbered_list_item("How to use ChatGPT for customer research"),
        numbered_list_item("AI-powered email automation for sales"),
        numbered_list_item("Building MVPs with AI coding assistants"),
        numbered_list_item("Content creation workflows with AI"),
        
        heading_3("Success Stories & Case Studies:"),
        numbered_list_item("How I saved 10 hours/week with AI"),
        numbered_list_item("$10K → $50K MRR using AI tools"),
        numbered_list_item("AI mistakes that cost me time (and how to avoid them)"),
        
        heading_3("Frameworks & Strategies:"),
        numbered_list_item("The AI-First Business Stack"),
        numbered_list_item("When to use AI vs. hire humans"),
        numbered_list_item("ROI calculator for AI tools"),
        
        divider(),
        
        heading_2("📊 Success Metrics"),
        
        to_do("Post at least 3x per week on this pillar"),
        to_do("Track engagement rate (target: 3-5%)"),
        to_do("Monitor follower growth from this topic"),
        to_do("Collect testimonials from people you've helped"),
        
        divider(),
        
        heading_2("🎨 Voice & Tone for This Pillar"),
        
        callout(
            "Practical, no-BS, results-focused. Share real examples with numbers. "
            "Be honest about failures. Position AI as a tool, not magic.",
            icon="🗣️",
            color="blue_background"
        ),
        
        divider(),
        
        callout(
            "Pro Tip: Review this pillar monthly. Are you staying on topic? "
            "Is your audience engaging? Adjust based on what resonates!",
            icon="💡",
            color="yellow_background"
        )
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def create_voice_discovery(client: NotionTemplateClient) -> str:
    """
    Create the Voice Discovery database - interactive workbook for defining voice.
    
    Returns:
        Database ID of the created Voice Discovery database
    """
    print("\n🎤 Creating Voice Discovery Module...")
    
    properties = {
        "Section": {
            "title": {}
        },
        "Completed": {
            "checkbox": {}
        },
        "Notes": {
            "rich_text": {}
        }
    }
    
    database = client.create_database(
        title="🎤 Voice Discovery",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add comprehensive voice discovery worksheet
    print("  📝 Adding voice discovery worksheet...")
    page_properties = {
        "Section": {
            "title": [{"type": "text", "text": {"content": "Complete Voice Profile"}}]
        },
        "Completed": {
            "checkbox": False
        }
    }
    
    page_content = [
        table_of_contents(),
        divider(),
        
        heading_1("🎤 Discover Your Authentic Voice", color="purple_background"),
        
        callout(
            "Your voice is what makes you YOU. It's not about being perfect—it's about being authentic. "
            "Complete this worksheet to define your unique LinkedIn presence.",
            icon="✨",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("1. Voice Adjectives", color="blue_background"),
        
        paragraph("Choose 3-5 adjectives that describe how you want to sound:"),
        
        heading_3("Common Voice Styles:"),
        bullet_list_item("🔥 Bold & Provocative - Challenge conventions, strong opinions"),
        bullet_list_item("💡 Helpful & Educational - Teacher energy, step-by-step guides"),
        bullet_list_item("😊 Friendly & Conversational - Like talking to a friend"),
        bullet_list_item("📊 Data-Driven & Analytical - Numbers, research, logic"),
        bullet_list_item("🎭 Story-Driven & Personal - Share experiences, vulnerable"),
        
        divider(),
        
        heading_3("✍️ Your Turn: My Voice Is..."),
        
        toggle("Fill this out: I sound _____, _____, and _____"),
        
        paragraph("Example: 'I sound practical, no-BS, and results-focused'"),
        
        callout(
            "Write your 3-5 adjectives here:",
            icon="✏️",
            color="gray_background"
        ),
        
        divider(),
        
        heading_2("2. Audience Definition", color="orange_background"),
        
        paragraph("Who are you talking to? Get specific!"),
        
        heading_3("Answer These Questions:"),
        
        numbered_list_item("What's their job title or role?"),
        numbered_list_item("What's their biggest daily frustration?"),
        numbered_list_item("What transformation are they seeking?"),
        numbered_list_item("What do they believe that's wrong?"),
        numbered_list_item("What do they need to hear from you?"),
        
        divider(),
        
        callout(
            "Example Audience Profile:\n\n"
            "\"I'm talking to solo founders (under $100K revenue) who are drowning in manual tasks "
            "and believe they need to hire a team to scale. They need to hear that AI can be their "
            "first 'hire' and save them 20+ hours per week.\"",
            icon="🎯",
            color="blue_background"
        ),
        
        divider(),
        
        heading_2("3. Content Pillar Brainstorm", color="green_background"),
        
        paragraph("What 3-5 topics will you become known for?"),
        
        callout(
            "Formula: Your Expertise × Your Audience's Pain Points = Your Pillars",
            icon="📐",
            color="yellow_background"
        ),
        
        heading_3("Brainstorming Questions:"),
        bullet_list_item("What do people always ask you about?"),
        bullet_list_item("What problems have you solved that others struggle with?"),
        bullet_list_item("What topics could you talk about for hours?"),
        bullet_list_item("What unique combination of skills do you have?"),
        
        divider(),
        
        heading_3("🎯 Your Content Pillars:"),
        
        numbered_list_item("Pillar 1: _____________________"),
        numbered_list_item("Pillar 2: _____________________"),
        numbered_list_item("Pillar 3: _____________________"),
        numbered_list_item("Pillar 4: _____________________ (optional)"),
        numbered_list_item("Pillar 5: _____________________ (optional)"),
        
        divider(),
        
        heading_2("4. Personal Vocabulary & Phrases", color="purple_background"),
        
        paragraph("What words, phrases, or frameworks are uniquely YOURS?"),
        
        heading_3("Examples:"),
        bullet_list_item("Gary Vee: 'Document, don't create'"),
        bullet_list_item("Naval: 'Specific knowledge'"),
        bullet_list_item("Tim Ferriss: 'What would this look like if it were easy?'"),
        
        heading_3("✍️ Your Signature Phrases:"),
        
        callout(
            "List phrases you use often, or create new ones:",
            icon="💬",
            color="gray_background"
        ),
        
        divider(),
        
        heading_2("5. Do's and Don'ts", color="red_background"),
        
        heading_3("I DO Sound Like:"),
        bullet_list_item("Example: Direct and to the point"),
        bullet_list_item("Example: Sharing real numbers and results"),
        bullet_list_item("Example: Admitting when I don't know something"),
        
        heading_3("I DON'T Sound Like:"),
        bullet_list_item("Example: Corporate jargon and buzzwords"),
        bullet_list_item("Example: Overly salesy or pushy"),
        bullet_list_item("Example: Fake guru promising overnight success"),
        
        divider(),
        
        heading_2("6. Tone Examples", color="blue_background"),
        
        paragraph("Let's see your voice in action! Rewrite this boring sentence in YOUR voice:"),
        
        quote("Original: 'Time management is important for productivity.'"),
        
        heading_3("Your Version:"),
        
        callout(
            "Rewrite it here in your authentic voice...",
            icon="✏️",
            color="gray_background"
        ),
        
        paragraph("Examples in different voices:"),
        bullet_list_item("Bold: 'Time management is BS. Energy management is everything.'"),
        bullet_list_item("Helpful: 'Here's the 3-step system I use to get 2x more done in half the time...'"),
        bullet_list_item("Data-driven: 'Studies show that 93% of productivity gains come from eliminating, not optimizing.'"),
        
        divider(),
        
        heading_2("✅ Action Steps", color="green_background"),
        
        to_do("Complete all 6 sections above"),
        to_do("Write your first post using your defined voice"),
        to_do("Ask 3 people: 'Does this sound like me?'"),
        to_do("Refine based on feedback"),
        to_do("Save your voice profile to reference before writing"),
        
        divider(),
        
        callout(
            "Remember: Your voice will evolve! Come back to this worksheet every 3 months "
            "and update it. Authenticity beats perfection every time.",
            icon="🎉",
            color="purple_background"
        )
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def main():
    """
    Main function to create the LinkedIn Content OS.
    """
    print("=" * 60)
    print("🚀 LINKEDIN CONTENT OS - NOTION GENERATOR")
    print("=" * 60)
    print("Creating your complete content creation system...\n")
    
    try:
        # Initialize Notion client
        client = NotionTemplateClient()
        
        # Create all databases
        content_hub_id = create_content_hub(client)
        pillars_id = create_content_pillars(client)
        voice_id = create_voice_discovery(client)
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ LINKEDIN CONTENT OS CREATED!")
        print("=" * 60)
        print("\n📊 Created Databases:")
        print(f"  • Content Hub: {content_hub_id}")
        print(f"  • Content Pillars: {pillars_id}")
        print(f"  • Voice Discovery: {voice_id}")
        print("\n🔗 Visit your Notion workspace to see your new system!")
        print("\n💡 Next Steps:")
        print("  1. Complete the Voice Discovery worksheet")
        print("  2. Define your 3-5 Content Pillars")
        print("  3. Start creating posts in the Content Hub!")
        
    except Exception as e:
        print(f"\n❌ Error during creation: {e}")
        raise


if __name__ == "__main__":
    main()
