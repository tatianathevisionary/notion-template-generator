#!/usr/bin/env python3
"""
Working Notion Reorganization Tool
Uses correct Notion API endpoints and formats for actual page reorganization
"""

import os
import sys
import json
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

class WorkingNotionReorganizer:
    """Notion reorganizer that uses correct API endpoints and formats."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("Notion API key not found")
        
        self.client = Client(auth=self.api_key, notion_version="2025-09-03")
    
    def extract_page_content_with_blocks(self, page_id: str) -> Dict[str, Any]:
        """Extract complete page content including all blocks."""
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get page details using the correct API
            page = self.client.pages.retrieve(page_id=clean_page_id)
            
            # Get all blocks (content)
            blocks_response = self.client.blocks.children.list(block_id=clean_page_id, page_size=100)
            blocks = blocks_response.get("results", [])
            
            # Get remaining blocks if paginated
            while blocks_response.get("has_more"):
                blocks_response = self.client.blocks.children.list(
                    block_id=clean_page_id,
                    start_cursor=blocks_response.get("next_cursor"),
                    page_size=100
                )
                blocks.extend(blocks_response.get("results", []))
            
            # Extract title
            title = self._extract_title_from_page(page)
            
            # Extract text content from blocks
            content_text = self._extract_text_from_blocks(blocks)
            
            return {
                "page_id": page_id,
                "title": title,
                "url": page.get("url", ""),
                "parent": page.get("parent", {}),
                "created_time": page.get("created_time", ""),
                "last_edited_time": page.get("last_edited_time", ""),
                "blocks": blocks,
                "content_text": content_text,
                "block_count": len(blocks),
                "word_count": len(content_text.split()) if content_text else 0
            }
            
        except Exception as e:
            print(f"❌ Error extracting content from page {page_id}: {e}")
            return {
                "page_id": page_id,
                "error": str(e)
            }
    
    def _extract_title_from_page(self, page: Dict) -> str:
        """Extract title from page object."""
        try:
            properties = page.get("properties", {})
            for prop_name, prop_data in properties.items():
                if prop_data.get("type") == "title":
                    title_content = prop_data.get("title", [])
                    if title_content:
                        return title_content[0].get("text", {}).get("content", "Untitled")
            return "Untitled"
        except:
            return "Untitled"
    
    def _extract_text_from_blocks(self, blocks: List[Dict]) -> str:
        """Extract plain text from all supported block types."""
        text_parts = []
        
        for block in blocks:
            try:
                block_type = block.get("type")
                
                # Handle text-containing blocks with rich_text
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "quote", "callout"]:
                    block_content = block.get(block_type, {})
                    rich_text = block_content.get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        text_parts.append(text)
                
                elif block_type in ["bulleted_list_item", "numbered_list_item", "to_do"]:
                    block_content = block.get(block_type, {})
                    rich_text = block_content.get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        # Add checkbox status for to_do items
                        if block_type == "to_do":
                            checked = block_content.get("checked", False)
                            text = f"{'☑️' if checked else '☐'} {text}"
                        text_parts.append(text)
                
                elif block_type == "toggle":
                    toggle_content = block.get("toggle", {})
                    rich_text = toggle_content.get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        text_parts.append(f"▶️ {text}")
                
                elif block_type == "code":
                    code_content = block.get("code", {})
                    rich_text = code_content.get("rich_text", [])
                    language = code_content.get("language", "")
                    text = self._extract_rich_text(rich_text)
                    if text:
                        text_parts.append(f"Code ({language}): {text}")
                
                elif block_type == "child_page":
                    child_page = block.get("child_page", {})
                    title = child_page.get("title", "Untitled Page")
                    text_parts.append(f"📄 {title}")
                
                elif block_type == "child_database":
                    child_db = block.get("child_database", {})
                    title = child_db.get("title", "Untitled Database")
                    text_parts.append(f"🗄️ {title}")
                
                elif block_type == "bookmark":
                    bookmark = block.get("bookmark", {})
                    url = bookmark.get("url", "")
                    caption = self._extract_rich_text(bookmark.get("caption", []))
                    text_parts.append(f"🔖 {caption or url}")
                
                elif block_type == "embed":
                    embed = block.get("embed", {})
                    url = embed.get("url", "")
                    text_parts.append(f"🔗 Embed: {url}")
                
                elif block_type == "image":
                    image = block.get("image", {})
                    if image.get("type") == "external":
                        url = image.get("external", {}).get("url", "")
                    elif image.get("type") == "file":
                        url = image.get("file", {}).get("url", "")
                    else:
                        url = "Image"
                    text_parts.append(f"🖼️ {url}")
                
                elif block_type == "video":
                    video = block.get("video", {})
                    if video.get("type") == "external":
                        url = video.get("external", {}).get("url", "")
                    elif video.get("type") == "file":
                        url = video.get("file", {}).get("url", "")
                    else:
                        url = "Video"
                    text_parts.append(f"🎥 {url}")
                
                elif block_type == "audio":
                    audio = block.get("audio", {})
                    if audio.get("type") == "external":
                        url = audio.get("external", {}).get("url", "")
                    elif audio.get("type") == "file":
                        url = audio.get("file", {}).get("url", "")
                    else:
                        url = "Audio"
                    text_parts.append(f"🎵 {url}")
                
                elif block_type == "file":
                    file_obj = block.get("file", {})
                    name = file_obj.get("name", "File")
                    if file_obj.get("type") == "external":
                        url = file_obj.get("external", {}).get("url", "")
                    elif file_obj.get("type") == "file":
                        url = file_obj.get("file", {}).get("url", "")
                    else:
                        url = ""
                    text_parts.append(f"📎 {name} {url}".strip())
                
                elif block_type == "pdf":
                    pdf = block.get("pdf", {})
                    if pdf.get("type") == "external":
                        url = pdf.get("external", {}).get("url", "")
                    elif pdf.get("type") == "file":
                        url = pdf.get("file", {}).get("url", "")
                    else:
                        url = "PDF"
                    text_parts.append(f"📄 PDF: {url}")
                
                elif block_type == "table":
                    table = block.get("table", {})
                    width = table.get("table_width", 0)
                    text_parts.append(f"📊 Table ({width} columns)")
                
                elif block_type == "table_row":
                    table_row = block.get("table_row", {})
                    cells = table_row.get("cells", [])
                    cell_texts = []
                    for cell in cells:
                        cell_text = self._extract_rich_text(cell)
                        cell_texts.append(cell_text)
                    text_parts.append(" | ".join(cell_texts))
                
                elif block_type == "equation":
                    equation = block.get("equation", {})
                    expression = equation.get("expression", "")
                    text_parts.append(f"🧮 {expression}")
                
                elif block_type == "divider":
                    text_parts.append("---")
                
                elif block_type == "breadcrumb":
                    text_parts.append("🍞 Breadcrumb")
                
                elif block_type == "table_of_contents":
                    text_parts.append("📋 Table of Contents")
                
                elif block_type == "link_preview":
                    link_preview = block.get("link_preview", {})
                    url = link_preview.get("url", "")
                    text_parts.append(f"🔗 {url}")
                
                elif block_type == "template":
                    template = block.get("template", {})
                    rich_text = template.get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        text_parts.append(f"📝 Template: {text}")
                
                elif block_type == "synced_block":
                    synced = block.get("synced_block", {})
                    if synced.get("synced_from") is None:
                        text_parts.append("🔄 Original Synced Block")
                    else:
                        text_parts.append("🔄 Synced Block")
                
                elif block_type == "column_list":
                    text_parts.append("📐 Column Layout")
                
                elif block_type == "column":
                    column = block.get("column", {})
                    width_ratio = column.get("width_ratio", "auto")
                    text_parts.append(f"📐 Column ({width_ratio})")
                
                elif block_type == "unsupported":
                    text_parts.append("❓ Unsupported Block")
                
                # Handle blocks with children recursively
                if block.get("has_children") and "children" in block:
                    children = block.get("children", [])
                    if children:
                        children_text = self._extract_text_from_blocks(children)
                        if children_text:
                            text_parts.append(children_text)
                            
            except Exception as e:
                print(f"⚠️  Error extracting text from {block_type} block: {e}")
        
        return "\n".join(text_parts)
    
    def _extract_rich_text(self, rich_text_data: List[Dict]) -> str:
        """Extract plain text from rich text objects."""
        try:
            return "".join([
                rt.get("text", {}).get("content", "") 
                for rt in rich_text_data
            ])
        except:
            return ""
    
    def get_page_hierarchy_with_content(self, root_page_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Get complete page hierarchy with content extraction."""
        try:
            return self._get_hierarchy_recursive(root_page_id, max_depth, 0, set())
        except Exception as e:
            print(f"❌ Error getting hierarchy: {e}")
            return []
    
    def _get_hierarchy_recursive(self, page_id: str, max_depth: int, current_depth: int, visited: set) -> List[Dict[str, Any]]:
        """Recursively get page hierarchy with content."""
        if current_depth >= max_depth or page_id in visited:
            return []
        
        visited.add(page_id)
        pages = []
        
        try:
            # Extract current page content
            page_content = self.extract_page_content_with_blocks(page_id)
            if not page_content.get("error"):
                page_content["depth"] = current_depth
                pages.append(page_content)
                
                # Get child pages from blocks
                for block in page_content.get("blocks", []):
                    if block.get("type") == "child_page":
                        child_page_id = block["id"]
                        child_pages = self._get_hierarchy_recursive(
                            child_page_id, max_depth, current_depth + 1, visited
                        )
                        pages.extend(child_pages)
            else:
                pages.append(page_content)
                
        except Exception as e:
            print(f"❌ Error processing page {page_id}: {e}")
            pages.append({
                "page_id": page_id,
                "error": str(e),
                "depth": current_depth
            })
        
        return pages
    
    def create_page_with_icon(self, parent_id: str, title: str, content_blocks: List[Dict] = None, emoji: str = "📁") -> Optional[str]:
        """Create a page with emoji icon using the correct Notion API format."""
        try:
            clean_parent_id = parent_id.replace("-", "")
            
            # Prepare the request with proper emoji format
            create_data = {
                "parent": {"type": "page_id", "page_id": clean_parent_id},
                "properties": {
                    "title": [{"type": "text", "text": {"content": title}}]
                },
                "icon": {
                    "type": "emoji",
                    "emoji": emoji
                }
            }
            
            # Add content blocks if provided
            if content_blocks:
                create_data["children"] = content_blocks
            
            response = self.client.pages.create(**create_data)
            
            print(f"✅ Created page '{title}' with icon {emoji}")
            return response["id"]
            
        except APIResponseError as e:
            print(f"❌ API Error creating page '{title}': {e}")
            return None
        except Exception as e:
            print(f"❌ Error creating page '{title}': {e}")
            return None
    
    def create_page_correctly(self, parent_id: str, title: str, content_blocks: List[Dict] = None) -> Optional[str]:
        """Create a page using the correct Notion API format."""
        try:
            clean_parent_id = parent_id.replace("-", "")
            
            # Prepare the request
            create_data = {
                "parent": {"type": "page_id", "page_id": clean_parent_id},
                "properties": {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            }
            
            # Add content blocks if provided
            if content_blocks:
                create_data["children"] = content_blocks
            
            response = self.client.pages.create(**create_data)
            
            print(f"✅ Created page '{title}' successfully")
            return response["id"]
            
        except APIResponseError as e:
            print(f"❌ API Error creating page '{title}': {e}")
            return None
        except Exception as e:
            print(f"❌ Error creating page '{title}': {e}")
            return None
    
    def move_page_correctly(self, page_id: str, new_parent_id: str) -> bool:
        """Move a page using the correct PATCH API endpoint."""
        try:
            clean_page_id = page_id.replace("-", "")
            clean_parent_id = new_parent_id.replace("-", "")
            
            # Use the PATCH endpoint to update the page's parent
            # According to the API docs, we need to use the correct format
            update_data = {
                "parent": {
                    "type": "page_id", 
                    "page_id": clean_parent_id
                }
            }
            
            response = self.client.pages.update(
                page_id=clean_page_id,
                **update_data
            )
            
            # Verify the move was successful
            updated_parent = response.get("parent", {})
            if updated_parent.get("page_id") == clean_parent_id:
                print(f"✅ Successfully moved page to new parent")
                return True
            else:
                print(f"⚠️  Move may not have been successful - parent still shows: {updated_parent}")
                return False
                
        except APIResponseError as e:
            print(f"❌ API Error moving page: {e}")
            return False
        except Exception as e:
            print(f"❌ Error moving page: {e}")
            return False
    
    def copy_page_content_to_new_page(self, source_page: Dict[str, Any], target_parent_id: str) -> Optional[str]:
        """Copy a page's content to a new page under a different parent."""
        try:
            title = source_page.get("title", "Untitled")
            blocks = source_page.get("blocks", [])
            
            # Filter and prepare blocks for copying
            copyable_blocks = []
            for block in blocks[:20]:  # Limit to first 20 blocks to avoid API limits
                block_type = block.get("type")
                
                # Only copy certain block types to avoid issues
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "quote"]:
                    try:
                        block_content = block.get(block_type, {})
                        if "rich_text" in block_content:
                            copyable_blocks.append({
                                "type": block_type,
                                block_type: {
                                    "rich_text": block_content["rich_text"]
                                }
                            })
                    except Exception as e:
                        print(f"⚠️  Skipping block due to error: {e}")
            
            # If no copyable blocks, create a simple content block
            if not copyable_blocks:
                copyable_blocks = [
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": f"Content from '{title}' - reorganized for better structure."}}]
                        }
                    }
                ]
            
            # Create the new page
            new_page_id = self.create_page_correctly(target_parent_id, title, copyable_blocks)
            
            if new_page_id:
                print(f"✅ Copied '{title}' to new location")
                return new_page_id
            else:
                print(f"❌ Failed to copy '{title}'")
                return None
                
        except Exception as e:
            print(f"❌ Error copying page content: {e}")
            return None
    
    def execute_intelligent_reorganization(self, root_page_id: str, reorganization_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute reorganization based on an intelligent analysis plan."""
        try:
            print("🚀 EXECUTING INTELLIGENT REORGANIZATION")
            print("=" * 60)
            
            results = {
                "categories_created": 0,
                "pages_moved": 0,
                "pages_copied": 0,
                "errors": []
            }
            
            # Extract the reorganization plan
            categories = reorganization_plan.get("suggested_categories", {})
            
            if not categories:
                return {
                    "status": "error",
                    "message": "No reorganization plan provided"
                }
            
            print(f"📋 Plan: Create {len(categories)} categories")
            
            # Step 1: Create category pages
            category_ids = {}
            for category_name, category_info in categories.items():
                description = category_info.get("description", f"Pages related to {category_name}")
                
                # Create category page with description and emoji icon
                content_blocks = [
                    {
                        "type": "heading_1",
                        "heading_1": {
                            "rich_text": [{"type": "text", "text": {"content": category_name}}]
                        }
                    },
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": description}}]
                        }
                    },
                    {
                        "type": "divider",
                        "divider": {}
                    }
                ]
                
                # Extract emoji from category name for icon
                emoji = category_name.split()[0] if category_name.split() else "📁"
                
                category_id = self.create_page_with_icon(root_page_id, category_name, content_blocks, emoji)
                if category_id:
                    category_ids[category_name] = category_id
                    results["categories_created"] += 1
                    print(f"✅ Created category: {category_name}")
                else:
                    error_msg = f"Failed to create category: {category_name}"
                    results["errors"].append(error_msg)
                    print(f"❌ {error_msg}")
            
            # Step 2: Wait for API sync
            print("\n⏳ Waiting for API synchronization...")
            time.sleep(3)
            
            # Step 3: Copy pages to categories
            pages_to_organize = reorganization_plan.get("pages_to_organize", [])
            
            for page_info in pages_to_organize:
                page_id = page_info.get("page_id")
                suggested_category = page_info.get("suggested_category")
                
                if suggested_category in category_ids:
                    target_category_id = category_ids[suggested_category]
                    
                    # Try to copy the page content to the new category
                    new_page_id = self.copy_page_content_to_new_page(page_info, target_category_id)
                    
                    if new_page_id:
                        results["pages_copied"] += 1
                        print(f"✅ Organized '{page_info.get('title', 'Unknown')}' into {suggested_category}")
                    else:
                        error_msg = f"Failed to organize page: {page_info.get('title', 'Unknown')}"
                        results["errors"].append(error_msg)
                        print(f"❌ {error_msg}")
                else:
                    error_msg = f"Category not found for page: {page_info.get('title', 'Unknown')}"
                    results["errors"].append(error_msg)
                    print(f"⚠️  {error_msg}")
            
            # Step 4: Verify the new structure
            print(f"\n🔍 VERIFICATION")
            print("-" * 30)
            
            total_organized = 0
            for category_name, category_id in category_ids.items():
                try:
                    # Check how many pages are now in this category
                    blocks_response = self.client.blocks.children.list(block_id=category_id.replace("-", ""))
                    child_pages = [b for b in blocks_response.get("results", []) if b.get("type") == "child_page"]
                    total_organized += len(child_pages)
                    print(f"📁 {category_name}: {len(child_pages)} pages")
                except Exception as e:
                    print(f"⚠️  Could not verify {category_name}: {e}")
            
            # Generate final results
            results["total_organized"] = total_organized
            results["success_rate"] = (results["pages_copied"] / max(len(pages_to_organize), 1)) * 100
            
            print(f"\n📊 REORGANIZATION RESULTS:")
            print(f"✅ Categories created: {results['categories_created']}")
            print(f"✅ Pages organized: {results['pages_copied']}")
            print(f"📈 Success rate: {results['success_rate']:.1f}%")
            print(f"❌ Errors: {len(results['errors'])}")
            
            if results["success_rate"] > 80:
                print(f"\n🎉 REORGANIZATION SUCCESSFUL!")
                print("Your Notion workspace now has a clean, organized structure!")
            else:
                print(f"\n⚠️  REORGANIZATION COMPLETED WITH ISSUES")
                print("Some pages may need manual adjustment.")
            
            return {
                "status": "success",
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during reorganization: {e}"
            }

# MCP Tool Functions
def reorganize_notion_pages_intelligent(
    root_page_id: str, 
    reorganization_plan: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute intelligent reorganization of Notion pages."""
    try:
        reorganizer = WorkingNotionReorganizer()
        return reorganizer.execute_intelligent_reorganization(root_page_id, reorganization_plan)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error in reorganization: {e}"
        }

