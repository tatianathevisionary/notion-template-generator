"""
LinkedIn Content OS - COMPLETE SYSTEM
Creates the full product bundle with:
- Dashboard/Cover Page
- 5-Day Onboarding Module  
- Content Hub
- Content Pillars
- Voice Discovery
- Prompt Library
- Weekly Review & Analytics
"""

import json
import os
from typing import Dict, Any
from notion_api_client import NotionTemplateClient
from notion_api_client import (
    heading_1, heading_2, heading_3, paragraph, bullet_list_item, numbered_list_item,
    to_do, toggle, callout, quote, code, table_of_contents, divider, bookmark
)


def create_dashboard_cover_page(client: NotionTemplateClient) -> str:
    """
    Create the main dashboard/cover page for the LinkedIn Content OS.
    
    Returns:
        Page ID of the created dashboard
    """
    print("\n🎨 Creating Dashboard Cover Page...")
    
    # Create as a regular page (not in a database)
    page_data = {
        "parent": {"page_id": client.parent_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "🚀 LinkedIn Content OS - Welcome"}}]
            }
        },
        "children": [
            # Hero Section
            heading_1("Welcome to Your LinkedIn Content OS 🚀", color="blue_background"),
            
            callout(
                "Stop guessing on LinkedIn. Start growing. This is your guided, all-in-one system "
                "to find your authentic voice, build a powerful content habit, and turn your audience into revenue.",
                icon="✨",
                color="purple_background"
            ),
            
            divider(),
            
            # Quick Stats
            heading_2("📊 Your System Includes:", color="blue_background"),
            
            bullet_list_item("✅ 5-Day Guided Onboarding (eliminate overwhelm)"),
            bullet_list_item("📝 Content Hub (manage everything from idea to publish)"),
            bullet_list_item("🎯 Content Pillars (define your 3-5 core topics)"),
            bullet_list_item("🎤 Voice Discovery (find your authentic voice)"),
            bullet_list_item("💡 Prompt Library (25+ AI prompts)"),
            bullet_list_item("📊 Weekly Review (track your growth)"),
            
            divider(),
            
            # Getting Started
            heading_2("🎯 Start Here", color="green_background"),
            
            callout(
                "New to the system? Follow this path:",
                icon="🗺️",
                color="yellow_background"
            ),
            
            numbered_list_item("📚 Read the 5-Day Onboarding (below)"),
            numbered_list_item("🎤 Complete Voice Discovery worksheet"),
            numbered_list_item("🎯 Define your 3-5 Content Pillars"),
            numbered_list_item("📝 Create your first post in Content Hub"),
            numbered_list_item("🚀 Publish and track in Weekly Review!"),
            
            divider(),
            
            # Navigation
            heading_2("🧭 Quick Navigation", color="purple_background"),
            
            heading_3("Core Databases:"),
            bullet_list_item("📝 Content Hub → Your main workspace for all posts"),
            bullet_list_item("🎯 Content Pillars → Strategic topic planning"),
            bullet_list_item("🎤 Voice Discovery → Define your unique voice"),
            bullet_list_item("💡 Prompt Library → 25+ AI prompts ready to use"),
            bullet_list_item("📊 Weekly Review → Analytics and progress tracking"),
            
            heading_3("Getting Started:"),
            bullet_list_item("📚 5-Day Onboarding → Complete this first!"),
            bullet_list_item("🎓 Video Guides → Visual walkthroughs (coming soon)"),
            bullet_list_item("🔧 Automation Setup → Connect your AI tools"),
            
            divider(),
            
            # System Benefits
            heading_2("✨ What This System Does For You", color="blue_background"),
            
            heading_3("Before:"),
            bullet_list_item("❌ Scattered ideas with no clear strategy"),
            bullet_list_item("❌ Inconsistent posting (or not posting at all)"),
            bullet_list_item("❌ Feeling overwhelmed by blank screen"),
            bullet_list_item("❌ Complex templates you abandon after a week"),
            bullet_list_item("❌ Shouting into the void with no results"),
            
            heading_3("After:"),
            bullet_list_item("✅ A calm, automated content system"),
            bullet_list_item("✅ Clear strategy with 3-5 defined pillars"),
            bullet_list_item("✅ Predictable posting schedule (3x per week)"),
            bullet_list_item("✅ AI co-pilot that sounds like YOU"),
            bullet_list_item("✅ Growing, engaged audience that sees you as an expert"),
            
            divider(),
            
            # Pro Tips
            heading_2("💡 Pro Tips for Success", color="yellow_background"),
            
            callout(
                "Consistency > Perfection: Post 3 good posts per week beats waiting for 1 perfect post. "
                "Done is better than perfect!",
                icon="🔄",
                color="blue_background"
            ),
            
            callout(
                "First Hour Matters: Respond to all comments within 60 minutes of posting. "
                "LinkedIn's algorithm rewards early engagement!",
                icon="⏰",
                color="green_background"
            ),
            
            callout(
                "Batch Create Content: Dedicate 2 hours on Friday to plan next week's content. "
                "Batch creation = less daily stress.",
                icon="📅",
                color="purple_background"
            ),
            
            divider(),
            
            # Support
            heading_2("💬 Need Help?", color="blue_background"),
            
            paragraph("Common questions:"),
            toggle("How do I start? → Begin with Day 1 of the 5-Day Onboarding below"),
            toggle("What if I don't know my voice yet? → That's what the Voice Discovery module is for!"),
            toggle("How often should I post? → Start with 3x per week, same days/times"),
            toggle("Can I use this with ChatGPT/Claude? → Yes! Works with any AI tool"),
            
            divider(),
            
            # CTA
            heading_2("🚀 Ready to Start?", color="green_background"),
            
            callout(
                "Scroll down to begin Day 1 of your onboarding, or jump directly to the Voice Discovery module if you're ready!",
                icon="🎯",
                color="purple_background"
            ),
            
            paragraph("Remember: This system is designed to be USED, not just admired. Take action, post consistently, and watch your LinkedIn presence grow! 💪"),
            
            divider(),
            divider()
        ]
    }
    
    response = client.client.pages.create(**page_data)
    print(f"✅ Successfully created dashboard page")
    return response["id"]


