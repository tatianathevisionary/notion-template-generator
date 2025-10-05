#!/usr/bin/env python3
"""
Multi-Format Update Generator

Transforms raw weekly notes into professional updates for:
- Detailed Document (Markdown)
- Slack Update (concise, emoji-rich)
- LinkedIn Post (engaging, public-facing)
- Blog Post (comprehensive, SEO-friendly)

Based on research from Slack, LinkedIn, and technical blogging best practices.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class UpdateGenerator:
    """Generate updates in multiple formats from structured data."""
    
    def __init__(self, project_name: str, date: str = None):
        """
        Initialize the generator.
        
        Args:
            project_name: Name of the project
            date: Date string (default: today)
        """
        self.project_name = project_name
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.update_data = {}
        
    def load_from_template(self, data: Dict[str, Any]):
        """
        Load update data from structured dictionary.
        
        Expected structure:
        {
            "status": "on_track" | "at_risk" | "off_track",
            "highlight": "Main accomplishment",
            "next_priority": "Next week's top priority",
            "progress": ["Item 1", "Item 2"...],
            "goals": ["Goal 1", "Goal 2"...],
            "metrics": [{"name": "Metric", "value": "100", "change": "+10%"}...],
            "risks": [{"type": "risk" | "blocker", "description": "..."}...],
            "decisions": ["Decision 1"...],
            "learnings": ["Learning 1"...],
            "asks": ["Ask 1"...]
        }
        """
        self.update_data = data
        
    def _get_status_emoji(self) -> str:
        """Get status emoji based on status."""
        status_map = {
            "on_track": "🟢",
            "at_risk": "🟡",
            "off_track": "🔴"
        }
        return status_map.get(self.update_data.get("status", "on_track"), "🟢")
    
    def generate_document(self, filename: str = None) -> str:
        """
        Generate detailed Markdown document.
        
        Returns:
            Markdown-formatted update
        """
        status_emoji = self._get_status_emoji()
        
        doc = f"""# Project Update: {self.project_name} - {self.date}

### **TL;DR - Executive Summary**
* **Status:** {status_emoji} {self.update_data.get('status', 'On Track').replace('_', ' ').title()}
* **Highlight:** {self.update_data.get('highlight', '[Highlight missing]')}
* **Next Up:** {self.update_data.get('next_priority', '[Next priority missing]')}

---

### ✅ Progress This Week
*A summary of key accomplishments completed this week.*
"""
        
        # Add progress items
        for item in self.update_data.get('progress', []):
            doc += f"- {item}\n"
        
        doc += f"""
### 🎯 Goals for Next Week
*The top 3-5 priorities for the upcoming week.*
"""
        
        # Add goals
        for goal in self.update_data.get('goals', []):
            doc += f"- {goal}\n"
        
        doc += f"""
### 📊 Key Metrics & KPIs
*A snapshot of key performance indicators.*
"""
        
        # Add metrics
        for metric in self.update_data.get('metrics', []):
            change = f" ({metric.get('change', 'N/A')})" if 'change' in metric else ""
            doc += f"- **{metric['name']}:** {metric['value']}{change}\n"
        
        doc += f"""
### ⚠️ Risks & Blockers
*Anything that could impede progress or requires attention from leadership.*
"""
        
        # Add risks
        risks = self.update_data.get('risks', [])
        if risks:
            for risk in risks:
                risk_type = risk.get('type', 'Risk').capitalize()
                doc += f"- **{risk_type}:** {risk['description']}\n"
        else:
            doc += "- [No blockers to report this week.]\n"
        
        doc += f"""
### 💡 Decisions & Learnings
*A record of key decisions made and insights gained. This is for our internal knowledge base.*
"""
        
        # Add decisions
        if self.update_data.get('decisions'):
            doc += "\n**Key Decisions:**\n"
            for decision in self.update_data['decisions']:
                doc += f"- **Decision:** {decision}\n"
        
        # Add learnings
        if self.update_data.get('learnings'):
            doc += "\n**Critical Learnings:**\n"
            for learning in self.update_data['learnings']:
                doc += f"- **Learning:** {learning}\n"
        
        if not self.update_data.get('decisions') and not self.update_data.get('learnings'):
            doc += "- [No major decisions or learnings this week.]\n"
        
        doc += f"""
