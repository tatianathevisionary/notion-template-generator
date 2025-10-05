#!/usr/bin/env python3
"""
Wiki Management Tool for Notion Template Generator MCP

This tool implements wiki principles including:
- Converting pages to wikis with default views (Home, All pages, Pages I own)
- Page verification with ownership and expiration management
- Wiki organization and knowledge management features
"""

import os
import sys
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from notion_client import Client
from notion_client.errors import APIResponseError
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class WikiManager:
    """Enhanced wiki management with verification and ownership features."""
    
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_API_KEY"))
        if not os.getenv("NOTION_API_KEY"):
            raise ValueError("NOTION_API_KEY environment variable is required")
    
    def create_wiki(self, page_id: str, wiki_title: str = None, description: str = None) -> Dict[str, Any]:
        """
        Convert a page into a wiki with default views and structure.
        
        Args:
            page_id: ID of the page to convert to wiki
            wiki_title: Optional custom title for the wiki
            description: Optional description for the wiki home page
        
        Returns:
            Dict with wiki creation results
        """
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get the original page info
            page_info = self.client.pages.retrieve(page_id=clean_page_id)
            original_title = self._extract_page_title(page_info)
            
            wiki_name = wiki_title or f"{original_title} Wiki"
            
            print(f"🏛️ Converting '{original_title}' to wiki: '{wiki_name}'")
            
            # Step 1: Update the main page to serve as wiki home
            home_blocks = []
            
            # Add wiki description
            if description:
                home_blocks.append({
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": description}}],
                        "icon": {"type": "emoji", "emoji": "📚"},
                        "color": "blue_background"
                    }
                })
            
            # Add wiki navigation
            home_blocks.extend([
                {
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📚 Wiki Navigation"}}],
                        "color": "default"
                    }
                },
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "Use the views below to navigate this wiki:"}}]
                    }
                }
            ])
            
            # Step 2: Create "All Pages" database
            all_pages_db = self._create_wiki_database(
                parent_id=clean_page_id,
                title="📄 All Pages",
                description="Complete database view of all wiki pages",
                include_verification=True
            )
            
            if all_pages_db:
                home_blocks.append({
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"📄 All Pages Database: {all_pages_db}"}}]
                    }
                })
            
            # Step 3: Create "Pages I Own" database view
            pages_i_own_db = self._create_wiki_database(
                parent_id=clean_page_id,
                title="👤 Pages I Own",
                description="Pages you own in this wiki",
                include_verification=True,
                owner_filter=True
            )
            
            if pages_i_own_db:
                home_blocks.append({
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"👤 Pages I Own Database: {pages_i_own_db}"}}]
                    }
                })
            
            # Step 4: Add wiki content organization section
            home_blocks.extend([
                {
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📋 Wiki Content Organization"}}],
                        "color": "default"
                    }
                },
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "Organize your wiki pages below by dragging and dropping them under relevant headings:"}}]
                    }
                },
                {
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "🎯 Getting Started"}}],
                        "color": "default"
                    }
                },
                {
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "📚 Knowledge Base"}}],
                        "color": "default"
                    }
                },
                {
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "🔧 Tools & Resources"}}],
                        "color": "default"
                    }
                }
            ])
            
            # Update the main page with wiki structure
            if home_blocks:
                self.client.blocks.children.append(
                    block_id=clean_page_id,
                    children=home_blocks[:50]  # Limit to avoid API limits
                )
            
            # Update page title and icon to reflect wiki status
            self.client.pages.update(
                page_id=clean_page_id,
                properties={
                    "title": [{"type": "text", "text": {"content": wiki_name}}]
                },
                icon={"type": "emoji", "emoji": "🏛️"}
            )
            
            print(f"✅ Successfully created wiki: '{wiki_name}'")
            print(f"   📄 All Pages database: {'✅' if all_pages_db else '❌'}")
            print(f"   👤 Pages I Own database: {'✅' if pages_i_own_db else '❌'}")
            
            return {
                "status": "success",
                "wiki_id": clean_page_id,
                "wiki_name": wiki_name,
                "all_pages_db_id": all_pages_db,
                "pages_i_own_db_id": pages_i_own_db,
                "message": f"Successfully converted to wiki: {wiki_name}"
            }
            
        except APIResponseError as e:
            error_msg = f"API Error creating wiki: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Error creating wiki: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
    
    def _create_wiki_database(self, parent_id: str, title: str, description: str, 
                             include_verification: bool = True, owner_filter: bool = False) -> Optional[str]:
        """Create a database for wiki page management."""
        try:
            # Define database properties
            properties = {
                "Title": {"title": {}},
                "Created": {"created_time": {}},
                "Last Edited": {"last_edited_time": {}},
                "Tags": {"multi_select": {"options": [
                    {"name": "Knowledge Base", "color": "blue"},
                    {"name": "Getting Started", "color": "green"},
                    {"name": "Tools", "color": "orange"},
                    {"name": "Reference", "color": "purple"},
                    {"name": "Archive", "color": "gray"}
                ]}}
            }
            
            # Add verification and owner properties if requested
            if include_verification:
                properties["Verified"] = {"checkbox": {}}
                properties["Owner"] = {"people": {}}
                properties["Verification Expires"] = {"date": {}}
            
            # Create the database
            db_response = self.client.databases.create(
                parent={"type": "page_id", "page_id": parent_id},
                title=[{"type": "text", "text": {"content": title}}],
                description=[{"type": "text", "text": {"content": description}}],
                properties=properties,
                icon={"type": "emoji", "emoji": "🗄️"}
            )
            
            return db_response["id"]
            
        except Exception as e:
            print(f"⚠️  Error creating wiki database '{title}': {e}")
            return None
    
    def verify_page(self, page_id: str, owner_ids: List[str] = None, 
                   expires_in_days: Optional[int] = None, indefinite: bool = False) -> Dict[str, Any]:
        """
        Verify a page with ownership and expiration settings.
        
        Args:
            page_id: ID of the page to verify
            owner_ids: List of user IDs to set as page owners
            expires_in_days: Number of days until verification expires (None for indefinite)
            indefinite: Set to True for indefinite verification
        
        Returns:
            Dict with verification results
        """
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get page info
            page_info = self.client.pages.retrieve(page_id=clean_page_id)
            page_title = self._extract_page_title(page_info)
            
            print(f"✅ Verifying page: '{page_title}'")
            
            # Prepare verification properties
            verification_props = {
                "Verified": {"checkbox": True}
            }
            
            # Set owners if provided
            if owner_ids:
                verification_props["Owner"] = {
                    "people": [{"id": user_id} for user_id in owner_ids]
                }
            
            # Set expiration date if specified
            if not indefinite and expires_in_days:
                expiry_date = datetime.now() + timedelta(days=expires_in_days)
                verification_props["Verification Expires"] = {
                    "date": {"start": expiry_date.isoformat().split('T')[0]}
                }
            elif indefinite:
                verification_props["Verification Expires"] = {"date": None}
            
            # Update page with verification
            self.client.pages.update(
                page_id=clean_page_id,
                properties=verification_props
            )
            
            # Add verification badge to page icon if not already present
            current_icon = page_info.get("icon")
            if not current_icon or current_icon.get("emoji") != "✅":
                self.client.pages.update(
                    page_id=clean_page_id,
                    icon={"type": "emoji", "emoji": "✅"}
                )
            
            verification_status = "indefinite" if indefinite else f"{expires_in_days} days" if expires_in_days else "no expiration set"
            
            print(f"✅ Page verified successfully")
            print(f"   👤 Owners: {len(owner_ids) if owner_ids else 0}")
            print(f"   ⏰ Expires: {verification_status}")
            
            return {
                "status": "success",
                "page_id": clean_page_id,
                "page_title": page_title,
                "owners_count": len(owner_ids) if owner_ids else 0,
                "expiration": verification_status,
                "message": f"Successfully verified page: {page_title}"
            }
            
        except APIResponseError as e:
            error_msg = f"API Error verifying page: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Error verifying page: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
    
    def remove_verification(self, page_id: str) -> Dict[str, Any]:
        """Remove verification from a page."""
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get page info
            page_info = self.client.pages.retrieve(page_id=clean_page_id)
            page_title = self._extract_page_title(page_info)
            
            print(f"🔓 Removing verification from: '{page_title}'")
            
            # Remove verification properties
            verification_props = {
                "Verified": {"checkbox": False},
                "Verification Expires": {"date": None}
            }
            
            # Update page
            self.client.pages.update(
                page_id=clean_page_id,
                properties=verification_props
            )
            
            print(f"✅ Verification removed from '{page_title}'")
            
            return {
                "status": "success",
                "page_id": clean_page_id,
                "page_title": page_title,
                "message": f"Successfully removed verification from: {page_title}"
            }
            
        except APIResponseError as e:
            error_msg = f"API Error removing verification: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Error removing verification: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
    
    def get_verified_pages(self, workspace_id: str = None) -> Dict[str, Any]:
        """Get all verified pages in the workspace."""
        try:
            print("📋 Retrieving all verified pages...")
            
            # This would typically query a database or search for verified pages
            # For now, we'll return a placeholder structure
            verified_pages = []
            
            print(f"✅ Found {len(verified_pages)} verified pages")
            
            return {
                "status": "success",
                "verified_pages": verified_pages,
                "count": len(verified_pages),
                "message": f"Retrieved {len(verified_pages)} verified pages"
            }
            
        except Exception as e:
            error_msg = f"Error retrieving verified pages: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
    
    def undo_wiki(self, page_id: str) -> Dict[str, Any]:
        """Convert a wiki back to a regular page."""
        try:
            clean_page_id = page_id.replace("-", "")
            
            # Get page info
            page_info = self.client.pages.retrieve(page_id=clean_page_id)
            page_title = self._extract_page_title(page_info)
            
            print(f"🔄 Converting wiki back to regular page: '{page_title}'")
            
            # Remove wiki icon and update title
            original_title = page_title.replace(" Wiki", "").replace("🏛️ ", "")
            
            self.client.pages.update(
                page_id=clean_page_id,
                properties={
                    "title": [{"type": "text", "text": {"content": original_title}}]
                },
                icon={"type": "emoji", "emoji": "📄"}
            )
            
            print(f"✅ Wiki converted back to regular page: '{original_title}'")
            
            return {
                "status": "success",
                "page_id": clean_page_id,
                "original_title": original_title,
                "message": f"Successfully converted wiki back to page: {original_title}"
            }
            
        except APIResponseError as e:
            error_msg = f"API Error undoing wiki: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Error undoing wiki: {e}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}
    
    def _extract_page_title(self, page_info: Dict[str, Any]) -> str:
        """Extract title from page info."""
        try:
            properties = page_info.get("properties", {})
            
            # Look for title property
            for prop_name, prop_data in properties.items():
                if prop_data.get("type") == "title":
                    title_array = prop_data.get("title", [])
                    if title_array:
                        return "".join([item.get("text", {}).get("content", "") for item in title_array])
            
            # Fallback to child_page title if available
            if page_info.get("object") == "page":
                return "Untitled Page"
            
            return "Untitled"
            
        except Exception as e:
            print(f"⚠️  Error extracting page title: {e}")
            return "Untitled"


