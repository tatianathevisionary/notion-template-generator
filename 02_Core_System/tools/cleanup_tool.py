#!/usr/bin/env python3
"""
Notion Cleanup Tool for MCP
Provides cleanup functionality for removing duplicate and unnecessary pages
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
    from dotenv import load_dotenv
    
    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
    
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

class NotionCleanupManager:
    """Manages cleanup of duplicate and unnecessary pages."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("Notion API key not found")
        
        self.client = Client(auth=self.api_key, notion_version="2025-09-03")
        
        # Define the correct categories we want to keep
        self.target_categories = {
            "🎯 Brand Strategy & Discovery": "🎯",
            "📝 Content Planning & Creation": "📝", 
            "📅 Content Calendar & Scheduling": "📅",
            "📈 Performance & Analytics": "📈",
            "🤖 Automation & Systems": "🤖"
        }
    
    def get_all_root_pages(self, root_page_id: str) -> List[Dict[str, Any]]:
        """Get all pages at the root level."""
        try:
            clean_root_id = root_page_id.replace("-", "")
            blocks_response = self.client.blocks.children.list(block_id=clean_root_id, page_size=100)
            
            pages = []
            for block in blocks_response.get("results", []):
                if block.get("type") == "child_page":
                    page_id = block["id"]
                    title = block.get("child_page", {}).get("title", "Untitled")
                    pages.append({"id": page_id, "title": title})
            
            return pages
            
        except Exception as e:
            print(f"❌ Error getting root pages: {e}")
            return []
    
    def migrate_content_to_target_category(self, source_page: Dict[str, Any], target_category_id: str) -> bool:
        """Migrate content from a source page by creating a proper subpage in the target category."""
        try:
            # Get the full content of the source page
            source_page_id = source_page["id"].replace("-", "")
            
            # Get all blocks from the source page
            blocks_response = self.client.blocks.children.list(block_id=source_page_id, page_size=100)
            source_blocks = blocks_response.get("results", [])
            
            # Get remaining blocks if paginated
            while blocks_response.get("has_more"):
                blocks_response = self.client.blocks.children.list(
                    block_id=source_page_id,
                    start_cursor=blocks_response.get("next_cursor"),
                    page_size=100
                )
                source_blocks.extend(blocks_response.get("results", []))
            
            if not source_blocks:
                print(f"   📄 No content to migrate from '{source_page['title']}'")
                return True
            
            # Filter and prepare blocks for migration
            migratable_blocks = []
            for block in source_blocks:
                block_type = block.get("type")
                
                # Skip child_page blocks as they should be handled separately
                if block_type == "child_page":
                    continue
                
                # Only migrate certain block types to avoid API issues
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", 
                                "bulleted_list_item", "numbered_list_item", "quote", 
                                "callout", "divider", "to_do", "code", "image", "video", 
                                "file", "bookmark", "embed", "table", "table_row"]:
                    try:
                        block_content = block.get(block_type, {})
                        if "rich_text" in block_content:
                            migratable_blocks.append({
                                "type": block_type,
                                block_type: {
                                    "rich_text": block_content["rich_text"],
                                    "color": block_content.get("color", "default")
                                }
                            })
                        elif block_type == "divider":
                            migratable_blocks.append({"type": "divider", "divider": {}})
                        elif block_type in ["image", "video", "file", "bookmark", "embed"]:
                            # Copy media blocks as-is (with limitations)
                            migratable_blocks.append({
                                "type": block_type,
                                block_type: block_content
                            })
                    except Exception as e:
                        print(f"   ⚠️  Skipping block due to error: {e}")
            
            if migratable_blocks:
                # Create a new subpage in the target category with the migrated content
                clean_target_id = target_category_id.replace("-", "")
                
                # Create the subpage
                subpage_response = self.client.pages.create(
                    parent={"type": "page_id", "page_id": clean_target_id},
                    properties={
                        "title": [{"type": "text", "text": {"content": source_page["title"]}}]
                    },
                    children=migratable_blocks[:50]  # Limit to avoid API limits
                )
                
                print(f"   ✅ Created subpage '{source_page['title']}' with {len(migratable_blocks)} blocks")
                return True
            else:
                print(f"   📄 No migratable content found in '{source_page['title']}'")
                return True
                
        except Exception as e:
            print(f"   ❌ Error migrating content from '{source_page['title']}': {e}")
            return False
    
    def find_target_category_for_page(self, page_title: str, all_pages: List[Dict[str, Any]]) -> Optional[str]:
        """Find the appropriate target category for a page based on its title."""
        # Create a mapping of category keywords to target category IDs
        category_mapping = {}
        
        for page in all_pages:
            title = page["title"]
            if title in self.target_categories:
                category_mapping[title] = page["id"]
        
        # Determine which category this page should go to based on keywords
        page_lower = page_title.lower()
        
        if any(keyword in page_lower for keyword in ["brand", "discovery", "voice", "identity", "strategy"]):
            return category_mapping.get("🎯 Brand Strategy & Discovery")
        elif any(keyword in page_lower for keyword in ["content", "pillar", "ideas", "creation", "planning"]):
            return category_mapping.get("📝 Content Planning & Creation")
        elif any(keyword in page_lower for keyword in ["calendar", "schedule", "timeline", "posting"]):
            return category_mapping.get("📅 Content Calendar & Scheduling")
        elif any(keyword in page_lower for keyword in ["performance", "tracking", "analytics", "metrics"]):
            return category_mapping.get("📈 Performance & Analytics")
        elif any(keyword in page_lower for keyword in ["automation", "workflow", "system", "agent"]):
            return category_mapping.get("🤖 Automation & Systems")
        
        # Default to Content Planning & Creation
        return category_mapping.get("📝 Content Planning & Creation")
    
    def migrate_child_pages_to_target_categories(self, source_page: Dict[str, Any], all_pages: List[Dict[str, Any]]) -> int:
        """Migrate child pages from a source page to appropriate target categories."""
        try:
            source_page_id = source_page["id"].replace("-", "")
            
            # Get child pages
            blocks_response = self.client.blocks.children.list(block_id=source_page_id)
            child_pages = []
            
            for block in blocks_response.get("results", []):
                if block.get("type") == "child_page":
                    child_page_id = block["id"]
                    child_title = block.get("child_page", {}).get("title", "Untitled")
                    child_pages.append({"id": child_page_id, "title": child_title})
            
            migrated_count = 0
            
            for child_page in child_pages:
                # Find appropriate target category
                target_category_id = self.find_target_category_for_page(child_page["title"], all_pages)
                
                if target_category_id:
                    try:
                        # Move the child page to the target category
                        clean_child_id = child_page["id"].replace("-", "")
                        clean_target_id = target_category_id.replace("-", "")
                        
                        self.client.pages.update(
                            page_id=clean_child_id,
                            parent={"type": "page_id", "page_id": clean_target_id}
                        )
                        
                        print(f"   📄 Migrated child page '{child_page['title']}' to target category")
                        migrated_count += 1
                        
                    except Exception as e:
                        print(f"   ❌ Failed to migrate child page '{child_page['title']}': {e}")
            
            return migrated_count
            
        except Exception as e:
            print(f"   ❌ Error migrating child pages from '{source_page['title']}': {e}")
            return 0
    
    def delete_page(self, page_id: str, title: str) -> bool:
        """Delete a page by archiving it (moving to trash)."""
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Archive the page using the correct parameter
            response = self.client.pages.update(
                page_id=clean_page_id,
                archived=True
            )
            
            return True
            
        except APIResponseError as e:
            print(f"❌ API Error archiving '{title}': {e}")
            return False
        except Exception as e:
            print(f"❌ Error archiving '{title}': {e}")
            return False
    
    def is_page_empty_or_duplicate(self, page: Dict[str, Any]) -> bool:
        """Check if a page is empty or contains only duplicate/minimal content."""
        try:
            page_id = page["id"].replace("-", "")
            
            # Get all blocks from the page
            blocks_response = self.client.blocks.children.list(block_id=page_id, page_size=100)
            blocks = blocks_response.get("results", [])
            
            # Count meaningful content blocks
            content_blocks = 0
            total_text_length = 0
            
            for block in blocks:
                block_type = block.get("type")
                
                # Skip child_page blocks for this count
                if block_type == "child_page":
                    continue
                
                # Count blocks with actual content
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", 
                                "bulleted_list_item", "numbered_list_item", "quote", 
                                "callout", "to_do", "code"]:
                    block_content = block.get(block_type, {})
                    rich_text = block_content.get("rich_text", [])
                    
                    # Extract text content
                    text_content = ""
                    for rt in rich_text:
                        text_content += rt.get("text", {}).get("content", "")
                    
                    if text_content.strip():
                        content_blocks += 1
                        total_text_length += len(text_content.strip())
                
                elif block_type in ["image", "video", "file", "bookmark", "embed", "divider"]:
                    content_blocks += 1
            
            # Consider page empty if:
            # 1. No content blocks at all
            # 2. Very minimal content (less than 50 characters total)
            # 3. Only generic/template content
            is_empty = (
                content_blocks == 0 or 
                total_text_length < 50 or
                (content_blocks <= 2 and total_text_length < 100)
            )
            
            return is_empty
            
        except Exception as e:
            print(f"   ⚠️  Error checking if page is empty: {e}")
            return False
    
    def identify_pages_to_delete(self, all_pages: List[Dict[str, Any]]) -> tuple:
        """Identify which pages should be deleted."""
        pages_to_delete = []
        pages_to_keep = []
        
        # Track which target categories we've found
        found_categories = set()
        
        for page in all_pages:
            title = page["title"]
            
            # Check if this is one of our target categories
            is_target_category = False
            for target_name, target_emoji in self.target_categories.items():
                if target_name == title:
                    is_target_category = True
                    found_categories.add(target_name)
                    pages_to_keep.append(page)
                    break
            
            if not is_target_category:
                # Check if it's a duplicate or old category
                is_duplicate_category = False
                
                # Look for similar category names or old categories
                category_keywords = [
                    "Brand Strategy", "Content Planning", "Content Creation",
                    "Calendar", "Scheduling", "Performance", "Analytics", 
                    "Automation", "Systems", "Strategy & Performance",
                    "Performance & Automation", "Content Management"
                ]
                
                for keyword in category_keywords:
                    if keyword.lower() in title.lower():
                        is_duplicate_category = True
                        break
                
                # Also check for pages that look like categories but aren't our targets
                if any(emoji in title for emoji in ["🎯", "📝", "📅", "📈", "🤖", "❤️", "📋", "🚀", "🗄️"]) and title not in self.target_categories:
                    is_duplicate_category = True
                
                if is_duplicate_category:
                    pages_to_delete.append(page)
                elif self.is_page_empty_or_duplicate(page):
                    # Also delete empty or minimal content pages
                    pages_to_delete.append(page)
                    print(f"   🗑️  '{page['title']}' marked for deletion (empty/minimal content)")
                else:
                    # Keep other pages (they might be legitimate content)
                    pages_to_keep.append(page)
        
        return pages_to_delete, pages_to_keep, found_categories
    
    def analyze_cleanup_needed(self, root_page_id: str) -> Dict[str, Any]:
        """Analyze what cleanup is needed without executing it."""
        try:
            # Get all pages at root level
            all_pages = self.get_all_root_pages(root_page_id)
            
            # Identify what needs cleanup
            pages_to_delete, pages_to_keep, found_categories = self.identify_pages_to_delete(all_pages)
            
            return {
                "status": "success",
                "analysis": {
                    "total_pages": len(all_pages),
                    "pages_to_delete": len(pages_to_delete),
                    "pages_to_keep": len(pages_to_keep),
                    "target_categories_found": len(found_categories),
                    "cleanup_needed": len(pages_to_delete) > 0
                },
                "pages_to_delete": [{"title": p["title"], "id": p["id"]} for p in pages_to_delete],
                "pages_to_keep": [{"title": p["title"], "id": p["id"]} for p in pages_to_keep],
                "found_categories": list(found_categories),
                "message": f"Found {len(pages_to_delete)} pages that need cleanup"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error analyzing cleanup: {e}"
            }
    
    def execute_cleanup(self, root_page_id: str, confirm_deletion: bool = False) -> Dict[str, Any]:
        """Execute the cleanup process."""
        try:
            if not confirm_deletion:
                return {
                    "status": "error",
                    "message": "Cleanup not executed. Set confirm_deletion=True to proceed."
                }
            
            # Get analysis first
            analysis_result = self.analyze_cleanup_needed(root_page_id)
            if analysis_result["status"] != "success":
                return analysis_result
            
            pages_to_delete = analysis_result["pages_to_delete"]
            all_pages = self.get_all_root_pages(root_page_id)  # Get all pages for reference
            
            if not pages_to_delete:
                return {
                    "status": "success",
                    "message": "No cleanup needed - workspace is already clean",
                    "results": {
                        "deleted_count": 0,
                        "failed_count": 0,
                        "remaining_count": analysis_result["analysis"]["pages_to_keep"]
                    }
                }
            
            # Execute deletions with content migration
            deleted_count = 0
            failed_count = 0
            migrated_content_count = 0
            migrated_child_pages_count = 0
            failed_pages = []
            
            for page in pages_to_delete:
                print(f"\n🔄 Processing '{page['title']}'...")
                
                # Step 1: Migrate child pages to appropriate categories
                child_pages_migrated = self.migrate_child_pages_to_target_categories(page, all_pages)
                migrated_child_pages_count += child_pages_migrated
                
                # Step 2: Migrate content to appropriate target category
                target_category_id = self.find_target_category_for_page(page["title"], all_pages)
                if target_category_id:
                    if self.migrate_content_to_target_category(page, target_category_id):
                        migrated_content_count += 1
                
                # Step 3: Delete the now-empty duplicate page
                if self.delete_page(page["id"], page["title"]):
                    deleted_count += 1
                    print(f"🗑️  Deleted '{page['title']}' after migration")
                    time.sleep(0.5)  # Brief pause between deletions
                else:
                    failed_count += 1
                    failed_pages.append(page["title"])
            
            # Wait for API sync and verify
            time.sleep(2)
            remaining_pages = self.get_all_root_pages(root_page_id)
            
            return {
                "status": "success",
                "message": f"Cleanup completed: {deleted_count} pages deleted, {migrated_content_count} content migrated, {migrated_child_pages_count} child pages migrated",
                "results": {
                    "deleted_count": deleted_count,
                    "failed_count": failed_count,
                    "remaining_count": len(remaining_pages),
                    "migrated_content_count": migrated_content_count,
                    "migrated_child_pages_count": migrated_child_pages_count,
                    "failed_pages": failed_pages,
                    "success_rate": (deleted_count / len(pages_to_delete)) * 100 if pages_to_delete else 100
                },
                "remaining_pages": [{"title": p["title"], "id": p["id"]} for p in remaining_pages]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during cleanup: {e}"
            }
    
    def fix_emoji_consistency(self, root_page_id: str) -> Dict[str, Any]:
        """Fix emoji consistency in category titles."""
        try:
            all_pages = self.get_all_root_pages(root_page_id)
            fixed_count = 0
            
            for page in all_pages:
                title = page["title"]
                page_id = page["id"]
                
                # Check if this page needs emoji fixing
                new_title = None
                
                for target_name, target_emoji in self.target_categories.items():
                    # If the title matches a target category but has wrong emoji
                    if target_name.split(" ", 1)[1] in title and not title.startswith(target_emoji):
                        new_title = target_name
                        break
                
                if new_title and new_title != title:
                    try:
                        clean_page_id = page_id.replace("-", "")
                        self.client.pages.update(
                            page_id=clean_page_id,
                            properties={
                                "title": [{"type": "text", "text": {"content": new_title}}]
                            }
                        )
                        fixed_count += 1
                        print(f"🎨 Fixed emoji: '{title}' → '{new_title}'")
                    except Exception as e:
                        print(f"❌ Failed to fix emoji for '{title}': {e}")
            
            return {
                "status": "success",
                "message": f"Fixed emoji consistency for {fixed_count} pages",
                "fixed_count": fixed_count
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error fixing emoji consistency: {e}"
            }

# MCP Tool Functions
def analyze_workspace_cleanup(root_page_id: str) -> Dict[str, Any]:
    """Analyze what cleanup is needed in the workspace without executing it."""
    try:
        cleanup_manager = NotionCleanupManager()
        return cleanup_manager.analyze_cleanup_needed(root_page_id)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error analyzing cleanup: {e}"
        }

def execute_workspace_cleanup(root_page_id: str, confirm_deletion: bool = False) -> Dict[str, Any]:
    """Execute cleanup of duplicate and unnecessary pages."""
    try:
        cleanup_manager = NotionCleanupManager()
        return cleanup_manager.execute_cleanup(root_page_id, confirm_deletion)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error executing cleanup: {e}"
        }

def fix_emoji_consistency(root_page_id: str) -> Dict[str, Any]:
    """Fix emoji consistency in category page titles."""
    try:
        cleanup_manager = NotionCleanupManager()
        return cleanup_manager.fix_emoji_consistency(root_page_id)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fixing emoji consistency: {e}"
        }