### 🙏 Asks / Needs
*Specific help required from the update's recipients.*
"""
        
        # Add asks
        asks = self.update_data.get('asks', [])
        if asks:
            for ask in asks:
                doc += f"- {ask}\n"
        else:
            doc += "- [No specific asks this week.]\n"
        
        doc += f"\n---\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        # Save to file if filename provided
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(doc)
            print(f"✅ Document saved to: {filename}")
        
        return doc
    
    def generate_slack_update(self) -> str:
        """
        Generate concise Slack update.
        
        Based on best practices:
        - Use emojis for visual scanning
        - Keep it brief (under 500 words)
        - Lead with status
        - Use threads for details
        """
        status_emoji = self._get_status_emoji()
        
        slack = f"""*{self.project_name} Weekly Update* • {self.date}

{status_emoji} *Status:* {self.update_data.get('status', 'on_track').replace('_', ' ').title()}

*🎯 This Week's Win*
{self.update_data.get('highlight', '[Highlight missing]')}

*✅ What We Shipped*
"""
        
        # Add top 3 progress items
        for item in self.update_data.get('progress', [])[:3]:
            slack += f"• {item}\n"
        
        more_items = len(self.update_data.get('progress', [])) - 3
        if more_items > 0:
            slack += f"_...and {more_items} more (see thread)_\n"
        
        slack += f"""
*🚀 Next Week*
"""
        
        # Add top 2 goals
        for goal in self.update_data.get('goals', [])[:2]:
            slack += f"• {goal}\n"
        
        # Add metrics if available
        if self.update_data.get('metrics'):
            slack += "\n*📊 Key Metrics*\n"
            for metric in self.update_data['metrics'][:3]:
                change = f" {metric.get('change', '')}" if 'change' in metric else ""
                slack += f"• {metric['name']}: *{metric['value']}*{change}\n"
        
        # Add blockers if any
        if self.update_data.get('risks'):
            slack += "\n*⚠️ Needs Attention*\n"
            for risk in self.update_data['risks'][:2]:
                slack += f"• {risk['description']}\n"
        
        # Add asks if any
        if self.update_data.get('asks'):
            slack += "\n*🙏 Need Help With*\n"
            for ask in self.update_data['asks'][:2]:
                slack += f"• {ask}\n"
        
        slack += f"\n_Full details in thread_ 👇"
        
        return slack
    
    def generate_linkedin_post(self) -> str:
        """
        Generate engaging LinkedIn post.
        
        Based on best practices:
        - Hook in first 2 lines
        - Tell a story
        - Use line breaks (every 1-2 sentences)
        - End with question/CTA
        - 3-5 hashtags
        """
        
        # Extract key numbers for impact
        metrics = self.update_data.get('metrics', [])
        metric_callout = ""
        if metrics:
            top_metric = metrics[0]
            metric_callout = f"\n\n📊 {top_metric['name']}: {top_metric['value']}"
            if 'change' in top_metric:
                metric_callout += f" ({top_metric['change']})"
        
        linkedin = f"""🚀 Week in Review: {self.project_name}

{self.update_data.get('highlight', '[Add your main accomplishment]')}

Here's what we shipped this week:
"""
        
        # Add progress with emojis
        progress_emojis = ["✅", "🎯", "💡", "🔧", "📦"]
        for i, item in enumerate(self.update_data.get('progress', [])[:3]):
            emoji = progress_emojis[i % len(progress_emojis)]
            # Shorten for LinkedIn
            short_item = item[:100] + "..." if len(item) > 100 else item
            linkedin += f"\n{emoji} {short_item}"
        
        linkedin += metric_callout
        
        # Add a learning or decision as story
        learnings = self.update_data.get('learnings', [])
        if learnings:
            linkedin += f"\n\n💭 Key insight:\n{learnings[0][:150]}"
        
        # Next focus
        next_priority = self.update_data.get('next_priority', '')
        if next_priority:
            linkedin += f"\n\n🎯 Next up:\n{next_priority[:120]}"
        
        # CTA question
        linkedin += "\n\nWhat's the biggest win from your week? 👇"
        
        # Hashtags
        linkedin += "\n\n#BuildInPublic #ProductDevelopment #TechUpdates"
        
        # Add project-specific hashtags
        if "notion" in self.project_name.lower():
            linkedin += " #Notion #Productivity"
        if "ai" in self.project_name.lower():
            linkedin += " #AI #Automation"
        
        return linkedin
    
    def generate_blog_post(self) -> str:
        """
        Generate comprehensive blog post.
        
        Based on best practices:
        - SEO-friendly title
        - Clear structure with headers
        - Introduction with hook
        - Detailed sections
        - Visuals/code blocks
        - Conclusion with CTA
        """
        
        blog = f"""# {self.project_name}: Weekly Development Update ({self.date})