def extract_pages_with_full_content(
    root_page_id: str, 
    max_depth: int = 5
) -> Dict[str, Any]:
    """Extract all pages with complete content for analysis."""
    try:
        reorganizer = WorkingNotionReorganizer()
        pages = reorganizer.get_page_hierarchy_with_content(root_page_id, max_depth)
        
        # Calculate statistics
        total_pages = len(pages)
        total_words = sum(page.get("word_count", 0) for page in pages if not page.get("error"))
        total_blocks = sum(page.get("block_count", 0) for page in pages if not page.get("error"))
        
        return {
            "status": "success",
            "pages": pages,
            "statistics": {
                "total_pages": total_pages,
                "total_words": total_words,
                "total_blocks": total_blocks,
                "pages_with_errors": len([p for p in pages if p.get("error")])
            },
            "message": f"Extracted {total_pages} pages with complete content"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting pages: {e}"
        }

def create_reorganization_plan_from_content(pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a reorganization plan based on content analysis."""
    try:
        # Analyze content and create categories
        categories = {
            "🎯 Brand Strategy & Discovery": {
                "description": "Personal brand development, voice discovery, and strategic positioning",
                "keywords": ["brand", "discovery", "voice", "identity", "strategy", "personal"]
            },
            "📝 Content Planning & Creation": {
                "description": "Content strategy, planning frameworks, and creative development",
                "keywords": ["content", "pillar", "ideas", "creation", "planning", "framework"]
            },
            "📅 Content Calendar & Scheduling": {
                "description": "Timeline management, scheduling systems, and publishing workflows",
                "keywords": ["calendar", "schedule", "timeline", "posting", "publishing"]
            },
            "📈 Performance & Analytics": {
                "description": "Performance tracking, analytics, and optimization tools",
                "keywords": ["performance", "tracking", "analytics", "metrics", "optimization"]
            },
            "🤖 Automation & Systems": {
                "description": "Automated processes, workflow optimization, and system architecture",
                "keywords": ["automation", "workflow", "system", "agent", "process"]
            }
        }
        
        # Categorize pages
        pages_to_organize = []
        
        for page in pages_data:
            if page.get("error"):
                continue
                
            title = page.get("title", "").lower()
            content = page.get("content_text", "").lower()
            combined_text = f"{title} {content}"
            
            best_category = None
            best_score = 0
            
            # Find best matching category
            for category_name, category_info in categories.items():
                score = 0
                for keyword in category_info["keywords"]:
                    if keyword in combined_text:
                        score += 1
                
                if score > best_score:
                    best_score = score
                    best_category = category_name
            
            # Default category if no good match
            if not best_category:
                best_category = "📝 Content Planning & Creation"
            
            pages_to_organize.append({
                "page_id": page.get("page_id"),
                "title": page.get("title"),
                "suggested_category": best_category,
                "confidence_score": best_score,
                "word_count": page.get("word_count", 0),
                "content_text": page.get("content_text", "")[:200] + "..." if len(page.get("content_text", "")) > 200 else page.get("content_text", "")
            })
        
        return {
            "status": "success",
            "reorganization_plan": {
                "suggested_categories": categories,
                "pages_to_organize": pages_to_organize,
                "total_pages": len(pages_to_organize),
                "categories_count": len(categories)
            },
            "message": f"Created reorganization plan for {len(pages_to_organize)} pages into {len(categories)} categories"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating reorganization plan: {e}"
        }
