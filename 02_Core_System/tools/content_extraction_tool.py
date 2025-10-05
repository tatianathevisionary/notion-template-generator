#!/usr/bin/env python3
"""
Content Extraction Tool for Notion Template Generator MCP
Comprehensive content retrieval from Notion pages including blocks, properties, and metadata
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from notion_client import Client
    from dotenv import load_dotenv
    
    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
    
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

class NotionContentExtractor:
    """Comprehensive content extraction from Notion pages."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("Notion API key not found")
        
        self.client = Client(auth=self.api_key, notion_version="2025-09-03")
    
    def extract_page_content_full(self, page_id: str) -> Dict[str, Any]:
        """Extract complete page content including properties, blocks, and metadata."""
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get page details
            page = self.client.pages.retrieve(page_id=clean_page_id)
            
            # Get page blocks (content)
            blocks = self.client.blocks.children.list(block_id=clean_page_id, page_size=100)
            
            # Extract all content
            content_data = {
                "page_id": page_id,
                "title": self._extract_title(page),
                "url": page.get("url", ""),
                "created_time": page.get("created_time", ""),
                "last_edited_time": page.get("last_edited_time", ""),
                "parent": page.get("parent", {}),
                "properties": self._extract_all_properties(page),
                "blocks": self._extract_all_blocks(blocks.get("results", [])),
                "content_text": "",  # Will be populated
                "metadata": {
                    "total_blocks": len(blocks.get("results", [])),
                    "extraction_time": datetime.now().isoformat(),
                    "has_children": blocks.get("has_more", False)
                }
            }
            
            # Extract plain text content
            content_data["content_text"] = self._extract_plain_text_from_blocks(content_data["blocks"])
            
            # Get additional pages if has_more
            if blocks.get("has_more"):
                content_data["blocks"].extend(self._get_remaining_blocks(clean_page_id, blocks.get("next_cursor")))
                content_data["content_text"] = self._extract_plain_text_from_blocks(content_data["blocks"])
                content_data["metadata"]["total_blocks"] = len(content_data["blocks"])
            
            return content_data
            
        except Exception as e:
            print(f"❌ Error extracting content from page {page_id}: {e}")
            return {
                "page_id": page_id,
                "error": str(e),
                "extraction_time": datetime.now().isoformat()
            }
    
    def _get_remaining_blocks(self, page_id: str, start_cursor: str) -> List[Dict]:
        """Get remaining blocks if pagination is needed."""
        all_blocks = []
        cursor = start_cursor
        
        try:
            while cursor:
                response = self.client.blocks.children.list(
                    block_id=page_id,
                    start_cursor=cursor,
                    page_size=100
                )
                all_blocks.extend(response.get("results", []))
                cursor = response.get("next_cursor")
                
                if not response.get("has_more"):
                    break
                    
        except Exception as e:
            print(f"⚠️  Error getting remaining blocks: {e}")
        
        return all_blocks
    
    def _extract_title(self, page: Dict) -> str:
        """Extract title from page."""
        try:
            if "properties" in page and "title" in page["properties"]:
                title_prop = page["properties"]["title"]
                if "title" in title_prop and title_prop["title"]:
                    return title_prop["title"][0].get("text", {}).get("content", "Untitled")
            return "Untitled"
        except:
            return "Untitled"
    
    def _extract_all_properties(self, page: Dict) -> Dict[str, Any]:
        """Extract all page properties."""
        properties = {}
        
        try:
            for prop_name, prop_data in page.get("properties", {}).items():
                prop_type = prop_data.get("type")
                properties[prop_name] = {
                    "type": prop_type,
                    "id": prop_data.get("id"),
                    "value": self._extract_property_value(prop_data, prop_type)
                }
        except Exception as e:
            print(f"⚠️  Error extracting properties: {e}")
        
        return properties
    
    def _extract_property_value(self, prop_data: Dict, prop_type: str) -> Any:
        """Extract value from property data based on type."""
        try:
            if prop_type == "title":
                title_data = prop_data.get("title", [])
                return self._extract_rich_text_content(title_data)
            
            elif prop_type == "rich_text":
                rich_text_data = prop_data.get("rich_text", [])
                return self._extract_rich_text_content(rich_text_data)
            
            elif prop_type == "number":
                return prop_data.get("number")
            
            elif prop_type == "select":
                select_data = prop_data.get("select")
                return select_data.get("name") if select_data else None
            
            elif prop_type == "multi_select":
                multi_select_data = prop_data.get("multi_select", [])
                return [item.get("name") for item in multi_select_data]
            
            elif prop_type == "date":
                date_data = prop_data.get("date")
                if date_data:
                    return {
                        "start": date_data.get("start"),
                        "end": date_data.get("end")
                    }
                return None
            
            elif prop_type == "checkbox":
                return prop_data.get("checkbox", False)
            
            elif prop_type == "url":
                return prop_data.get("url")
            
            elif prop_type == "email":
                return prop_data.get("email")
            
            elif prop_type == "phone_number":
                return prop_data.get("phone_number")
            
            elif prop_type == "people":
                people_data = prop_data.get("people", [])
                return [person.get("name", "Unknown") for person in people_data]
            
            elif prop_type == "created_time":
                return prop_data.get("created_time")
            
            elif prop_type == "last_edited_time":
                return prop_data.get("last_edited_time")
            
            else:
                # For other types, return a simplified representation
                return str(prop_data.get(prop_type, ""))
                
        except Exception as e:
            print(f"⚠️  Error extracting {prop_type} property: {e}")
            return None
    
    def _extract_rich_text_content(self, rich_text_data: List[Dict]) -> str:
        """Extract plain text from rich text objects."""
        try:
            return "".join([
                rt.get("text", {}).get("content", "") 
                for rt in rich_text_data
            ])
        except:
            return ""
    
    def _extract_all_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """Extract and process all blocks from a page."""
        processed_blocks = []
        
        for block in blocks:
            try:
                block_data = self._process_block(block)
                processed_blocks.append(block_data)
                
                # If block has children, get them too
                if block.get("has_children"):
                    try:
                        children_response = self.client.blocks.children.list(block_id=block["id"])
                        children = self._extract_all_blocks(children_response.get("results", []))
                        block_data["children"] = children
                    except Exception as e:
                        print(f"⚠️  Error getting children for block {block['id']}: {e}")
                        
            except Exception as e:
                print(f"⚠️  Error processing block: {e}")
                processed_blocks.append({
                    "id": block.get("id", "unknown"),
                    "type": block.get("type", "unknown"),
                    "error": str(e)
                })
        
        return processed_blocks
    
    def _process_block(self, block: Dict) -> Dict:
        """Process a single block and extract its content."""
        block_type = block.get("type")
        block_id = block.get("id")
        
        processed = {
            "id": block_id,
            "type": block_type,
            "has_children": block.get("has_children", False),
            "created_time": block.get("created_time"),
            "last_edited_time": block.get("last_edited_time"),
            "content": "",
            "raw_content": {}
        }
        
        # Extract content based on block type
        if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "quote", "callout"]:
            block_content = block.get(block_type, {})
            rich_text = block_content.get("rich_text", [])
            processed["content"] = self._extract_rich_text_content(rich_text)
            processed["raw_content"] = block_content
            
        elif block_type in ["bulleted_list_item", "numbered_list_item", "to_do"]:
            block_content = block.get(block_type, {})
            rich_text = block_content.get("rich_text", [])
            processed["content"] = self._extract_rich_text_content(rich_text)
            if block_type == "to_do":
                processed["checked"] = block_content.get("checked", False)
            processed["raw_content"] = block_content
            
        elif block_type == "code":
            code_content = block.get("code", {})
            rich_text = code_content.get("rich_text", [])
            processed["content"] = self._extract_rich_text_content(rich_text)
            processed["language"] = code_content.get("language", "")
            processed["raw_content"] = code_content
            
        elif block_type == "child_page":
            child_page = block.get("child_page", {})
            processed["content"] = child_page.get("title", "Untitled Page")
            processed["raw_content"] = child_page
            
        elif block_type == "child_database":
            child_db = block.get("child_database", {})
            processed["content"] = child_db.get("title", "Untitled Database")
            processed["raw_content"] = child_db
            
        elif block_type == "image":
            image_content = block.get("image", {})
            if image_content.get("type") == "external":
                processed["content"] = f"Image: {image_content.get('external', {}).get('url', '')}"
            elif image_content.get("type") == "file":
                processed["content"] = f"Image: {image_content.get('file', {}).get('url', '')}"
            processed["raw_content"] = image_content
            
        elif block_type == "video":
            video_content = block.get("video", {})
            if video_content.get("type") == "external":
                processed["content"] = f"Video: {video_content.get('external', {}).get('url', '')}"
            processed["raw_content"] = video_content
            
        elif block_type == "file":
            file_content = block.get("file", {})
            if file_content.get("type") == "external":
                processed["content"] = f"File: {file_content.get('external', {}).get('url', '')}"
            elif file_content.get("type") == "file":
                processed["content"] = f"File: {file_content.get('file', {}).get('url', '')}"
            processed["raw_content"] = file_content
            
        elif block_type == "bookmark":
            bookmark_content = block.get("bookmark", {})
            processed["content"] = f"Bookmark: {bookmark_content.get('url', '')}"
            processed["raw_content"] = bookmark_content
            
        elif block_type == "embed":
            embed_content = block.get("embed", {})
            processed["content"] = f"Embed: {embed_content.get('url', '')}"
            processed["raw_content"] = embed_content
            
        elif block_type == "table":
            processed["content"] = "Table"
            processed["raw_content"] = block.get("table", {})
            
        elif block_type == "divider":
            processed["content"] = "---"
            processed["raw_content"] = {}
            
        else:
            # For unknown block types, try to extract any rich_text content
            block_content = block.get(block_type, {})
            if isinstance(block_content, dict) and "rich_text" in block_content:
                processed["content"] = self._extract_rich_text_content(block_content["rich_text"])
            else:
                processed["content"] = f"[{block_type}]"
            processed["raw_content"] = block_content
        
        return processed
    
    def _extract_plain_text_from_blocks(self, blocks: List[Dict]) -> str:
        """Extract all plain text content from blocks."""
        text_parts = []
        
        for block in blocks:
            if block.get("content"):
                text_parts.append(block["content"])
            
            # Add children content recursively
            if block.get("children"):
                children_text = self._extract_plain_text_from_blocks(block["children"])
                if children_text:
                    text_parts.append(children_text)
        
        return "\n".join(text_parts)
    
    def extract_page_hierarchy_with_content(self, root_page_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Extract complete page hierarchy with full content."""
        try:
            return self._extract_hierarchy_recursive(root_page_id, max_depth, 0, set())
        except Exception as e:
            print(f"❌ Error extracting hierarchy: {e}")
            return []
    
    def _extract_hierarchy_recursive(self, page_id: str, max_depth: int, current_depth: int, visited: set) -> List[Dict[str, Any]]:
        """Recursively extract page hierarchy with content."""
        if current_depth >= max_depth or page_id in visited:
            return []
        
        visited.add(page_id)
        pages = []
        
        try:
            # Extract current page content
            page_content = self.extract_page_content_full(page_id)
            page_content["depth"] = current_depth
            pages.append(page_content)
            
            # Get child pages
            if not page_content.get("error"):
                clean_page_id = page_id.replace("-", "")
                blocks_response = self.client.blocks.children.list(block_id=clean_page_id)
                
                for block in blocks_response.get("results", []):
                    if block.get("type") == "child_page":
                        child_page_id = block["id"]
                        child_pages = self._extract_hierarchy_recursive(
                            child_page_id, max_depth, current_depth + 1, visited
                        )
                        pages.extend(child_pages)
            
        except Exception as e:
            print(f"❌ Error processing page {page_id}: {e}")
            pages.append({
                "page_id": page_id,
                "error": str(e),
                "depth": current_depth
            })
        
        return pages

# MCP Tool Functions
def extract_page_content(page_id: str) -> Dict[str, Any]:
    """Extract complete content from a single Notion page."""
    try:
        extractor = NotionContentExtractor()
        content = extractor.extract_page_content_full(page_id)
        
        return {
            "status": "success",
            "page_content": content,
            "message": f"Extracted content from page {page_id}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting content: {e}"
        }

def extract_hierarchy_with_content(root_page_id: str, max_depth: int = 5) -> Dict[str, Any]:
    """Extract complete page hierarchy with all content."""
    try:
        extractor = NotionContentExtractor()
        pages = extractor.extract_page_hierarchy_with_content(root_page_id, max_depth)
        
        # Calculate statistics
        total_pages = len(pages)
        total_blocks = sum(page.get("metadata", {}).get("total_blocks", 0) for page in pages if not page.get("error"))
        total_content_length = sum(len(page.get("content_text", "")) for page in pages if not page.get("error"))
        
        return {
            "status": "success",
            "pages": pages,
            "statistics": {
                "total_pages": total_pages,
                "total_blocks": total_blocks,
                "total_content_length": total_content_length,
                "pages_with_errors": len([p for p in pages if p.get("error")])
            },
            "message": f"Extracted content from {total_pages} pages"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting hierarchy: {e}"
        }

def analyze_page_content_semantic(pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze page content for semantic relationships and organization opportunities."""
    try:
        # Basic content analysis without external dependencies
        analysis = {
            "content_analysis": [],
            "potential_categories": {},
            "merge_candidates": [],
            "organization_suggestions": []
        }
        
        for page in pages_data:
            if page.get("error"):
                continue
                
            content_text = page.get("content_text", "")
            title = page.get("title", "")
            
            # Basic content analysis
            word_count = len(content_text.split())
            block_count = page.get("metadata", {}).get("total_blocks", 0)
            
            page_analysis = {
                "page_id": page.get("page_id"),
                "title": title,
                "word_count": word_count,
                "block_count": block_count,
                "content_density": word_count / max(block_count, 1),
                "key_topics": extract_key_topics(content_text, title),
                "content_type": classify_content_type(content_text, title)
            }
            
            analysis["content_analysis"].append(page_analysis)
        
        # Group by content type for potential categories
        content_types = {}
        for page_analysis in analysis["content_analysis"]:
            content_type = page_analysis["content_type"]
            if content_type not in content_types:
                content_types[content_type] = []
            content_types[content_type].append(page_analysis)
        
        analysis["potential_categories"] = content_types
        
        # Find merge candidates (pages with similar titles or very little content)
        merge_candidates = []
        for i, page1 in enumerate(analysis["content_analysis"]):
            for j, page2 in enumerate(analysis["content_analysis"][i+1:], i+1):
                similarity_score = calculate_title_similarity(page1["title"], page2["title"])
                if similarity_score > 0.6 or (page1["word_count"] < 50 and page2["word_count"] < 50):
                    merge_candidates.append({
                        "page1": page1["page_id"],
                        "page2": page2["page_id"],
                        "title1": page1["title"],
                        "title2": page2["title"],
                        "similarity_score": similarity_score,
                        "reason": "Similar titles" if similarity_score > 0.6 else "Low content"
                    })
        
        analysis["merge_candidates"] = merge_candidates
        
        # Generate organization suggestions
        suggestions = []
        if len(content_types) > 1:
            suggestions.append(f"Consider organizing into {len(content_types)} main categories: {', '.join(content_types.keys())}")
        
        if merge_candidates:
            suggestions.append(f"Found {len(merge_candidates)} potential merge opportunities")
        
        low_content_pages = [p for p in analysis["content_analysis"] if p["word_count"] < 50]
        if low_content_pages:
            suggestions.append(f"{len(low_content_pages)} pages have minimal content and could be consolidated")
        
        analysis["organization_suggestions"] = suggestions
        
        return {
            "status": "success",
            "analysis": analysis,
            "message": f"Analyzed {len(analysis['content_analysis'])} pages"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error analyzing content: {e}"
        }

def extract_key_topics(content: str, title: str) -> List[str]:
    """Extract key topics from content and title."""
    # Simple keyword extraction
    text = f"{title} {content}".lower()
    
    # Common topic keywords for LinkedIn/Content
    topic_keywords = {
        "strategy": ["strategy", "strategic", "planning", "plan"],
        "content": ["content", "post", "posts", "writing", "blog"],
        "branding": ["brand", "branding", "identity", "voice"],
        "calendar": ["calendar", "schedule", "timeline", "posting"],
        "performance": ["performance", "analytics", "tracking", "metrics"],
        "automation": ["automation", "workflow", "system", "process"],
        "discovery": ["discovery", "research", "analysis", "insights"],
        "templates": ["template", "framework", "guide", "checklist"]
    }
    
    found_topics = []
    for topic, keywords in topic_keywords.items():
        if any(keyword in text for keyword in keywords):
            found_topics.append(topic)
    
    return found_topics

def classify_content_type(content: str, title: str) -> str:
    """Classify content type based on title and content."""
    text = f"{title} {content}".lower()
    
    if any(word in text for word in ["calendar", "schedule", "timeline", "posting"]):
        return "Planning & Scheduling"
    elif any(word in text for word in ["brand", "discovery", "voice", "identity"]):
        return "Brand Strategy"
    elif any(word in text for word in ["content", "pillar", "ideas", "creation"]):
        return "Content Creation"
    elif any(word in text for word in ["performance", "tracking", "analytics", "metrics"]):
        return "Performance & Analytics"
    elif any(word in text for word in ["automation", "workflow", "system", "agent"]):
        return "Automation & Systems"
    elif any(word in text for word in ["template", "framework", "guide", "checklist"]):
        return "Templates & Frameworks"
    else:
        return "General"

def calculate_title_similarity(title1: str, title2: str) -> float:
    """Calculate similarity between two titles."""
    # Simple word-based similarity
    words1 = set(title1.lower().split())
    words2 = set(title2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)
