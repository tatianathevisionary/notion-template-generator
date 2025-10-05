#!/usr/bin/env python3
"""
LinkedIn Content OS Template - Setup Script
Professional setup for template users
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 LinkedIn Content OS Template Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Install requirements
    print("📦 Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️  .env file not found. Creating template...")
        create_env_template()
    
    # Setup complete
    print("🎉 Setup complete!")
    print("Next steps:")
    print("1. Add your Notion API key to .env")
    print("2. Run: python populate_template.py")
    print("3. Start creating content!")

def create_env_template():
    """Create .env template file."""
    env_content = """# LinkedIn Content OS Template Configuration
# Add your Notion API key below
NOTION_API_KEY=your_notion_api_key_here
NOTION_PARENT_PAGE_ID=your_parent_page_id_here

# Optional: Customize these settings
DEBUG=False
LOG_LEVEL=INFO
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env template")

if __name__ == "__main__":
    main()