def create_onboarding_module(client: NotionTemplateClient, dashboard_page_id: str) -> None:
    """
    Create the 5-Day Onboarding as child pages of the dashboard.
    """
    print("\n📚 Creating 5-Day Onboarding Module...")
    
    # Day 1: Foundation
    day1_content = [
        heading_1("Day 1: The Foundation 🎯", color="blue_background"),
        
        callout(
            "Welcome! Over the next 5 days, we're building your content system together—one module at a time. "
            "No overwhelm, just focused action.",
            icon="👋",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("Today's Mission (5 minutes):", color="green_background"),
        
        paragraph("Answer this one question to set your direction:"),
        
        heading_3("What is your primary goal for using LinkedIn?"),
        
        to_do("Thought Leadership - Become known as an expert in my field"),
        to_do("Lead Generation - Attract potential clients and customers"),
        to_do("Career Opportunities - Land my next job or promotion"),
        to_do("Community Building - Connect with like-minded professionals"),
        to_do("Product/Service Promotion - Grow awareness for what I offer"),
        
        divider(),
        
        heading_2("Why This Matters", color="purple_background"),
        
        paragraph("Your goal determines everything:"),
        bullet_list_item("Content pillars you choose"),
        bullet_list_item("Voice and tone you develop"),
        bullet_list_item("Topics you focus on"),
        bullet_list_item("CTAs you use in posts"),
        
        divider(),
        
        callout(
            "Action: Check ONE box above, then come back tomorrow for Day 2!",
            icon="✅",
            color="green_background"
        ),
        
        paragraph("P.S. Don't skip ahead. Trust the process. We'll unlock each module together."),
    ]
    
    page_data = {
        "parent": {"page_id": dashboard_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "📚 Day 1: Foundation"}}]
            }
        },
        "children": day1_content
    }
    
    client.client.pages.create(**page_data)
    print("  ✅ Created Day 1: Foundation")
    
    # Day 2: Voice Discovery
    day2_content = [
        heading_1("Day 2: Discover Your Voice 🎤", color="purple_background"),
        
        callout(
            "Today, we're defining YOUR unique voice. This becomes the instruction manual for your AI co-pilot.",
            icon="✨",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("Today's Mission (10-15 minutes):", color="green_background"),
        
        paragraph("Navigate to the Voice Discovery database and complete these sections:"),
        
        numbered_list_item("Choose 3-5 adjectives that describe how you want to sound"),
        numbered_list_item("Define your target audience (be specific!)"),
        numbered_list_item("List words/phrases you love (and ones you avoid)"),
        numbered_list_item("Write your 'voice statement' in one sentence"),
        
        divider(),
        
        heading_2("Why This Matters", color="orange_background"),
        
        quote(
            "The more accurate your voice profile, the better your AI-generated content will sound like YOU. "
            "This is the foundation of authenticity at scale."
        ),
        
        divider(),
        
        heading_2("Voice Examples", color="blue_background"),
        
        heading_3("Bold & Provocative:"),
        paragraph("'Most LinkedIn advice is garbage. Here's what actually works...'"),
        
        heading_3("Helpful & Educational:"),
        paragraph("'Here's the exact 5-step framework I use to write viral LinkedIn posts...'"),
        
        heading_3("Story-Driven & Personal:"),
        paragraph("'3 years ago, I was posting daily with zero engagement. Then everything changed when...'"),
        
        divider(),
        
        callout(
            "Action: Spend 15 minutes in Voice Discovery module. Make it feel 100% YOU.",
            icon="✅",
            color="green_background"
        ),
        
        paragraph("Tomorrow: We'll use this voice to define your Content Pillars!"),
    ]
    
    page_data = {
        "parent": {"page_id": dashboard_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "📚 Day 2: Voice Discovery"}}]
            }
        },
        "children": day2_content
    }
    
    client.client.pages.create(**page_data)
    print("  ✅ Created Day 2: Voice Discovery")
    
    # Day 3: Content Pillars
    day3_content = [
        heading_1("Day 3: Define Your Content Pillars 🎯", color="blue_background"),
        
        callout(
            "Content pillars are the 3-5 core topics you'll become known for. They guide your strategy and build your authority.",
            icon="🎯",
            color="blue_background"
        ),
        
        divider(),
        
        heading_2("Today's Mission (15-20 minutes):", color="green_background"),
        
        numbered_list_item("Navigate to the Content Pillars database"),
        numbered_list_item("Create 3-5 pillar pages (use the sample as a template)"),
        numbered_list_item("For each pillar, brainstorm 10+ content ideas"),
        numbered_list_item("Set your posting frequency for each pillar"),
        
        divider(),
        
        heading_2("How to Choose Your Pillars", color="purple_background"),
        
        callout(
            "Formula: Your Expertise × Audience Pain Points × What You Love Talking About = Your Pillars",
            icon="📐",
            color="yellow_background"
        ),
        
        heading_3("Brainstorming Questions:"),
        bullet_list_item("What do people always ask you about?"),
        bullet_list_item("What problems have you solved that others struggle with?"),
        bullet_list_item("What topics could you talk about for hours without getting bored?"),
        bullet_list_item("What unique combination of skills/experiences do you have?"),
        
        divider(),
        
        heading_2("Example Pillar Combinations", color="orange_background"),
        
        heading_3("For a Startup Founder:"),
        numbered_list_item("AI Tools for Entrepreneurs"),
        numbered_list_item("Bootstrapping Strategies"),
        numbered_list_item("Product Launch Playbooks"),
        
        heading_3("For a Product Manager:"),
        numbered_list_item("Product Strategy Frameworks"),
        numbered_list_item("User Research Methods"),
        numbered_list_item("Career Growth in Tech"),
        
        divider(),
        
        callout(
            "Pro Tip: Start with 3 pillars. You can always add more later. Better to go deep on 3 than shallow on 5.",
            icon="💡",
            color="green_background"
        ),
        
        divider(),
        
        callout(
            "Action: Create your 3-5 Content Pillars today. Fill out the template for each one.",
            icon="✅",
            color="green_background"
        ),
        
        paragraph("Tomorrow: We'll write your first post!"),
    ]
    
    page_data = {
        "parent": {"page_id": dashboard_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "📚 Day 3: Content Pillars"}}]
            }
        },
        "children": day3_content
    }
    
    client.client.pages.create(**page_data)
    print("  ✅ Created Day 3: Content Pillars")
    
    # Day 4: First Post
    day4_content = [
        heading_1("Day 4: Write Your First Post ✍️", color="green_background"),
        
        callout(
            "Today's the day! We're creating your first piece of content using everything you've built so far.",
            icon="🚀",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("Today's Mission (20-30 minutes):", color="green_background"),
        
        numbered_list_item("Open the Content Hub database"),
        numbered_list_item("Click 'New' to create your first post"),
        numbered_list_item("Choose a Content Pillar and Hook Type"),
        numbered_list_item("Write or AI-generate your draft"),
        numbered_list_item("Review and refine using your voice profile"),
        
        divider(),
        
        heading_2("Post Structure Template", color="blue_background"),
        
        heading_3("The Winning Formula:"),
        
        callout(
            "Hook (1-2 lines) → Context (Why it matters) → Value (3-5 points) → CTA (Question)",
            icon="📐",
            color="yellow_background"
        ),
        
        divider(),
        
        heading_3("Example Post Breakdown:"),
        
        code(
            "Hook: 'Why AI won't replace you (but AI-powered creators will)'\n\n"
            "Context: 'I see this debate everywhere. Here's the truth...'\n\n"
            "Value:\n"
            "• AI removes blank page problem\n"
            "• AI handles research in seconds\n"
            "• AI helps you stay consistent\n\n"
            "CTA: 'Are you using AI to accelerate your content?'",
            language="markdown"
        ),
        
        divider(),
        
        heading_2("Use the Prompt Library", color="purple_background"),
        
        paragraph("Navigate to the Prompt Library and try these:"),
        
        bullet_list_item("Hook Generator: For attention-grabbing first lines"),
        bullet_list_item("Framework Post: To teach a system or process"),
        bullet_list_item("Story Post: To share personal experiences"),
        bullet_list_item("Hot Take: For contrarian opinions"),
        
        divider(),
        
        heading_2("Quality Checklist", color="orange_background"),
        
        to_do("Hook stops the scroll (does it grab attention?)"),
        to_do("Value delivered in first 3 lines"),
        to_do("Paragraphs are short (2-3 lines max)"),
        to_do("Includes personal story or data point"),
        to_do("Ends with engaging question"),
        to_do("Sounds like YOU (check against voice profile)"),
        
        divider(),
        
        callout(
            "Action: Write your first post draft today. Don't overthink it—you can always refine!",
            icon="✅",
            color="green_background"
        ),
        
        paragraph("Tomorrow: We'll schedule it and set up your posting rhythm!"),
    ]
    
    page_data = {
        "parent": {"page_id": dashboard_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "📚 Day 4: First Post"}}]
            }
        },
        "children": day4_content
    }
    
    client.client.pages.create(**page_data)
    print("  ✅ Created Day 4: First Post")
    
    # Day 5: Launch & Rhythm
    day5_content = [
        heading_1("Day 5: Launch & Build Your Rhythm 🚀", color="blue_background"),
        
        callout(
            "Congratulations! Today you'll publish your first post and set up your sustainable posting rhythm.",
            icon="🎉",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("Today's Mission:", color="green_background"),
        
        numbered_list_item("Finalize your post from yesterday"),
        numbered_list_item("Set your Publish Date in Content Hub"),
        numbered_list_item("Post it on LinkedIn!"),
        numbered_list_item("Set up your posting schedule for next 2 weeks"),
        numbered_list_item("Engage with 5 people's posts before/after posting"),
        
        divider(),
        
        heading_2("Best Posting Times", color="orange_background"),
        
        callout(
            "Tuesday-Thursday, 8-10 AM or 12-2 PM in your timezone gets highest engagement",
            icon="⏰",
            color="yellow_background"
        ),
        
        heading_3("Recommended Schedule:"),
        bullet_list_item("Monday: Batch create 3 posts for the week"),
        bullet_list_item("Tuesday, Thursday, Friday: Post at 9 AM"),
        bullet_list_item("Daily: Spend 15 min engaging with others"),
        
        divider(),
        
        heading_2("Engagement Strategy", color="purple_background"),
        
        heading_3("First Hour is Critical:"),
        numbered_list_item("Respond to every comment within 60 minutes"),
        numbered_list_item("Ask follow-up questions to encourage dialogue"),
        numbered_list_item("Tag relevant people in comments"),
        numbered_list_item("Share to your story if it's performing well"),
        
        divider(),
        
        heading_2("Track Your Results", color="blue_background"),
        
        paragraph("After 48 hours, add these metrics to your Weekly Review:"),
        
        bullet_list_item("Impressions (how many people saw it)"),
        bullet_list_item("Engagement rate (likes + comments / impressions)"),
        bullet_list_item("Comments (and their quality)"),
        bullet_list_item("Profile views from this post"),
        bullet_list_item("Connection requests received"),
        
        divider(),
        
        heading_2("Your 30-Day Action Plan", color="green_background"),
        
        heading_3("Week 1-2:"),
        to_do("Post 3x per week minimum"),
        to_do("Engage daily (15 minutes)"),
        to_do("Track all metrics"),
        
        heading_3("Week 3-4:"),
        to_do("Analyze what's working (review Weekly Review database)"),
        to_do("Double down on best-performing pillar"),
        to_do("Experiment with different hook types"),
        
        divider(),
        
        callout(
            "Remember: Consistency beats perfection. Show up 3x per week for 90 days and watch what happens!",
            icon="💪",
            color="blue_background"
        ),
        
        divider(),
        
        heading_2("🎉 You Did It!", color="purple_background"),
        
        paragraph("You've completed the 5-day onboarding! Here's what you've built:"),
        
        bullet_list_item("✅ Defined your unique voice"),
        bullet_list_item("✅ Established 3-5 content pillars"),
        bullet_list_item("✅ Created and published your first post"),
        bullet_list_item("✅ Set up your posting rhythm"),
        bullet_list_item("✅ Learned the engagement strategies"),
        
        divider(),
        
        callout(
            "Now keep going! Use your Content Hub daily, batch create on Mondays, post consistently, and watch your LinkedIn presence grow.",
            icon="🚀",
            color="green_background"
        ),
        
        paragraph("Pro tip: Come back to the Voice Discovery and Content Pillars every 90 days to refine and evolve. Your voice will naturally develop as you post more!"),
    ]
    
    page_data = {
        "parent": {"page_id": dashboard_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "📚 Day 5: Launch & Rhythm"}}]
            }
        },
        "children": day5_content
    }
    
    client.client.pages.create(**page_data)
    print("  ✅ Created Day 5: Launch & Rhythm")


