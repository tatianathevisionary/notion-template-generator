"""
Notion Template Generator - Main Orchestration Script

This script creates the complete AI Product Manager OS template structure in Notion.
It creates four main databases:
1. Opportunity Hub
2. AI Product Spec Generator
3. Experiment Tracker
4. Launch & Growth Hub
"""

import json
import os
from typing import Dict, Any
from notion_api_client import NotionTemplateClient
from notion_api_client import (
    heading_1, heading_2, heading_3, paragraph, bullet_list_item, numbered_list_item,
    to_do, toggle, callout, quote, code, table_of_contents, divider, bookmark
)


def load_template(template_name: str) -> Dict[str, Any]:
    """
    Load a template definition from the templates/ directory.
    
    Args:
        template_name: Name of the template file (without .json extension)
    
    Returns:
        Dictionary containing the template definition
    """
    template_path = os.path.join("templates", f"{template_name}.json")
    
    try:
        with open(template_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Template file not found: {template_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing template file: {e}")
        return {}


def create_opportunity_hub(client: NotionTemplateClient) -> str:
    """
    Create the Opportunity Hub database with sample entries.
    
    Returns:
        Database ID of the created Opportunity Hub
    """
    print("\n🎯 Creating Opportunity Hub...")
    
    # Load template definition
    template = load_template("opportunity_hub")
    
    # Define database properties
    properties = {
        "Name": {
            "title": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Backlog", "color": "gray"},
                    {"name": "Evaluating", "color": "blue"},
                    {"name": "Ready", "color": "green"},
                    {"name": "In Progress", "color": "yellow"},
                    {"name": "Shipped", "color": "purple"},
                    {"name": "Archived", "color": "red"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "P0 - Critical", "color": "red"},
                    {"name": "P1 - High", "color": "orange"},
                    {"name": "P2 - Medium", "color": "yellow"},
                    {"name": "P3 - Low", "color": "gray"}
                ]
            }
        },
        "Impact Score": {
            "number": {
                "format": "number"
            }
        },
        "Effort Score": {
            "number": {
                "format": "number"
            }
        },
        "Created": {
            "created_time": {}
        },
        "Last Edited": {
            "last_edited_time": {}
        }
    }
    
    # Create database
    database = client.create_database(
        title="🎯 Opportunity Hub",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add sample opportunity with rich text content
    print("  📝 Adding sample opportunity...")
    page_properties = {
        "Name": {
            "title": [{"type": "text", "text": {"content": "Example: AI-Powered Feature Discovery"}}]
        },
        "Status": {
            "select": {"name": "Evaluating"}
        },
        "Priority": {
            "select": {"name": "P1 - High"}
        },
        "Impact Score": {
            "number": 8
        },
        "Effort Score": {
            "number": 5
        }
    }
    
    # Rich text content blocks showcasing ALL Notion block types
    page_content = [
        # Table of Contents
        table_of_contents(),
        divider(),
        
        # Main Header with Color
        heading_1("🎯 Opportunity Overview", color="blue_background"),
        
        # Callout Box - Important Info
        callout(
            "This is a comprehensive example showcasing ALL available Notion block types! "
            "Use this as a template to create rich, structured content in your workspace.",
            icon="✨",
            color="purple_background"
        ),
        
        paragraph("This opportunity demonstrates how to use every content type available in the Notion API."),
        divider(),
        
        # Problem Statement Section
        heading_2("📋 Problem Statement", color="red_background"),
        paragraph(
            "Users struggle to discover relevant features in our product, "
            "leading to underutilization and frustration."
        ),
        
        # Quote Block
        quote(
            "The best products are built when teams deeply understand their users' pain points. "
            "- Product Management Wisdom"
        ),
        divider(),
        
        # Target Users with Different List Types
        heading_2("👥 Target Users", color="orange_background"),
        paragraph("We're targeting the following user segments:"),
        
        # Bulleted List
        heading_3("Primary Segments"),
        bullet_list_item("Product Managers looking for better workflows", color="default"),
        bullet_list_item("Teams wanting to improve collaboration", color="default"),
        bullet_list_item("Solo entrepreneurs building digital products", color="default"),
        
        # Numbered List
        heading_3("User Research Steps"),
        numbered_list_item("Conduct user interviews (10-15 users)"),
        numbered_list_item("Analyze usage patterns and pain points"),
        numbered_list_item("Create user personas and journey maps"),
        numbered_list_item("Validate findings with larger sample"),
        divider(),
        
        # Action Items with To-Do Checkboxes
        heading_2("✅ Action Items", color="green_background"),
        to_do("Schedule 10 user interviews", checked=True),
        to_do("Create user persona documents", checked=True),
        to_do("Analyze competitive solutions", checked=False),
        to_do("Draft initial feature requirements", checked=False),
        to_do("Present findings to stakeholders", checked=False),
        divider(),
        
        # Technical Implementation with Code Block
        heading_2("💻 Technical Considerations", color="blue_background"),
        paragraph("Here's a sample API call for feature tracking:"),
        code(
            '{\n'
            '  "feature_id": "ai_discovery",\n'
            '  "user_id": "usr_123",\n'
            '  "event": "feature_viewed",\n'
            '  "timestamp": "2025-10-05T10:30:00Z"\n'
            '}',
            language="json"
        ),
        paragraph("This allows us to track feature usage and measure adoption rates."),
        divider(),
        
        # Success Metrics Section
        heading_2("📊 Success Metrics", color="purple_background"),
        callout(
            "These metrics will help us measure the impact of this opportunity.",
            icon="📈",
            color="gray_background"
        ),
        
        # Metrics as Numbered List
        numbered_list_item("Increase feature adoption by 25% within 3 months"),
        numbered_list_item("Reduce time-to-value for new users from 7 days to 3 days"),
        numbered_list_item("Improve user satisfaction scores (NPS) by 15 points"),
        numbered_list_item("Decrease support tickets related to feature discovery by 40%"),
        divider(),
        
        # Collapsible Section with Toggle
        heading_2("📚 Additional Resources"),
        toggle("Click here to see related documentation and links"),
        
        # Bookmark Example
        bookmark(
            "https://www.notion.com/help",
            "Notion Help Center - Best practices for product management"
        ),
        divider(),
        
        # Final Tips Section
        heading_2("💡 Pro Tips", color="yellow_background"),
        callout(
            "Impact vs. Effort Matrix: Plot opportunities on a 2x2 grid. "
            "High impact + low effort = quick wins. Focus on these first!",
            icon="🎯",
            color="yellow_background"
        ),
        callout(
            "Regular Reviews: Revisit your opportunities monthly. User needs evolve, "
            "and yesterday's P3 might be today's P0!",
            icon="🔄",
            color="blue_background"
        ),
        callout(
            "Data-Driven Decisions: Always back your prioritization with user data, "
            "analytics, and customer feedback.",
            icon="📊",
            color="green_background"
        ),
        divider(),
        
        # Conclusion
        heading_2("🎉 Next Steps"),
        paragraph("Now that you understand the opportunity, here's what to do next:"),
        numbered_list_item("Share this doc with stakeholders for feedback"),
        numbered_list_item("Move to 'AI Product Spec' database to create detailed requirements"),
        numbered_list_item("Set up experiments to validate assumptions"),
        numbered_list_item("Track progress in the Launch Hub when ready"),
        
        # Final Callout
        callout(
            "This template demonstrates: Headings (1, 2, 3) with colors, Paragraphs, "
            "Bulleted lists, Numbered lists, To-do checkboxes, Toggles, Callouts with icons, "
            "Quotes, Code blocks, Table of contents, Dividers, and Bookmarks!",
            icon="🚀",
            color="purple_background"
        )
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def create_ai_product_spec(client: NotionTemplateClient) -> str:
    """
    Create the AI Product Spec Generator database with sample spec.
    
    Returns:
        Database ID of the created AI Product Spec database
    """
    print("\n📋 Creating AI Product Spec Generator...")
    
    # Load template definition
    template = load_template("ai_product_spec")
    
    # Define database properties
    properties = {
        "Name": {
            "title": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Draft", "color": "gray"},
                    {"name": "In Review", "color": "blue"},
                    {"name": "Approved", "color": "green"},
                    {"name": "In Development", "color": "yellow"},
                    {"name": "Shipped", "color": "purple"}
                ]
            }
        },
        "Owner": {
            "people": {}
        },
        "Created": {
            "created_time": {}
        }
    }
    
    database = client.create_database(
        title="📋 AI Product Spec",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add sample product spec with structured content
    print("  📝 Adding sample product spec...")
    page_properties = {
        "Name": {
            "title": [{"type": "text", "text": {"content": "Example: Smart Notifications Feature"}}]
        },
        "Status": {
            "select": {"name": "Draft"}
        }
    }
    
    # Rich text content for product spec
    page_content = [
        heading_1("📋 Product Specification"),
        paragraph("This is an example product spec template. Use this structure to document your product requirements."),
        divider(),
        heading_2("1. Overview"),
        paragraph("A brief summary of what this product/feature does and why it matters."),
        bullet_list_item("Problem: Users miss important updates"),
        bullet_list_item("Solution: Intelligent notification system"),
        bullet_list_item("Impact: Improved user engagement and satisfaction"),
        divider(),
        heading_2("2. User Stories"),
        paragraph("As a [user type], I want to [action] so that [benefit]."),
        bullet_list_item("As a product manager, I want to receive priority notifications so that I can respond quickly to critical issues"),
        bullet_list_item("As a team member, I want to customize my notification preferences so that I only see relevant updates"),
        divider(),
        heading_2("3. Requirements"),
        heading_2("Functional Requirements"),
        bullet_list_item("System shall send real-time notifications"),
        bullet_list_item("Users can customize notification preferences"),
        bullet_list_item("Notifications include action buttons for quick response"),
        heading_2("Non-Functional Requirements"),
        bullet_list_item("99.9% uptime for notification service"),
        bullet_list_item("Notifications delivered within 3 seconds"),
        bullet_list_item("Support for 10,000+ concurrent users"),
        divider(),
        heading_2("4. Success Metrics"),
        bullet_list_item("50% reduction in missed notifications"),
        bullet_list_item("80% user satisfaction score"),
        bullet_list_item("30% increase in feature engagement"),
        divider(),
        paragraph("💡 Tip: Keep your spec updated as requirements evolve. Use the Status property to track progress!")
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def create_experiment_tracker(client: NotionTemplateClient) -> str:
    """
    Create the Experiment Tracker database with sample experiment.
    
    Returns:
        Database ID of the created Experiment Tracker database
    """
    print("\n🧪 Creating Experiment Tracker...")
    
    # Load template definition
    template = load_template("experiment_tracker")
    
    # Define database properties
    properties = {
        "Name": {
            "title": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Planning", "color": "gray"},
                    {"name": "Running", "color": "blue"},
                    {"name": "Analyzing", "color": "yellow"},
                    {"name": "Completed", "color": "green"},
                    {"name": "Cancelled", "color": "red"}
                ]
            }
        },
        "Hypothesis": {
            "rich_text": {}
        },
        "Success Metric": {
            "rich_text": {}
        },
        "Start Date": {
            "date": {}
        },
        "End Date": {
            "date": {}
        },
        "Result": {
            "select": {
                "options": [
                    {"name": "Success", "color": "green"},
                    {"name": "Partial Success", "color": "yellow"},
                    {"name": "Failed", "color": "red"},
                    {"name": "Inconclusive", "color": "gray"}
                ]
            }
        }
    }
    
    database = client.create_database(
        title="🧪 Experiment Tracker",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add sample experiment with detailed content
    print("  📝 Adding sample experiment...")
    page_properties = {
        "Name": {
            "title": [{"type": "text", "text": {"content": "Example: Onboarding Flow A/B Test"}}]
        },
        "Status": {
            "select": {"name": "Planning"}
        },
        "Hypothesis": {
            "rich_text": [{"type": "text", "text": {"content": "Simplifying the onboarding flow will increase completion rates"}}]
        },
        "Success Metric": {
            "rich_text": [{"type": "text", "text": {"content": "Onboarding completion rate"}}]
        },
        "Start Date": {
            "date": {"start": "2025-10-10"}
        },
        "End Date": {
            "date": {"start": "2025-10-24"}
        }
    }
    
    # Rich text content for experiment
    page_content = [
        heading_1("🧪 Experiment Design"),
        paragraph("This is an example experiment to demonstrate how to structure and track your tests."),
        divider(),
        heading_2("Hypothesis"),
        paragraph("IF we simplify the onboarding flow from 5 steps to 3 steps,"),
        paragraph("THEN we will see an increase in completion rates,"),
        paragraph("BECAUSE users get frustrated with lengthy signup processes."),
        divider(),
        heading_2("Experiment Setup"),
        heading_2("Control Group (A)"),
        bullet_list_item("Current 5-step onboarding flow"),
        bullet_list_item("50% of new users"),
        heading_2("Treatment Group (B)"),
        bullet_list_item("New 3-step onboarding flow"),
        bullet_list_item("50% of new users"),
        divider(),
        heading_2("Success Metrics"),
        heading_2("Primary Metric"),
        bullet_list_item("Onboarding completion rate (target: +20%)"),
        heading_2("Secondary Metrics"),
        bullet_list_item("Time to complete onboarding"),
        bullet_list_item("User activation rate (completing first action)"),
        bullet_list_item("7-day retention rate"),
        divider(),
        heading_2("Sample Size & Duration"),
        bullet_list_item("Minimum sample: 1,000 users per group"),
        bullet_list_item("Duration: 2 weeks"),
        bullet_list_item("Statistical significance threshold: 95%"),
        divider(),
        heading_2("Results"),
        paragraph("📊 Results will be recorded here after the experiment concludes."),
        divider(),
        paragraph("💡 Tip: Document your learnings even if the experiment fails. Failed experiments teach us what NOT to do!")
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def create_launch_hub(client: NotionTemplateClient) -> str:
    """
    Create the Launch & Growth Hub database with sample launch plan.
    
    Returns:
        Database ID of the created Launch Hub database
    """
    print("\n🚀 Creating Launch & Growth Hub...")
    
    # Load template definition
    template = load_template("launch_hub")
    
    # Define database properties
    properties = {
        "Name": {
            "title": {}
        },
        "Phase": {
            "select": {
                "options": [
                    {"name": "Planning", "color": "gray"},
                    {"name": "Pre-Launch", "color": "blue"},
                    {"name": "Launch", "color": "orange"},
                    {"name": "Post-Launch", "color": "green"},
                    {"name": "Growth", "color": "purple"}
                ]
            }
        },
        "Launch Date": {
            "date": {}
        },
        "Channel": {
            "multi_select": {
                "options": [
                    {"name": "Product Hunt", "color": "orange"},
                    {"name": "LinkedIn", "color": "blue"},
                    {"name": "Twitter", "color": "blue"},
                    {"name": "Email", "color": "green"},
                    {"name": "Blog", "color": "purple"}
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Not Started", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Complete", "color": "green"}
                ]
            }
        }
    }
    
    database = client.create_database(
        title="🚀 Launch & Growth Hub",
        properties=properties
    )
    
    database_id = database["id"]
    
    # Add sample launch plan with comprehensive content
    print("  📝 Adding sample launch plan...")
    page_properties = {
        "Name": {
            "title": [{"type": "text", "text": {"content": "Example: Product Hunt Launch Campaign"}}]
        },
        "Phase": {
            "select": {"name": "Planning"}
        },
        "Launch Date": {
            "date": {"start": "2025-11-01"}
        },
        "Channel": {
            "multi_select": [
                {"name": "Product Hunt"},
                {"name": "LinkedIn"},
                {"name": "Twitter"}
            ]
        },
        "Status": {
            "select": {"name": "Not Started"}
        }
    }
    
    # Rich text content for launch plan
    page_content = [
        heading_1("🚀 Launch Strategy"),
        paragraph("This is an example launch plan to help you structure your go-to-market strategy."),
        divider(),
        heading_2("Launch Goals"),
        bullet_list_item("🎯 #1 Product of the Day on Product Hunt"),
        bullet_list_item("📈 1,000+ sign-ups in first week"),
        bullet_list_item("💬 50+ user testimonials"),
        bullet_list_item("📰 Featured in 3+ tech publications"),
        divider(),
        heading_2("Pre-Launch Checklist (2 weeks before)"),
        bullet_list_item("✅ Finalize product landing page"),
        bullet_list_item("✅ Prepare launch assets (screenshots, videos, graphics)"),
        bullet_list_item("✅ Build email list of supporters"),
        bullet_list_item("✅ Schedule Product Hunt launch (Tuesday or Wednesday)"),
        bullet_list_item("✅ Prepare social media content calendar"),
        bullet_list_item("✅ Reach out to influencers and journalists"),
        divider(),
        heading_2("Launch Day Timeline"),
        heading_2("12:01 AM PST - Go Live"),
        bullet_list_item("Publish on Product Hunt"),
        bullet_list_item("Send email to supporter list"),
        bullet_list_item("Post on social media channels"),
        heading_2("Throughout the Day"),
        bullet_list_item("Respond to all comments within 30 minutes"),
        bullet_list_item("Share updates every 2 hours"),
        bullet_list_item("Engage with community feedback"),
        heading_2("End of Day"),
        bullet_list_item("Thank supporters publicly"),
        bullet_list_item("Document metrics and learnings"),
        divider(),
        heading_2("Channel Strategy"),
        heading_2("🔶 Product Hunt"),
        bullet_list_item("Engage with hunters and voters"),
        bullet_list_item("Respond to every comment"),
        bullet_list_item("Share behind-the-scenes content"),
        heading_2("💼 LinkedIn"),
        bullet_list_item("Personal launch announcement post"),
        bullet_list_item("Share customer success stories"),
        bullet_list_item("Engage with relevant communities"),
        heading_2("🐦 Twitter"),
        bullet_list_item("Launch thread with product highlights"),
        bullet_list_item("Live updates throughout the day"),
        bullet_list_item("Retweet user feedback and testimonials"),
        divider(),
        heading_2("Success Metrics"),
        bullet_list_item("Product Hunt ranking: #1-3"),
        bullet_list_item("Website traffic: 10,000+ visitors"),
        bullet_list_item("Sign-ups: 1,000+"),
        bullet_list_item("Social mentions: 500+"),
        bullet_list_item("Press coverage: 3+ articles"),
        divider(),
        heading_2("Post-Launch (Week 1)"),
        bullet_list_item("Send thank you email to supporters"),
        bullet_list_item("Share launch metrics publicly"),
        bullet_list_item("Publish launch retrospective blog post"),
        bullet_list_item("Engage with new users for feedback"),
        bullet_list_item("Plan growth experiments based on data"),
        divider(),
        paragraph("💡 Tip: Launch is just the beginning! Focus on building momentum in the weeks after launch.")
    ]
    
    client.create_page_in_database(
        database_id=database_id,
        properties=page_properties,
        children=page_content
    )
    
    return database_id


def main():
    """
    Main function to orchestrate the creation of all templates.
    """
    print("=" * 60)
    print("🎨 NOTION TEMPLATE GENERATOR")
    print("=" * 60)
    print("Creating AI Product Manager OS templates...\n")
    
    try:
        # Initialize Notion client
        client = NotionTemplateClient()
        
        # Create all databases
        opportunity_hub_id = create_opportunity_hub(client)
        product_spec_id = create_ai_product_spec(client)
        experiment_tracker_id = create_experiment_tracker(client)
        launch_hub_id = create_launch_hub(client)
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ TEMPLATE CREATION COMPLETE!")
        print("=" * 60)
        print("\n📊 Created Databases:")
        print(f"  • Opportunity Hub: {opportunity_hub_id}")
        print(f"  • AI Product Spec: {product_spec_id}")
        print(f"  • Experiment Tracker: {experiment_tracker_id}")
        print(f"  • Launch & Growth Hub: {launch_hub_id}")
        print("\n🔗 Visit your Notion workspace to see the new templates!")
        
    except Exception as e:
        print(f"\n❌ Error during template creation: {e}")
        raise


if __name__ == "__main__":
    main()
