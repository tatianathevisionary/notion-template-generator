"""
Update Generation Tool

Provides multi-format update generation capabilities leveraging the existing
update_generator.py module.
"""

import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from update_generator import UpdateGenerator
except ImportError:
    UpdateGenerator = None
    print("Warning: update_generator not found. Update tools will operate in placeholder mode.")


def generate_multi_format_update(
    project_name: str,
    update_data: Dict[str, Any],
    formats: Optional[List[str]] = None,
    output_dir: str = ".",
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate updates in multiple formats (document, slack, linkedin, blog).
    
    Args:
        project_name: Name of the project
        update_data: Structured update data with keys:
            - status: "on_track" | "at_risk" | "off_track"
            - highlight: Main accomplishment
            - next_priority: Top priority for next week
            - progress: List of accomplishments
            - goals: List of next week's goals
            - metrics: List of metric dicts with name, value, change
            - risks: List of risk/blocker dicts
            - decisions: List of decisions made
            - learnings: List of learnings
            - asks: List of asks/needs
        formats: List of formats to generate (default: all)
        output_dir: Directory to save outputs
        date: Date string (default: today)
        
    Returns:
        Dictionary with generated file paths and status
        
    Example:
        >>> generate_multi_format_update(
        ...     project_name="My Project",
        ...     update_data={"status": "on_track", "highlight": "Shipped feature X", ...},
        ...     formats=["slack", "linkedin"]
        ... )
        {
            "status": "success",
            "files": {
                "slack": "path/to/slack.txt",
                "linkedin": "path/to/linkedin.txt"
            }
        }
    """
    if UpdateGenerator is None:
        return {
            "status": "placeholder",
            "message": "UpdateGenerator not available. Would generate updates in formats.",
            "project_name": project_name,
            "formats": formats or ["document", "slack", "linkedin", "blog"],
            "data_preview": {k: str(v)[:100] for k, v in update_data.items()}
        }
    
    try:
        # Initialize generator
        generator = UpdateGenerator(
            project_name=project_name,
            date=date or datetime.now().strftime("%Y-%m-%d")
        )
        
        # Load update data
        generator.load_from_template(update_data)
        
        # Determine which formats to generate
        if formats is None:
            formats = ["document", "slack", "linkedin", "blog"]
        
        generated_files = {}
        
        # Generate each requested format
        if "document" in formats:
            doc_file = f"{output_dir}/{project_name.lower().replace(' ', '_')}_update.md"
            generator.generate_document(doc_file)
            generated_files["document"] = doc_file
        
        if "slack" in formats:
            slack_text = generator.generate_slack_update()
            slack_file = f"{output_dir}/{project_name.lower().replace(' ', '_')}_slack.txt"
            with open(slack_file, 'w', encoding='utf-8') as f:
                f.write(slack_text)
            generated_files["slack"] = slack_file
        
        if "linkedin" in formats:
            linkedin_text = generator.generate_linkedin_post()
            linkedin_file = f"{output_dir}/{project_name.lower().replace(' ', '_')}_linkedin.txt"
            with open(linkedin_file, 'w', encoding='utf-8') as f:
                f.write(linkedin_text)
            generated_files["linkedin"] = linkedin_file
        
        if "blog" in formats:
            blog_text = generator.generate_blog_post()
            blog_file = f"{output_dir}/{project_name.lower().replace(' ', '_')}_blog.md"
            with open(blog_file, 'w', encoding='utf-8') as f:
                f.write(blog_text)
            generated_files["blog"] = blog_file
        
        return {
            "status": "success",
            "project_name": project_name,
            "formats_generated": list(generated_files.keys()),
            "files": generated_files
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "project_name": project_name,
            "formats": formats
        }


def create_update_template() -> Dict[str, Any]:
    """
    Return a template structure for update data.
    
    Returns:
        Dictionary with template structure and examples
    """
    return {
        "template": {
            "project_name": "Your Project Name",
            "date": "2025-10-05",
            "status": "on_track",  # or "at_risk" | "off_track"
            "highlight": "The single most important accomplishment from this week",
            "next_priority": "The #1 priority for the upcoming week",
            "progress": [
                "Accomplishment 1 - Be specific and link to goals",
                "Accomplishment 2 - Include impact/metrics",
                "Accomplishment 3 - Use action verbs"
            ],
            "goals": [
                "Priority 1 for next week",
                "Priority 2 for next week",
                "Priority 3 for next week"
            ],
            "metrics": [
                {
                    "name": "Metric Name",
                    "value": "100",
                    "change": "+10% WoW"
                }
            ],
            "risks": [
                {
                    "type": "risk",  # or "blocker"
                    "description": "Description of the risk or blocker"
                }
            ],
            "decisions": [
                "Key decision 1 - Why we chose this approach"
            ],
            "learnings": [
                "Important insight 1 - What we discovered"
            ],
            "asks": [
                "Specific help needed from leadership/team"
            ]
        },
        "tips": {
            "progress": "Focus on outcomes, not activities. 'Shipped feature X' not 'Worked on feature X'",
            "goals": "Keep to 3-5 items. Prioritize ruthlessly",
            "metrics": "Include week-over-week change to show momentum",
            "risks": "Be transparent. Surface problems early",
            "decisions": "Document the 'why' for future reference",
            "learnings": "These become your knowledge base",
            "asks": "Make requests actionable"
        }
    }


def validate_update_data(update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate update data structure.
    
    Args:
        update_data: The update data to validate
        
    Returns:
        Dictionary with validation results
    """
    required_fields = [
        "status", "highlight", "next_priority",
        "progress", "goals"
    ]
    
    missing_fields = [
        field for field in required_fields
        if field not in update_data or not update_data[field]
    ]
    
    warnings = []
    
    # Check status value
    if update_data.get("status") not in ["on_track", "at_risk", "off_track"]:
        warnings.append("Status should be one of: on_track, at_risk, off_track")
    
    # Check list lengths
    if len(update_data.get("progress", [])) < 2:
        warnings.append("Recommended: At least 2 progress items")
    
    if len(update_data.get("goals", [])) < 2:
        warnings.append("Recommended: At least 2 goals for next week")
    
    return {
        "valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "warnings": warnings,
        "status": "valid" if len(missing_fields) == 0 else "invalid"
    }

