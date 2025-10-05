#!/usr/bin/env python3
"""
Comprehensive Page Management Tool for Notion Template Generator MCP
Handles all Notion page properties and provides intelligent reorganization capabilities
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "02_Core_System"))

try:
    from notion_client import Client
    from dotenv import load_dotenv
    from notion_api_client import NotionTemplateClient, AdvancedNotionClient
    
    # Load environment variables
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

# Import intelligent reorganization components
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from intelligent_page_reorganizer import (
        PageContent, ContentAnalysis, PageRelationship,
        NotionContentExtractor, SemanticAnalyzer
    )
    INTELLIGENT_ANALYSIS_AVAILABLE = True
except ImportError:
    print("⚠️  Intelligent analysis components not available")
    INTELLIGENT_ANALYSIS_AVAILABLE = False

@dataclass
class PagePropertyValue:
    """Represents a comprehensive page property value with all Notion types."""
    property_id: str
    property_name: str
    property_type: str
    value: Any
    metadata: Dict[str, Any] = None

@dataclass 
class PageHierarchy:
    """Represents a page hierarchy structure."""
    page_id: str
    title: str
    url: str
    parent_id: Optional[str]
    children: List['PageHierarchy']
    properties: Dict[str, PagePropertyValue]
    created_time: str
    last_edited_time: str
    depth: int = 0

class ComprehensivePageManager:
    """Comprehensive page manager with all Notion property types and intelligent analysis."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("Notion API key not found")
        
        self.client = Client(auth=self.api_key, notion_version="2025-09-03")
        self.template_client = NotionTemplateClient(self.api_key)
        self.advanced_client = AdvancedNotionClient(self.api_key)
        
        # Initialize intelligent analysis if available
        self.content_extractor = None
        self.semantic_analyzer = None
        if INTELLIGENT_ANALYSIS_AVAILABLE:
            try:
                self.content_extractor = NotionContentExtractor(self.api_key)
                self.semantic_analyzer = SemanticAnalyzer()
            except Exception as e:
                print(f"⚠️  Could not initialize intelligent analysis: {e}")
    
    def extract_all_page_properties(self, page_id: str) -> Dict[str, PagePropertyValue]:
        """Extract all page properties with comprehensive type handling."""
        try:
            clean_page_id = page_id.replace("-", "")
            page = self.client.pages.retrieve(page_id=clean_page_id)
            properties = {}
            
            for prop_name, prop_data in page.get("properties", {}).items():
                prop_id = prop_data.get("id")
                prop_type = prop_data.get("type")
                
                # Extract value based on property type
                value = self._extract_property_value(prop_data, prop_type)
                
                properties[prop_name] = PagePropertyValue(
                    property_id=prop_id,
                    property_name=prop_name,
                    property_type=prop_type,
                    value=value,
                    metadata={
                        "raw_data": prop_data,
                        "extracted_at": datetime.now().isoformat()
                    }
                )
            
            return properties
            
        except Exception as e:
            print(f"❌ Error extracting properties from page {page_id}: {e}")
            return {}
    
    def _extract_property_value(self, prop_data: Dict, prop_type: str) -> Any:
        """Extract value from property data based on type."""
        try:
            if prop_type == "title":
                title_data = prop_data.get("title", [])
                return self._extract_rich_text(title_data)
            
            elif prop_type == "rich_text":
                rich_text_data = prop_data.get("rich_text", [])
                return self._extract_rich_text(rich_text_data)
            
            elif prop_type == "number":
                return prop_data.get("number")
            
            elif prop_type == "select":
                select_data = prop_data.get("select")
                if select_data:
                    return {
                        "id": select_data.get("id"),
                        "name": select_data.get("name"),
                        "color": select_data.get("color")
                    }
                return None
            
            elif prop_type == "multi_select":
                multi_select_data = prop_data.get("multi_select", [])
                return [
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "color": item.get("color")
                    }
                    for item in multi_select_data
                ]
            
            elif prop_type == "date":
                date_data = prop_data.get("date")
                if date_data:
                    return {
                        "start": date_data.get("start"),
                        "end": date_data.get("end"),
                        "time_zone": date_data.get("time_zone")
                    }
                return None
            
            elif prop_type == "people":
                people_data = prop_data.get("people", [])
                return [
                    {
                        "id": person.get("id"),
                        "name": person.get("name"),
                        "avatar_url": person.get("avatar_url"),
                        "type": person.get("type"),
                        "email": person.get("person", {}).get("email") if person.get("type") == "person" else None
                    }
                    for person in people_data
                ]
            
            elif prop_type == "files":
                files_data = prop_data.get("files", [])
                return [
                    {
                        "name": file_item.get("name"),
                        "type": file_item.get("type"),
                        "url": file_item.get("external", {}).get("url") if file_item.get("type") == "external" else file_item.get("file", {}).get("url")
                    }
                    for file_item in files_data
                ]
            
            elif prop_type == "checkbox":
                return prop_data.get("checkbox", False)
            
            elif prop_type == "url":
                return prop_data.get("url")
            
            elif prop_type == "email":
                return prop_data.get("email")
            
            elif prop_type == "phone_number":
                return prop_data.get("phone_number")
            
            elif prop_type == "formula":
                formula_data = prop_data.get("formula", {})
                formula_type = formula_data.get("type")
                return {
                    "type": formula_type,
                    "value": formula_data.get(formula_type)
                }
            
            elif prop_type == "relation":
                relation_data = prop_data.get("relation", [])
                return [{"id": rel.get("id")} for rel in relation_data]
            
            elif prop_type == "rollup":
                rollup_data = prop_data.get("rollup", {})
                rollup_type = rollup_data.get("type")
                return {
                    "type": rollup_type,
                    "function": rollup_data.get("function"),
                    "value": rollup_data.get(rollup_type)
                }
            
            elif prop_type == "created_time":
                return prop_data.get("created_time")
            
            elif prop_type == "created_by":
                created_by = prop_data.get("created_by", {})
                return {
                    "id": created_by.get("id"),
                    "name": created_by.get("name"),
                    "type": created_by.get("type")
                }
            
            elif prop_type == "last_edited_time":
                return prop_data.get("last_edited_time")
            
            elif prop_type == "last_edited_by":
                edited_by = prop_data.get("last_edited_by", {})
                return {
                    "id": edited_by.get("id"),
                    "name": edited_by.get("name"),
                    "type": edited_by.get("type")
                }
            
            elif prop_type == "status":
                status_data = prop_data.get("status")
                if status_data:
                    return {
                        "id": status_data.get("id"),
                        "name": status_data.get("name"),
                        "color": status_data.get("color")
                    }
                return None
            
            elif prop_type == "unique_id":
                unique_id_data = prop_data.get("unique_id", {})
                return {
                    "number": unique_id_data.get("number"),
                    "prefix": unique_id_data.get("prefix")
                }
            
            elif prop_type == "verification":
                verification_data = prop_data.get("verification", {})
                return {
                    "state": verification_data.get("state"),
                    "verified_by": verification_data.get("verified_by"),
                    "date": verification_data.get("date")
                }
            
            else:
                # Return raw data for unknown types
                return prop_data.get(prop_type)
                
        except Exception as e:
            print(f"⚠️  Error extracting {prop_type} property: {e}")
            return None
    
    def _extract_rich_text(self, rich_text_data: List[Dict]) -> str:
        """Extract plain text from rich text objects."""
        try:
            return "".join([
                rt.get("text", {}).get("content", "") 
                for rt in rich_text_data
            ])
        except:
            return ""
    
    def get_page_hierarchy(self, root_page_id: str, max_depth: int = 10) -> PageHierarchy:
        """Get comprehensive page hierarchy with all properties."""
        try:
            return self._build_hierarchy_recursive(root_page_id, max_depth, 0)
        except Exception as e:
            print(f"❌ Error building hierarchy: {e}")
            return None
    
    def _build_hierarchy_recursive(self, page_id: str, max_depth: int, current_depth: int) -> PageHierarchy:
        """Recursively build page hierarchy."""
        if current_depth >= max_depth:
            return None
        
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get page details
            page = self.client.pages.retrieve(page_id=clean_page_id)
            
            # Extract basic info
            title = self._extract_title(page)
            url = page.get("url", "")
            created_time = page.get("created_time", "")
            last_edited_time = page.get("last_edited_time", "")
            parent_id = self._extract_parent_id(page)
            
            # Extract all properties
            properties = self.extract_all_page_properties(page_id)
            
            # Get children
            children = []
            try:
                blocks_response = self.client.blocks.children.list(block_id=clean_page_id)
                for block in blocks_response.get("results", []):
                    if block.get("type") == "child_page":
                        child_page_id = block["id"]
                        child_hierarchy = self._build_hierarchy_recursive(
                            child_page_id, max_depth, current_depth + 1
                        )
                        if child_hierarchy:
                            children.append(child_hierarchy)
            except Exception as e:
                print(f"⚠️  Error getting children for {page_id}: {e}")
            
            return PageHierarchy(
                page_id=page_id,
                title=title,
                url=url,
                parent_id=parent_id,
                children=children,
                properties=properties,
                created_time=created_time,
                last_edited_time=last_edited_time,
                depth=current_depth
            )
            
        except Exception as e:
            print(f"❌ Error processing page {page_id}: {e}")
            return None
    
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
    
    def _extract_parent_id(self, page: Dict) -> Optional[str]:
        """Extract parent ID from page."""
        try:
            parent = page.get("parent", {})
            if parent.get("type") == "page_id":
                return parent.get("page_id")
            elif parent.get("type") == "database_id":
                return parent.get("database_id")
            return None
        except:
            return None
    
    def update_page_property(self, page_id: str, property_name: str, property_type: str, value: Any) -> bool:
        """Update a page property with proper type handling."""
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Build property update based on type
            property_update = self._build_property_update(property_type, value)
            
            if property_update is None:
                print(f"❌ Unsupported property type: {property_type}")
                return False
            
            # Update the page
            self.client.pages.update(
                page_id=clean_page_id,
                properties={
                    property_name: property_update
                }
            )
            
            print(f"✅ Updated {property_type} property '{property_name}' on page")
            return True
            
        except Exception as e:
            print(f"❌ Error updating property: {e}")
            return False
    
    def _build_property_update(self, property_type: str, value: Any) -> Optional[Dict]:
        """Build property update object based on type."""
        try:
            if property_type == "title":
                if isinstance(value, str):
                    return {"title": [{"text": {"content": value}}]}
                return {"title": value}
            
            elif property_type == "rich_text":
                if isinstance(value, str):
                    return {"rich_text": [{"text": {"content": value}}]}
                return {"rich_text": value}
            
            elif property_type == "number":
                return {"number": value}
            
            elif property_type == "select":
                if isinstance(value, str):
                    return {"select": {"name": value}}
                return {"select": value}
            
            elif property_type == "multi_select":
                if isinstance(value, list) and all(isinstance(item, str) for item in value):
                    return {"multi_select": [{"name": item} for item in value]}
                return {"multi_select": value}
            
            elif property_type == "date":
                return {"date": value}
            
            elif property_type == "people":
                return {"people": value}
            
            elif property_type == "files":
                return {"files": value}
            
            elif property_type == "checkbox":
                return {"checkbox": bool(value)}
            
            elif property_type == "url":
                return {"url": value}
            
            elif property_type == "email":
                return {"email": value}
            
            elif property_type == "phone_number":
                return {"phone_number": value}
            
            elif property_type == "relation":
                return {"relation": value}
            
            elif property_type == "status":
                if isinstance(value, str):
                    return {"status": {"name": value}}
                return {"status": value}
            
            else:
                print(f"⚠️  Property type '{property_type}' is read-only or not supported for updates")
                return None
                
        except Exception as e:
            print(f"❌ Error building property update: {e}")
            return None
    
    def create_page_with_properties(self, parent_id: str, title: str, properties: Dict[str, Any] = None) -> Optional[str]:
        """Create a new page with comprehensive properties."""
        try:
            clean_parent_id = parent_id.replace("-", "")
            
            # Build properties
            page_properties = {"title": [{"text": {"content": title}}]}
            
            if properties:
                for prop_name, prop_data in properties.items():
                    prop_type = prop_data.get("type")
                    prop_value = prop_data.get("value")
                    
                    prop_update = self._build_property_update(prop_type, prop_value)
                    if prop_update:
                        page_properties[prop_name] = prop_update
            
            # Create the page
            response = self.client.pages.create(
                parent={"type": "page_id", "page_id": clean_parent_id},
                properties=page_properties
            )
            
            print(f"✅ Created page '{title}' with {len(page_properties)} properties")
            return response["id"]
            
        except Exception as e:
            print(f"❌ Error creating page: {e}")
            return None
    
    def move_page(self, page_id: str, new_parent_id: str, new_parent_type: str = "page_id") -> bool:
        """Move a page to a new parent."""
        try:
            clean_page_id = page_id.replace("-", "")
            clean_parent_id = new_parent_id.replace("-", "")
            
            self.client.pages.update(
                page_id=clean_page_id,
                parent={"type": new_parent_type, new_parent_type: clean_parent_id}
            )
            
            print(f"✅ Moved page to new parent")
            return True
            
        except Exception as e:
            print(f"❌ Error moving page: {e}")
            return False
    
    async def analyze_page_structure_intelligent(self, root_page_id: str) -> Optional[Dict]:
        """Perform intelligent page structure analysis."""
        if not INTELLIGENT_ANALYSIS_AVAILABLE or not self.content_extractor:
            print("⚠️  Intelligent analysis not available")
            return None
        
        try:
            print("🧠 Starting intelligent page structure analysis...")
            
            # Extract page content
            pages = self.content_extractor.extract_page_hierarchy(root_page_id, max_depth=5)
            
            if not pages:
                print("❌ No pages found for analysis")
                return None
            
            # Generate semantic embeddings
            if self.semantic_analyzer:
                self.semantic_analyzer.generate_embeddings(pages)
                relationships = self.semantic_analyzer.find_similar_pages(pages, threshold=0.4)
                clusters = self.semantic_analyzer.cluster_pages(pages)
                
                return {
                    "pages": [asdict(page) for page in pages],
                    "relationships": [asdict(rel) for rel in relationships],
                    "clusters": {str(k): [asdict(p) for p in v] for k, v in clusters.items()},
                    "analysis_timestamp": datetime.now().isoformat()
                }
            
            return {"pages": [asdict(page) for page in pages]}
            
        except Exception as e:
            print(f"❌ Error in intelligent analysis: {e}")
            return None