# MCP Tool Functions
def create_notion_wiki(page_id: str, wiki_title: str = None, description: str = None) -> Dict[str, Any]:
    """
    Convert a Notion page into a wiki with default views and structure.
    
    Args:
        page_id: ID of the page to convert to wiki
        wiki_title: Optional custom title for the wiki
        description: Optional description for the wiki home page
    
    Returns:
        Dict with wiki creation results
    """
    try:
        manager = WikiManager()
        return manager.create_wiki(page_id, wiki_title, description)
    except Exception as e:
        return {"status": "error", "message": f"Failed to create wiki: {e}"}


def verify_notion_page(page_id: str, owner_ids: List[str] = None, 
                      expires_in_days: Optional[int] = None, indefinite: bool = False) -> Dict[str, Any]:
    """
    Verify a Notion page with ownership and expiration settings.
    
    Args:
        page_id: ID of the page to verify
        owner_ids: List of user IDs to set as page owners
        expires_in_days: Number of days until verification expires
        indefinite: Set to True for indefinite verification
    
    Returns:
        Dict with verification results
    """
    try:
        manager = WikiManager()
        return manager.verify_page(page_id, owner_ids, expires_in_days, indefinite)
    except Exception as e:
        return {"status": "error", "message": f"Failed to verify page: {e}"}


def remove_notion_page_verification(page_id: str) -> Dict[str, Any]:
    """
    Remove verification from a Notion page.
    
    Args:
        page_id: ID of the page to remove verification from
    
    Returns:
        Dict with removal results
    """
    try:
        manager = WikiManager()
        return manager.remove_verification(page_id)
    except Exception as e:
        return {"status": "error", "message": f"Failed to remove verification: {e}"}


def undo_notion_wiki(page_id: str) -> Dict[str, Any]:
    """
    Convert a wiki back to a regular Notion page.
    
    Args:
        page_id: ID of the wiki to convert back
    
    Returns:
        Dict with conversion results
    """
    try:
        manager = WikiManager()
        return manager.undo_wiki(page_id)
    except Exception as e:
        return {"status": "error", "message": f"Failed to undo wiki: {e}"}


def get_all_verified_pages(workspace_id: str = None) -> Dict[str, Any]:
    """
    Get all verified pages in the workspace.
    
    Args:
        workspace_id: Optional workspace ID to filter by
    
    Returns:
        Dict with verified pages list
    """
    try:
        manager = WikiManager()
        return manager.get_verified_pages(workspace_id)
    except Exception as e:
        return {"status": "error", "message": f"Failed to get verified pages: {e}"}