## TL;DR

{self.update_data.get('highlight', '[Main accomplishment]')} This week focused on {len(self.update_data.get('progress', []))} major improvements while maintaining our momentum toward {self.update_data.get('next_priority', '[next milestone]')}.

---

## Introduction

Another productive week for the {self.project_name} project! This update covers our progress, challenges, and what's coming next.

**Quick Stats:**
"""
        
        # Add metrics
        for metric in self.update_data.get('metrics', [])[:5]:
            change = f" ({metric.get('change', 'N/A')})" if 'change' in metric else ""
            blog += f"- {metric['name']}: **{metric['value']}**{change}\n"
        
        blog += f"""
---

## What We Built This Week

This week was all about execution. Here's what we shipped:

"""
        
        # Add detailed progress
        for i, item in enumerate(self.update_data.get('progress', []), 1):
            blog += f"### {i}. {item.split(':')[0] if ':' in item else f'Feature {i}'}\n\n"
            blog += f"{item}\n\n"
        
        blog += "---\n\n"
        
        # Add learnings section
        if self.update_data.get('learnings') or self.update_data.get('decisions'):
            blog += "## Key Insights & Decisions\n\n"
            blog += "Every week brings new learnings that shape our approach. Here's what we discovered:\n\n"
            
            if self.update_data.get('decisions'):
                blog += "### Strategic Decisions\n\n"
                for decision in self.update_data['decisions']:
                    blog += f"- {decision}\n"
                blog += "\n"
            
            if self.update_data.get('learnings'):
                blog += "### Technical Learnings\n\n"
                for learning in self.update_data['learnings']:
                    blog += f"- {learning}\n"
                blog += "\n"
            
            blog += "---\n\n"
        
        # Add challenges section
        if self.update_data.get('risks'):
            blog += "## Challenges & Solutions\n\n"
            blog += "Transparency is key. Here are the challenges we're navigating:\n\n"
            
            for risk in self.update_data['risks']:
                risk_type = risk.get('type', 'Challenge').capitalize()
                blog += f"**{risk_type}:** {risk['description']}\n\n"
            
            blog += "---\n\n"
        
        # Add next week section
        blog += "## What's Next\n\n"
        blog += f"Looking ahead, our top priority is: **{self.update_data.get('next_priority', '[Next priority]')}**\n\n"
        blog += "### Planned Work\n\n"
        
        for goal in self.update_data.get('goals', []):
            blog += f"- {goal}\n"
        
        blog += "\n---\n\n"
        
        # Add conclusion
        blog += "## Conclusion\n\n"
        blog += f"This week demonstrated strong momentum on {self.project_name}. "
        blog += f"We're {self._get_status_emoji()} {self.update_data.get('status', 'on track').replace('_', ' ')} "
        blog += "and excited about the progress ahead.\n\n"
        
        # Add asks
        if self.update_data.get('asks'):
            blog += "### How You Can Help\n\n"
            for ask in self.update_data['asks']:
                blog += f"- {ask}\n"
            blog += "\n"
        
        blog += "---\n\n"
        blog += f"*Last updated: {datetime.now().strftime('%B %d, %Y')}*\n"
        
        return blog
    
    def generate_all(self, output_dir: str = "."):
        """
        Generate all formats and save to files.
        
        Args:
            output_dir: Directory to save files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        date_slug = self.date
        project_slug = self.project_name.lower().replace(" ", "_")
        
        # Generate all formats
        print("\n📝 Generating updates in all formats...\n")
        
        # 1. Detailed document
        doc_file = output_path / f"{project_slug}_update_{date_slug}.md"
        doc = self.generate_document(str(doc_file))
        
        # 2. Slack update
        slack_file = output_path / f"{project_slug}_slack_{date_slug}.txt"
        slack = self.generate_slack_update()
        with open(slack_file, 'w', encoding='utf-8') as f:
            f.write(slack)
        print(f"✅ Slack update saved to: {slack_file}")
        
        # 3. LinkedIn post
        linkedin_file = output_path / f"{project_slug}_linkedin_{date_slug}.txt"
        linkedin = self.generate_linkedin_post()
        with open(linkedin_file, 'w', encoding='utf-8') as f:
            f.write(linkedin)
        print(f"✅ LinkedIn post saved to: {linkedin_file}")
        
        # 4. Blog post
        blog_file = output_path / f"{project_slug}_blog_{date_slug}.md"
        blog = self.generate_blog_post()
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(blog)
        print(f"✅ Blog post saved to: {blog_file}")
        
        print(f"\n🎉 All formats generated successfully!\n")
        
        return {
            "document": str(doc_file),
            "slack": str(slack_file),
            "linkedin": str(linkedin_file),
            "blog": str(blog_file)
        }