# Tool functions for MCP integration
def create_notion_page_comprehensive(parent_id: str, title: str, properties: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a Notion page with comprehensive properties support."""
    try:
        manager = ComprehensivePageManager()
        page_id = manager.create_page_with_properties(parent_id, title, properties)
        
        if page_id:
            return {
                "status": "success",
                "page_id": page_id,
                "message": f"Created page '{title}' successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to create page"
            }
            
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error creating page: {e}"
        }

def get_page_hierarchy_comprehensive(root_page_id: str, max_depth: int = 10) -> Dict[str, Any]:
    """Get comprehensive page hierarchy with all properties."""
    try:
        manager = ComprehensivePageManager()
        hierarchy = manager.get_page_hierarchy(root_page_id, max_depth)
        
        if hierarchy:
            return {
                "status": "success",
                "hierarchy": asdict(hierarchy),
                "message": f"Retrieved hierarchy for page {root_page_id}"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve hierarchy"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving hierarchy: {e}"
        }

def extract_page_properties_comprehensive(page_id: str) -> Dict[str, Any]:
    """Extract all page properties with comprehensive type support."""
    try:
        manager = ComprehensivePageManager()
        properties = manager.extract_all_page_properties(page_id)
        
        # Convert PagePropertyValue objects to dicts
        properties_dict = {
            name: asdict(prop) for name, prop in properties.items()
        }
        
        return {
            "status": "success",
            "properties": properties_dict,
            "property_count": len(properties),
            "message": f"Extracted {len(properties)} properties from page"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting properties: {e}"
        }

def update_page_property_comprehensive(page_id: str, property_name: str, property_type: str, value: Any) -> Dict[str, Any]:
    """Update a page property with comprehensive type support."""
    try:
        manager = ComprehensivePageManager()
        success = manager.update_page_property(page_id, property_name, property_type, value)
        
        if success:
            return {
                "status": "success",
                "message": f"Updated {property_type} property '{property_name}'"
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to update property '{property_name}'"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error updating property: {e}"
        }

def move_page_comprehensive(page_id: str, new_parent_id: str, new_parent_type: str = "page_id") -> Dict[str, Any]:
    """Move a page to a new parent."""
    try:
        manager = ComprehensivePageManager()
        success = manager.move_page(page_id, new_parent_id, new_parent_type)
        
        if success:
            return {
                "status": "success", 
                "message": "Page moved successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to move page"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error moving page: {e}"
        }

async def analyze_page_structure_intelligent_tool(root_page_id: str) -> Dict[str, Any]:
    """Perform intelligent page structure analysis."""
    try:
        manager = ComprehensivePageManager()
        analysis = await manager.analyze_page_structure_intelligent(root_page_id)
        
        if analysis:
            return {
                "status": "success",
                "analysis": analysis,
                "message": "Intelligent analysis completed"
            }
        else:
            return {
                "status": "error",
                "message": "Intelligent analysis failed or not available"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error in intelligent analysis: {e}"
        }
