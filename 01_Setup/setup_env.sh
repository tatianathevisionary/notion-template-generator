#!/bin/bash
# Quick setup script for MCP server environment

echo "🚀 Notion Template Generator MCP Setup"
echo "======================================"
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

echo "Let's configure your Notion API credentials..."
echo ""

# Get Notion API Key
echo "1️⃣  Notion API Key"
echo "   Get it from: https://www.notion.so/my-integrations"
read -p "   Enter your Notion API Key: " api_key

echo ""
echo "2️⃣  Notion Parent Page ID"
echo "   This is the page where templates will be created"
echo "   Find it in your Notion page URL (the long string)"
read -p "   Enter your Parent Page ID: " page_id

# Create .env file
cat > .env << EOF
# Notion API Configuration
# Generated on $(date)
NOTION_API_KEY=$api_key
NOTION_PARENT_PAGE_ID=$page_id
EOF

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Make sure you've shared your Notion page with the integration"
echo "2. Add the MCP configuration to Cursor settings"
echo "3. Restart Cursor"
echo ""
echo "See CURSOR_MCP_SETUP.md for detailed instructions!"