def load_template_from_file(template_file: str) -> Dict[str, Any]:
    """
    Load update data from JSON template file.
    
    Args:
        template_file: Path to JSON template
        
    Returns:
        Dictionary with update data
    """
    with open(template_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main function with command-line support."""
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        Multi-Format Update Generator                     ║
║        Document • Slack • LinkedIn • Blog                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check for template file argument
    if len(sys.argv) > 1:
        template_file = sys.argv[1]
        print(f"\n📂 Loading template from: {template_file}")
        
        try:
            update_data = load_template_from_file(template_file)
            
            # Extract metadata
            project_name = update_data.get("project_name", "Project")
            date = update_data.get("date", datetime.now().strftime("%Y-%m-%d"))
            
            # Generate all formats
            generator = UpdateGenerator(project_name, date)
            generator.load_from_template(update_data)
            
            output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
            files = generator.generate_all(output_dir)
            
            print("\n📊 Generated Files:")
            for format_name, filepath in files.items():
                print(f"   • {format_name.capitalize()}: {filepath}")
            
            return
            
        except FileNotFoundError:
            print(f"❌ Error: Template file not found: {template_file}")
            print("\n💡 Usage: python update_generator.py <template.json> [output_dir]")
            print("   Or run without arguments to see example")
            return
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in template file: {e}")
            return
    
    # Example update data (demo mode)
    example_data = {
        "status": "on_track",
        "highlight": "Successfully upgraded to Notion API 2025-09-03 and built comprehensive database enhancement tools",
        "next_priority": "Extend enhancement capabilities to remaining 4 databases with web-searched resources",
        "progress": [
            "Upgraded to Notion API 2025-09-03: Migrated entire codebase to support data sources architecture",
            "Built Complete Database Retrieval System: Created 3 production tools for analysis and content population",
            "Enhanced Content Hub with 210 Rich Blocks: Populated with templates, best practices, and examples"
        ],
        "goals": [
            "Build multi-format update generation system (Document, Slack, LinkedIn, Blog)",
            "Enhance remaining 4 databases with rich content and interactive elements",
            "Integrate web search to find and embed relevant images and resources"
        ],
        "metrics": [
            {"name": "API Version", "value": "2025-09-03", "change": "upgraded"},
            {"name": "Databases Enhanced", "value": "1 of 5", "change": "20%"},
            {"name": "Content Blocks Created", "value": "210", "change": "+210"},
            {"name": "Tools Built", "value": "3", "change": "+3"}
        ],
        "risks": [
            {
                "type": "blocker",
                "description": "Content volume challenge - creating rich content for all 5 databases will be time-intensive (4-6 hours per database)"
            }
        ],
        "decisions": [
            "Upgraded to Notion API 2025-09-03 despite breaking changes for future multi-source functionality",
            "Built modular tools instead of monolithic script for better maintainability"
        ],
        "learnings": [
            "Data source IDs are mandatory in 2025-09-03 - every page creation must use data_source_id as parent",
            "Real content beats empty schemas - users need production-ready templates with examples"
        ],
        "asks": [
            "Content review of enhanced Content Hub pages before replicating pattern",
            "Database priority guidance for next enhancement cycle"
        ]
    }
    
    # Generate all formats
    generator = UpdateGenerator("Notion Template Generator", "2025-10-05")
    generator.load_from_template(example_data)
    
    files = generator.generate_all(".")
    
    print("\n📊 Generated Files:")
    for format_name, filepath in files.items():
        print(f"   • {format_name.capitalize()}: {filepath}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