def create_prompt_library(client: NotionTemplateClient) -> str:
    """
    Create the Prompt Library database with 25+ ready-to-use prompts.
    
    Returns:
        Database ID
    """
    print("\n💡 Creating Prompt Library...")
    
    properties = {
        "Prompt Name": {
            "title": {}
        },
        "Category": {
            "select": {
                "options": [
                    {"name": "Hook Generator", "color": "red"},
                    {"name": "Post Structure", "color": "blue"},
                    {"name": "Idea Generation", "color": "green"},
                    {"name": "Repurposing", "color": "purple"},
                    {"name": "Voice-Specific", "color": "orange"}
                ]
            }
        },
        "Use Case": {
            "rich_text": {}
        },
        "Tested": {
            "checkbox": {}
        }
    }
    
    database = client.create_database(
        title="💡 Prompt Library",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add comprehensive prompt example
    print("  📝 Adding sample prompt...")
    page_properties = {
        "Prompt Name": {
            "title": [{"type": "text", "text": {"content": "Contrarian Opinion Hook Generator"}}]
        },
        "Category": {
            "select": {"name": "Hook Generator"}
        },
        "Use Case": {
            "rich_text": [{"type": "text", "text": {"content": "Create attention-grabbing first lines that challenge common beliefs"}}]
        },
        "Tested": {
            "checkbox": True
        }
    }
    
    page_content = [
        heading_1("💡 Contrarian Opinion Hook Generator", color="red_background"),
        
        callout(
            "Use this prompt to create scroll-stopping hooks that challenge conventional wisdom.",
            icon="🎣",
            color="red_background"
        ),
        
        divider(),
        
        heading_2("The Prompt", color="blue_background"),
        
        code(
            "I need a contrarian opinion hook for a LinkedIn post.\n\n"
            "Topic: [YOUR TOPIC]\n"
            "Common belief: [WHAT MOST PEOPLE THINK]\n"
            "Your contrarian take: [YOUR DIFFERENT VIEW]\n\n"
            "Generate 5 hook options that:\n"
            "1. Challenge the common belief directly\n"
            "2. Create curiosity and pattern interrupt\n"
            "3. Are under 12 words\n"
            "4. Sound like this voice: [PASTE YOUR VOICE PROFILE]\n\n"
            "Format as:\n"
            "Hook 1: [text]\n"
            "Why it works: [brief explanation]\n\n"
            "Hook 2: [text]\n"
            "Why it works: [brief explanation]\n"
            "...",
            language="markdown"
        ),
        
        divider(),
        
        heading_2("Example Usage", color="green_background"),
        
        heading_3("Input:"),
        paragraph("Topic: AI and Content Creation"),
        paragraph("Common belief: AI will replace content creators"),
        paragraph("Your take: AI won't replace creators, but AI-powered creators will replace those who don't adapt"),
        
        heading_3("Output Examples:"),
        quote("Hook 1: 'Why AI won't replace you (but AI-powered creators will)'"),
        quote("Hook 2: 'Everyone's asking the wrong question about AI'"),
        quote("Hook 3: 'AI isn't your competition. This is.'"),
        
        divider(),
        
        heading_2("When to Use This", color="purple_background"),
        
        bullet_list_item("When you have a unique perspective on a hot topic"),
        bullet_list_item("To stand out in a crowded feed"),
        bullet_list_item("When you want to spark debate/engagement"),
        bullet_list_item("To position yourself as a thought leader"),
        
        divider(),
        
        heading_2("Tips for Best Results", color="orange_background"),
        
        to_do("Make sure your contrarian view is backed by experience or data"),
        to_do("Don't be contrarian just to be different—have a real insight"),
        to_do("Test multiple hooks and see which performs best"),
        to_do("Always include your voice profile for authentic-sounding results"),
        
        divider(),
        
        callout(
            "Pro Tip: Save the hooks that perform well and analyze what made them work. Build your own library of winning patterns!",
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


def create_weekly_review(client: NotionTemplateClient) -> str:
    """
    Create Weekly Review & Analytics database.
    
    Returns:
        Database ID
    """
    print("\n📊 Creating Weekly Review & Analytics...")
    
    properties = {
        "Week Of": {
            "title": {}
        },
        "Posts Published": {
            "number": {}
        },
        "Total Engagement": {
            "number": {}
        },
        "New Followers": {
            "number": {}
        },
        "Best Performing Post": {
            "rich_text": {}
        },
        "Key Learning": {
            "rich_text": {}
        },
        "Next Week Goal": {
            "rich_text": {}
        }
    }
    
    database = client.create_database(
        title="📊 Weekly Review",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add sample week
    print("  📝 Adding sample week...")
    page_properties = {
        "Week Of": {
            "title": [{"type": "text", "text": {"content": "Week of Oct 7, 2025"}}]
        },
        "Posts Published": {
            "number": 3
        },
        "Total Engagement": {
            "number": 247
        },
        "New Followers": {
            "number": 18
        },
        "Best Performing Post": {
            "rich_text": [{"type": "text", "text": {"content": "AI Won't Replace You post - 1,234 impressions, 89 likes"}}]
        }
    }
    
    page_content = [
        heading_1("📊 Weekly Review Template", color="blue_background"),
        
        callout(
            "Use this template every Sunday to review your week and plan the next one. Data-driven improvement!",
            icon="📈",
            color="purple_background"
        ),
        
        divider(),
        
        heading_2("📊 This Week's Numbers", color="blue_background"),
        
        heading_3("Posts:"),
        bullet_list_item("Total published: 3"),
        bullet_list_item("Planned vs Actual: 3/3 ✅"),
        
        heading_3("Engagement:"),
        bullet_list_item("Total likes: 89"),
        bullet_list_item("Total comments: 34"),
        bullet_list_item("Total shares: 12"),
        bullet_list_item("Engagement rate: 4.2% (Target: 3-5%)"),
        
        heading_3("Growth:"),
        bullet_list_item("New followers: +18"),
        bullet_list_item("Profile views: 156"),
        bullet_list_item("Connection requests: 8"),
        
        divider(),
        
        heading_2("🏆 Best Performing Content", color="green_background"),
        
        heading_3("Top Post:"),
        quote("'Why AI Won't Replace You (But AI-Powered Creators Will)'"),
        
        paragraph("Performance:"),
        bullet_list_item("Impressions: 1,234"),
        bullet_list_item("Engagement: 89 likes, 23 comments"),
        bullet_list_item("Engagement rate: 9.1%"),
        
        heading_3("Why It Worked:"),
        numbered_list_item("Contrarian hook grabbed attention"),
        numbered_list_item("Timely topic (AI is trending)"),
        numbered_list_item("Clear value in numbered list"),
        numbered_list_item("Ended with engaging question"),
        numbered_list_item("Posted at optimal time (Tue 9 AM)"),
        
        divider(),
        
        heading_2("📉 What Didn't Work", color="red_background"),
        
        paragraph("Lower performing post: [Title]"),
        bullet_list_item("Only 234 impressions"),
        bullet_list_item("2.1% engagement rate"),
        
        heading_3("Hypothesis:"),
        bullet_list_item("Posted on weekend (lower activity)"),
        bullet_list_item("Hook wasn't strong enough"),
        bullet_list_item("Topic might be too niche"),
        
        divider(),
        
        heading_2("💡 Key Learnings", color="purple_background"),
        
        numbered_list_item("Contrarian hooks outperform questions by 2x"),
        numbered_list_item("AI topic resonates strongly with my audience"),
        numbered_list_item("Tuesday 9 AM is my sweet spot for posting"),
        numbered_list_item("Numbered lists get 40% more engagement"),
        
        divider(),
        
        heading_2("🎯 Next Week's Goals", color="green_background"),
        
        to_do("Post 3x (Tue, Thu, Fri at 9 AM)"),
        to_do("Focus on AI & Entrepreneurship pillar (it's performing best)"),
        to_do("Try 2 contrarian hooks, 1 story hook"),
        to_do("Engage 15 min daily before posting"),
        to_do("Experiment with carousel format"),
        
        divider(),
        
        heading_2("📝 Content Plan for Next Week", color="blue_background"),
        
        heading_3("Tuesday:"),
        bullet_list_item("Topic: AI tools for solo founders"),
        bullet_list_item("Hook type: Contrarian"),
        bullet_list_item("Status: Drafted ✅"),
        
        heading_3("Thursday:"),
        bullet_list_item("Topic: My biggest AI mistake (cost me $2K)"),
        bullet_list_item("Hook type: Story"),
        bullet_list_item("Status: To draft"),
        
        heading_3("Friday:"),
        bullet_list_item("Topic: 5-step AI workflow"),
        bullet_list_item("Hook type: Framework"),
        bullet_list_item("Status: To draft"),
        
        divider(),
        
        callout(
            "Remember: What gets measured gets improved. Fill this out every Sunday and watch your LinkedIn presence grow exponentially!",
            icon="📈",
            color="green_background"
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
    Main function to create the COMPLETE LinkedIn Content OS.
    """
    print("=" * 70)
    print("🚀 LINKEDIN CONTENT OS - COMPLETE SYSTEM")
    print("=" * 70)
    print("Creating your full product bundle...\n")
    
    try:
        # Initialize Notion client
        client = NotionTemplateClient()
        
        # 1. Create Dashboard Cover Page
        dashboard_id = create_dashboard_cover_page(client)
        
        # 2. Create 5-Day Onboarding as child pages
        create_onboarding_module(client, dashboard_id)
        
        # 3. Import existing databases (Content Hub, Pillars, Voice Discovery)
        from linkedin_content_os import create_content_hub, create_content_pillars, create_voice_discovery
        
        content_hub_id = create_content_hub(client)
        pillars_id = create_content_pillars(client)
        voice_id = create_voice_discovery(client)
        
        # 4. Create new databases
        prompts_id = create_prompt_library(client)
        review_id = create_weekly_review(client)
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ COMPLETE LINKEDIN CONTENT OS CREATED!")
        print("=" * 70)
        print("\n📊 What Was Created:")
        print(f"\n🎨 Main Dashboard: {dashboard_id}")
        print("  └─ 5-Day Onboarding (Days 1-5)")
        print(f"\n📝 Content Hub: {content_hub_id}")
        print(f"🎯 Content Pillars: {pillars_id}")
        print(f"🎤 Voice Discovery: {voice_id}")
        print(f"💡 Prompt Library: {prompts_id}")
        print(f"📊 Weekly Review: {review_id}")
        
        print("\n🎉 Your COMPLETE system is ready!")
        print("\n🔗 Open Notion and navigate to the Dashboard to start!")
        print("\n💡 Next Steps:")
        print("  1. Open the Dashboard (main page)")
        print("  2. Read Day 1 of the Onboarding")
        print("  3. Follow the 5-day journey!")
        print("  4. Start creating amazing content! 🚀")
        
    except Exception as e:
        print(f"\n❌ Error during creation: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
