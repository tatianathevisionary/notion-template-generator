#!/usr/bin/env python3
"""
Professional Notion Template System - Folder Structure Cleanup
Optimized for template sales and user experience
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any

def analyze_current_structure():
    """Analyze current folder structure and identify issues."""
    
    print("🔍 ANALYZING CURRENT FOLDER STRUCTURE")
    print("=" * 50)
    
    issues = []
    duplicates = []
    
    # Check for duplicate documentation files
    doc_files = [
        "COMPLETE_SYSTEM_SUMMARY.md",
        "COMPLETION_SUMMARY.md", 
        "PROJECT_STRUCTURE.md",
        "REORGANIZATION_SUMMARY.md",
        "NOTION_API_COMPLETE_IMPLEMENTATION.md",
        "LINKEDIN_OS_SETUP_COMPLETE.md",
        "USER_TESTING_READY.md",
        "TEST_RESULTS_SUMMARY.md",
        "GAP_ANALYSIS.md",
        "ADVANCED_FEATURES_COMPLETE.md",
        "MCP_CAPABILITIES_GUIDE.md",
        "DATABASE_CREATION_SUCCESS.md"
    ]
    
    print(f"📄 Found {len(doc_files)} documentation files (potential duplicates)")
    
    # Check for scattered scripts
    script_files = [
        "add_prompt_templates.py",
        "configure_existing_databases.py", 
        "create_linkedin_os.py",
        "populate_content.py",
        "populate_prompt_details.py",
        "test_all_tools.py",
        "test_interactive.py"
    ]
    
    print(f"🐍 Found {len(script_files)} scattered Python scripts")
    
    # Check for multiple setup files
    setup_files = [
        "setup_env.sh",
        "setup.sh", 
        "verify_mcp_setup.sh"
    ]
    
    print(f"⚙️ Found {len(setup_files)} setup files")
    
    # Check for multiple requirements files
    req_files = [
        "requirements.txt",
        "requirements_mcp.txt"
    ]
    
    print(f"📦 Found {len(req_files)} requirements files")
    
    return {
        "doc_files": doc_files,
        "script_files": script_files, 
        "setup_files": setup_files,
        "req_files": req_files
    }

def create_professional_structure():
    """Create a professional folder structure optimized for template sales."""
    
    print("\n🏗️ CREATING PROFESSIONAL FOLDER STRUCTURE")
    print("=" * 50)
    
    # Define the new professional structure
    structure = {
        "📁 LinkedIn Content OS Template": {
            "📁 01_Setup": [
                "README.md (main setup guide)",
                "QUICKSTART.md", 
                "requirements.txt",
                "setup.py"
            ],
            "📁 02_Core_System": [
                "mcp_server.py",
                "notion_api_client.py",
                "📁 tools/",
                "📁 prompts/"
            ],
            "📁 03_Templates": [
                "📁 notion_templates/",
                "📁 content_templates/",
                "📁 automation_templates/"
            ],
            "📁 04_Documentation": [
                "📁 user_guides/",
                "📁 api_reference/",
                "📁 examples/"
            ],
            "📁 05_Assets": [
                "📁 images/",
                "📁 videos/",
                "📁 sample_content/"
            ],
            "📁 06_Support": [
                "📁 troubleshooting/",
                "📁 faq/",
                "📁 updates/"
            ]
        }
    }
    
    print("✅ Professional structure designed:")
    for main_folder, subfolders in structure.items():
        print(f"   {main_folder}")
        for item in subfolders:
            print(f"   ├── {item}")
    
    return structure

def consolidate_files():
    """Consolidate duplicate files and organize them properly."""
    
    print("\n🔄 CONSOLIDATING FILES")
    print("=" * 30)
    
    # Create consolidated documentation
    consolidated_docs = {
        "README.md": "Main setup and overview guide",
        "QUICKSTART.md": "Quick start guide for users", 
        "USER_GUIDE.md": "Comprehensive user guide",
        "API_REFERENCE.md": "Technical API documentation",
        "TROUBLESHOOTING.md": "Common issues and solutions"
    }
    
    print("📄 Consolidated documentation:")
    for doc, description in consolidated_docs.items():
        print(f"   ✅ {doc} - {description}")
    
    # Consolidate scripts
    consolidated_scripts = {
        "setup.py": "Main setup script",
        "populate_template.py": "Template population script",
        "test_system.py": "System testing script"
    }
    
    print("\n🐍 Consolidated scripts:")
    for script, description in consolidated_scripts.items():
        print(f"   ✅ {script} - {description}")
    
    return consolidated_docs, consolidated_scripts

def create_user_experience_optimizations():
    """Create user experience optimizations for template sales."""
    
    print("\n🎯 USER EXPERIENCE OPTIMIZATIONS")
    print("=" * 40)
    
    optimizations = {
        "📁 Clear Onboarding": [
            "Step-by-step setup guide",
            "Video tutorials",
            "Sample content to get started"
        ],
        "📁 Professional Documentation": [
            "Clean, organized guides",
            "Visual diagrams and screenshots", 
            "Troubleshooting section"
        ],
        "📁 Template Organization": [
            "Logical folder structure",
            "Clear naming conventions",
            "Easy customization options"
        ],
        "📁 Support Materials": [
            "FAQ section",
            "Update notifications",
            "Community resources"
        ]
    }
    
    for category, items in optimizations.items():
        print(f"   {category}")
        for item in items:
            print(f"   ├── {item}")
    
    return optimizations

def generate_cleanup_plan():
    """Generate a comprehensive cleanup plan."""
    
    print("\n📋 CLEANUP PLAN")
    print("=" * 20)
    
    plan = {
        "Phase 1: Documentation Consolidation": [
            "Merge duplicate documentation files",
            "Create single comprehensive user guide", 
            "Organize technical documentation"
        ],
        "Phase 2: Script Organization": [
            "Consolidate scattered Python scripts",
            "Create single setup script",
            "Organize utility scripts"
        ],
        "Phase 3: Folder Restructure": [
            "Create professional folder hierarchy",
            "Move files to appropriate locations",
            "Clean up temporary files"
        ],
        "Phase 4: User Experience": [
            "Create clear onboarding flow",
            "Add visual guides and screenshots",
            "Optimize for template sales"
        ]
    }
    
    for phase, tasks in plan.items():
        print(f"\n   {phase}")
        for task in tasks:
            print(f"   ├── {task}")
    
    return plan

if __name__ == "__main__":
    print("🚀 PROFESSIONAL NOTION TEMPLATE SYSTEM CLEANUP")
    print("=" * 60)
    
    # Analyze current structure
    current_issues = analyze_current_structure()
    
    # Create professional structure
    professional_structure = create_professional_structure()
    
    # Consolidate files
    consolidated_docs, consolidated_scripts = consolidate_files()
    
    # User experience optimizations
    ux_optimizations = create_user_experience_optimizations()
    
    # Generate cleanup plan
    cleanup_plan = generate_cleanup_plan()
    
    print("\n🎉 CLEANUP ANALYSIS COMPLETE!")
    print("Ready to implement professional template structure.")
