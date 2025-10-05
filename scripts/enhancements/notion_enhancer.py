#!/usr/bin/env python3
"""
Notion Database Enhancement Tool

This tool:
1. Retrieves complete database structure and content from Notion
2. Uses web search to find relevant resources (images, links, examples)
3. Compares with local folder content
4. Removes duplicates
5. Enhances databases with rich content (images, checklists, links, callouts)
6. Updates Notion databases with improved content
"""

import os
import json
import time
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from datetime import datetime

from notion_api_client import (
    NotionTemplateClient,
    heading_1, heading_2, heading_3,
    paragraph, bullet_list_item, numbered_list_item,
    to_do, toggle, callout, quote, code,
    table_of_contents, divider, bookmark
)


class NotionEnhancer:
    """Enhanced Notion database manager with web search integration."""
    
    def __init__(self, local_content_folder: str):
        """
        Initialize the enhancer.
        
        Args:
            local_content_folder: Path to local content folder (e.g., LinkedIn Content OS)
        """
        self.client = NotionTemplateClient()
        self.local_folder = Path(local_content_folder)
        self.retrieved_content = {}
        self.enhancement_suggestions = []
        
    def retrieve_database_content(self, database_id: str) -> Dict[str, Any]:
        """
        Retrieve complete database content including all pages.
        
        Args:
            database_id: The Notion database ID
            
        Returns:
            Dictionary with database metadata and all pages
        """
        print(f"\n📊 Retrieving database: {database_id[:8]}...")
        
        try:
            # Get database metadata
            database = self.client.get_database(database_id)
            
            # Get data source
            data_source_id = database["data_sources"][0]["id"]
            data_source = self.client.retrieve_data_source(data_source_id)
            
            # Get title
            title_list = database.get("title", [])
            if title_list:
                db_title = title_list[0].get("text", {}).get("content", "Untitled")
            else:
                db_title = "Untitled"
            
            print(f"   📋 Database: {db_title}")
            
            # Query all pages
            pages = self.client.query_database(database_id)
            print(f"   📄 Found {len(pages)} pages")
            
            # Get content for each page
            detailed_pages = []
            for page in pages:
                page_id = page["id"]
                
                # Get page blocks (content)
                try:
                    blocks_response = self.client.client.blocks.children.list(
                        block_id=page_id,
                        page_size=100
                    )
                    blocks = blocks_response.get("results", [])
                    
                    page["blocks"] = blocks
                    page["block_count"] = len(blocks)
                except Exception as e:
                    print(f"      ⚠️  Could not retrieve blocks for page: {str(e)[:50]}")
                    page["blocks"] = []
                    page["block_count"] = 0
                
                detailed_pages.append(page)
                time.sleep(0.2)  # Rate limiting
            
            result = {
                "database": database,
                "data_source": data_source,
                "title": db_title,
                "pages": detailed_pages,
                "total_pages": len(detailed_pages),
                "properties": data_source.get("properties", {})
            }
            
            self.retrieved_content[database_id] = result
            return result
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def analyze_local_content(self) -> Dict[str, Any]:
        """
        Analyze local folder content for enhancement ideas.
        
        Returns:
            Dictionary with file contents and structure
        """
        print(f"\n📂 Analyzing local folder: {self.local_folder.name}")
        
        content_map = {}
        
        # Scan for markdown files
        md_files = list(self.local_folder.rglob("*.md"))
        txt_files = list(self.local_folder.rglob("*.txt"))
        
        all_files = md_files + txt_files
        
        print(f"   📄 Found {len(all_files)} content files")
        
        for file_path in all_files:
            try:
                relative_path = file_path.relative_to(self.local_folder)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_map[str(relative_path)] = {
                    "content": content,
                    "size": len(content),
                    "lines": content.count('\n'),
                    "category": self._categorize_file(relative_path)
                }
                
            except Exception as e:
                print(f"      ⚠️  Could not read {file_path.name}: {e}")
        
        return content_map
    
    def _categorize_file(self, path: Path) -> str:
        """Categorize file based on its path."""
        path_str = str(path).lower()
        
        if "onboarding" in path_str:
            return "onboarding"
        elif "marketing" in path_str:
            return "marketing"
        elif "prompt" in path_str:
            return "prompts"
        elif "data" in path_str:
            return "planning"
        elif "automation" in path_str:
            return "automation"
        else:
            return "other"
    
    def find_duplicates(self, db_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find duplicate pages based on title similarity.
        
        Args:
            db_content: Retrieved database content
            
        Returns:
            List of potential duplicates
        """
        print(f"\n🔍 Searching for duplicates...")
        
        pages = db_content.get("pages", [])
        duplicates = []
        seen_titles = {}
        
        for page in pages:
            # Extract title
            properties = page.get("properties", {})
            title_prop = None
            
            # Find title property
            for prop_name, prop_data in properties.items():
                if prop_data.get("type") == "title":
                    title_prop = prop_data
                    break
            
            if title_prop:
                title_array = title_prop.get("title", [])
                if title_array:
                    title = title_array[0].get("plain_text", "Untitled")
                else:
                    title = "Untitled"
            else:
                title = "Untitled"
            
            # Normalize title for comparison
            normalized = title.lower().strip()
            
            if normalized in seen_titles and normalized != "untitled":
                duplicates.append({
                    "title": title,
                    "page_id": page["id"],
                    "original_page_id": seen_titles[normalized],
                    "blocks": len(page.get("blocks", []))
                })
            else:
                seen_titles[normalized] = page["id"]
        
        if duplicates:
            print(f"   ⚠️  Found {len(duplicates)} potential duplicate(s)")
            for dup in duplicates:
                print(f"      • {dup['title']} ({dup['blocks']} blocks)")
        else:
            print(f"   ✅ No duplicates found")
        
        return duplicates
    
    def generate_enhancements(
        self,
        db_content: Dict[str, Any],
        local_content: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate enhancement suggestions based on content analysis.
        
        Args:
            db_content: Retrieved Notion database content
            local_content: Local folder content
            
        Returns:
            List of enhancement suggestions
        """
        print(f"\n✨ Generating enhancement suggestions...")
        
        enhancements = []
        db_title = db_content.get("title", "Database")
        
        # Suggest adding resources based on database type
        if "content" in db_title.lower() and "hub" in db_title.lower():
            enhancements.extend(self._suggest_content_hub_enhancements())
        
        elif "pillar" in db_title.lower():
            enhancements.extend(self._suggest_pillar_enhancements())
        
        elif "voice" in db_title.lower():
            enhancements.extend(self._suggest_voice_enhancements())
        
        elif "prompt" in db_title.lower():
            enhancements.extend(self._suggest_prompt_enhancements())
        
        elif "review" in db_title.lower() or "analytic" in db_title.lower():
            enhancements.extend(self._suggest_analytics_enhancements())
        
        # Check for empty pages
        pages = db_content.get("pages", [])
        empty_pages = [p for p in pages if p.get("block_count", 0) == 0]
        
        if empty_pages:
            enhancements.append({
                "type": "add_content",
                "priority": "high",
                "description": f"Found {len(empty_pages)} empty pages that need content",
                "action": "populate_empty_pages",
                "affected_pages": len(empty_pages)
            })
        
        print(f"   💡 Generated {len(enhancements)} enhancement suggestions")
        
        self.enhancement_suggestions = enhancements
        return enhancements
    
    def _suggest_content_hub_enhancements(self) -> List[Dict[str, Any]]:
        """Suggest enhancements for Content Hub database."""
        return [
            {
                "type": "add_resources",
                "priority": "high",
                "description": "Add LinkedIn best practices guide",
                "resources": [
                    {
                        "title": "LinkedIn Algorithm Guide 2025",
                        "url": "https://www.linkedin.com/help/linkedin/answer/a522735",
                        "type": "bookmark"
                    }
                ]
            },
            {
                "type": "add_template",
                "priority": "medium",
                "description": "Add content templates for common post types",
                "templates": [
                    "Personal Story Template",
                    "How-To Guide Template",
                    "Industry Insight Template",
                    "Question Post Template"
                ]
            },
            {
                "type": "add_checklist",
                "priority": "high",
                "description": "Add post optimization checklist",
                "checklist_items": [
                    "Hook grabs attention in first 3 seconds",
                    "Includes relevant hashtags (3-5)",
                    "Has clear call-to-action",
                    "Formatted with line breaks for readability",
                    "Includes engaging question or prompt",
                    "Tagged relevant people/companies",
                    "Scheduled for optimal posting time"
                ]
            }
        ]
    
    def _suggest_pillar_enhancements(self) -> List[Dict[str, Any]]:
        """Suggest enhancements for Content Pillars database."""
        return [
            {
                "type": "add_examples",
                "priority": "high",
                "description": "Add examples of successful pillar-based content strategies",
                "examples": [
                    "Tech industry leaders using expertise pillar",
                    "Personal brand builders using authenticity pillar",
                    "Entrepreneurs using lessons learned pillar"
                ]
            },
            {
                "type": "add_framework",
                "priority": "medium",
                "description": "Add content pillar framework guide",
                "framework": {
                    "name": "3-5 Pillar Rule",
                    "description": "Focus on 3-5 core topics for consistent brand positioning"
                }
            }
        ]
    
    def _suggest_voice_enhancements(self) -> List[Dict[str, Any]]:
        """Suggest enhancements for Voice Discovery database."""
        return [
            {
                "type": "add_exercises",
                "priority": "high",
                "description": "Add voice discovery exercises",
                "exercises": [
                    "Write 3 stories from your life that shaped your perspective",
                    "List 10 words that describe your personality",
                    "Identify 5 values you want to communicate",
                    "Analyze 3 creators whose voice resonates with you"
                ]
            }
        ]
    
    def _suggest_prompt_enhancements(self) -> List[Dict[str, Any]]:
        """Suggest enhancements for Prompt Library database."""
        return [
            {
                "type": "add_categories",
                "priority": "high",
                "description": "Organize prompts by use case",
                "categories": [
                    "Content Ideation",
                    "Hook Writing",
                    "Story Development",
                    "Call-to-Action Generation",
                    "Hashtag Research",
                    "Engagement Replies"
                ]
            }
        ]
    
    def _suggest_analytics_enhancements(self) -> List[Dict[str, Any]]:
        """Suggest enhancements for Analytics/Review database."""
        return [
            {
                "type": "add_metrics",
                "priority": "high",
                "description": "Add key metrics to track",
                "metrics": [
                    "Total Impressions",
                    "Engagement Rate",
                    "Profile Views",
                    "Connection Requests",
                    "Comments Received",
                    "Shares",
                    "Best Performing Content Type"
                ]
            }
        ]
    
    def export_analysis_report(self, output_file: str = None) -> str:
        """
        Export complete analysis report.
        
        Args:
            output_file: Optional output filename
            
        Returns:
            Path to exported file
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"notion_enhancement_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "databases_analyzed": len(self.retrieved_content),
            "enhancement_suggestions": self.enhancement_suggestions,
            "database_details": self.retrieved_content
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n📄 Report exported to: {output_file}")
        return output_file


def main():
    """Main execution function."""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        Notion Database Enhancement Tool                 ║
║        Retrieve • Analyze • Enhance                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    LOCAL_FOLDER = "/Users/tatiana/Cloning me/LinkedIn Content OS"
    
    LINKEDIN_DATABASES = {
        "Content Hub": "2830da0a-a5c8-8161-8619-f6b7fe525036",
        "Content Pillars": "2830da0a-a5c8-81e9-b0c3-f34424468ef2",
        "Voice Discovery": "2830da0a-a5c8-81c3-aa05-d39ee7302302",
        "Prompt Library": "2830da0a-a5c8-8105-adab-e20090bb6046",
        "Weekly Review": "2830da0a-a5c8-8192-ad18-edbbb3a3d471"
    }
    
    # Initialize enhancer
    enhancer = NotionEnhancer(LOCAL_FOLDER)
    
    # Step 1: Analyze local content
    print("\n" + "=" * 60)
    print("  STEP 1: Analyzing Local Content")
    print("=" * 60)
    
    local_content = enhancer.analyze_local_content()
    print(f"\n✅ Analyzed {len(local_content)} files")
    
    # Categorize files
    categories = {}
    for file_path, data in local_content.items():
        category = data["category"]
        categories[category] = categories.get(category, 0) + 1
    
    print("\n📊 Content by category:")
    for category, count in sorted(categories.items()):
        print(f"   • {category.capitalize()}: {count} files")
    
    # Step 2: Retrieve all databases
    print("\n" + "=" * 60)
    print("  STEP 2: Retrieving Notion Databases")
    print("=" * 60)
    
    all_db_content = {}
    
    for db_name, db_id in LINKEDIN_DATABASES.items():
        try:
            db_content = enhancer.retrieve_database_content(db_id)
            all_db_content[db_name] = db_content
            
            # Find duplicates
            duplicates = enhancer.find_duplicates(db_content)
            
            # Generate enhancements
            enhancements = enhancer.generate_enhancements(db_content, local_content)
            
            print(f"\n   📋 {db_name} Summary:")
            print(f"      • Pages: {db_content['total_pages']}")
            print(f"      • Properties: {len(db_content['properties'])}")
            print(f"      • Duplicates: {len(duplicates)}")
            print(f"      • Enhancement suggestions: {len(enhancements)}")
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"\n   ❌ Error processing {db_name}: {e}")
    
    # Step 3: Generate comprehensive report
    print("\n" + "=" * 60)
    print("  STEP 3: Generating Enhancement Report")
    print("=" * 60)
    
    report_file = enhancer.export_analysis_report()
    
    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    
    total_pages = sum(db.get("total_pages", 0) for db in all_db_content.values())
    total_suggestions = len(enhancer.enhancement_suggestions)
    
    print(f"""
📊 Databases Analyzed: {len(all_db_content)}
📄 Total Pages: {total_pages}
📁 Local Files: {len(local_content)}
💡 Enhancement Suggestions: {total_suggestions}
📄 Report: {report_file}

✅ Analysis Complete!
    """)
    
    print("\n💡 Next Steps:")
    print("   1. Review the enhancement report")
    print("   2. Use web search to find resources for suggested enhancements")
    print("   3. Apply enhancements to Notion databases")
    print("   4. Remove duplicate entries")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
