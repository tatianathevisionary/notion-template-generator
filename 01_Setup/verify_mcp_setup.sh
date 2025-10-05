#!/bin/bash
# Verification script for MCP server setup

echo "🔍 Notion Template Generator MCP Setup Verification"
echo "=================================================="
echo ""

# Check virtual environment
echo "1️⃣  Checking virtual environment..."
if [ -d "venv" ]; then
    echo "   ✅ Virtual environment exists"
else
    echo "   ❌ Virtual environment not found"
    echo "   Run: python3 -m venv venv"
    exit 1
fi

# Check .env file
echo ""
echo "2️⃣  Checking .env file..."
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"
    
    # Check for required variables (without showing values)
    if grep -q "NOTION_API_KEY" .env; then
        echo "   ✅ NOTION_API_KEY is set"
    else
        echo "   ❌ NOTION_API_KEY not found in .env"
    fi
    
    if grep -q "NOTION_PARENT_PAGE_ID" .env; then
        echo "   ✅ NOTION_PARENT_PAGE_ID is set"
    else
        echo "   ❌ NOTION_PARENT_PAGE_ID not found in .env"
    fi
else
    echo "   ❌ .env file not found"
    echo "   Run: ./setup_env.sh"
    exit 1
fi

# Check MCP dependencies
echo ""
echo "3️⃣  Checking MCP dependencies..."
source venv/bin/activate
if python -c "import mcp" 2>/dev/null; then
    echo "   ✅ MCP package installed"
else
    echo "   ❌ MCP package not installed"
    echo "   Run: pip install -r requirements_mcp.txt"
    exit 1
fi

# Test MCP server loading
echo ""
echo "4️⃣  Testing MCP server..."
result=$(python -c "
import sys
sys.path.insert(0, '.')
try:
    from mcp_server import mcp
    print(f'SUCCESS:{mcp.name}:{len(list(mcp._tool_manager._tools.values()))}:{len(list(mcp._prompt_manager._prompts.values()))}')
except Exception as e:
    print(f'ERROR:{str(e)}')
" 2>&1 | grep -E "(SUCCESS|ERROR)")

if echo "$result" | grep -q "SUCCESS"; then
    IFS=':' read -ra PARTS <<< "$result"
    echo "   ✅ MCP server loads successfully"
    echo "   📦 Server name: ${PARTS[1]}"
    echo "   🛠️  Available tools: ${PARTS[2]}"
    echo "   📚 Available prompts: ${PARTS[3]}"
else
    echo "   ❌ MCP server failed to load"
    echo "   Error: $result"
    exit 1
fi

# Show configuration
echo ""
echo "5️⃣  Cursor Configuration:"
echo "   Copy this to Cursor settings (Cmd+, → Search 'MCP'):"
echo ""
echo "   {"
echo "     \"mcpServers\": {"
echo "       \"notion-template-generator\": {"
echo "         \"command\": \"$(pwd)/venv/bin/python\","
echo "         \"args\": [\"$(pwd)/mcp_server.py\"]"
echo "       }"
echo "     }"
echo "   }"
echo ""

echo "=================================================="
echo "✅ All checks passed! Your MCP server is ready."
echo ""
echo "📋 Next Steps:"
echo "1. Copy the configuration above to Cursor settings"
echo "2. Make sure your Notion page is shared with your integration"
echo "3. Restart Cursor (Cmd+Q then reopen)"
echo "4. Start using the Notion tools in chat!"
echo ""
echo "📖 See CURSOR_MCP_SETUP.md for detailed instructions"

