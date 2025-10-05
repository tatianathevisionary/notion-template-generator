# Cursor MCP Server Setup Guide

## ✅ Step 1: Dependencies Installed
The MCP dependencies have been installed successfully!

## 📝 Step 2: Create Environment File

Create a file named `.env` in this directory (`/Users/tatiana/Cloning me/notion_template_generator/`) with the following content:

```env
# Notion API Configuration
NOTION_API_KEY=your_notion_api_key_here
NOTION_PARENT_PAGE_ID=your_parent_page_id_here
```

### How to Get Your Credentials:

1. **NOTION_API_KEY**: 
   - Go to https://www.notion.so/my-integrations
   - Click "+ New integration"
   - Give it a name (e.g., "Template Generator")
   - Copy the "Internal Integration Token"

2. **NOTION_PARENT_PAGE_ID**:
   - Open the Notion page where you want templates created
   - Copy the URL - it looks like: `https://www.notion.so/Your-Page-123abc456def...`
   - The page ID is the long string at the end (after the last `/` or `-`)
   - Important: Share this page with your integration!
     - Open the page → Click "Share" → Invite your integration

## ⚙️ Step 3: Configure Cursor MCP Settings

1. **Open Cursor Settings**:
   - Press `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)
   - Or go to: Cursor → Settings

2. **Find MCP Settings**:
   - Search for "MCP" in settings
   - Look for "Model Context Protocol" or "MCP Servers"

3. **Add This Configuration**:

```json
{
  "mcpServers": {
    "notion-template-generator": {
      "command": "/Users/tatiana/Cloning me/notion_template_generator/venv/bin/python",
      "args": ["/Users/tatiana/Cloning me/notion_template_generator/mcp_server.py"]
    }
  }
}
```

**Note**: We're using the virtual environment's Python to ensure all dependencies are available. The environment variables will be automatically loaded from the `.env` file by the MCP server.

## 🔄 Step 4: Restart Cursor

After adding the configuration:
1. Save the settings
2. Completely quit Cursor (`Cmd + Q`)
3. Reopen Cursor

## ✨ Step 5: Test the Connection

Once Cursor restarts, you should be able to use the Notion tools! Try asking:
- "Show me available Notion tools"
- "Create a new Notion page"
- "Query my Notion database"

## 🛠️ Available Tools

Your MCP server exposes:

### Notion Tools:
- `update_notion_page` - Update existing pages
- `query_notion_database` - Query databases
- `create_notion_database` - Create new databases
- `get_database_schema` - Get database structure

### Research Tools:
- `search_web` - Web search capabilities
- `analyze_content` - Content analysis

### Update Tools:
- `generate_multi_format_update` - Generate updates in multiple formats
- `create_update_template` - Create update templates
- `validate_update_data` - Validate update data

### Database Tools:
- `analyze_database` - Analyze database structure
- Various database management tools

## 📚 Available Prompts (Knowledge Base):

The server also provides 12 strategic knowledge documents:
- Notion API guides
- LinkedIn Content OS
- AI PM fundamentals
- Complete block types reference
- And more!

## 🐛 Troubleshooting

### MCP Server Not Showing Up:
1. Verify the `.env` file exists with correct credentials
2. Check that the path in the config is absolute and correct
3. Make sure you're using the venv Python path (not system Python)
4. Check Cursor's developer console for errors

### Test the Server Manually:
```bash
cd "/Users/tatiana/Cloning me/notion_template_generator"
source venv/bin/activate
python mcp_server.py
```

If it starts without errors and shows "Server loaded successfully", it's working!

### Quick Test:
```bash
cd "/Users/tatiana/Cloning me/notion_template_generator"
source venv/bin/activate
python -c "from mcp_server import mcp; print(f'✅ {mcp.name} - {len(list(mcp._tool_manager._tools.values()))} tools')"
```

### Check Logs:
The server logs to stderr. Check Cursor's output panel or developer console for any error messages.

## 📖 Additional Resources

- MCP Documentation: https://modelcontextprotocol.io/
- Notion API Docs: https://developers.notion.com/
- Project README: See `README.md` in this directory

---

**Need Help?** Make sure:
- ✅ Dependencies installed (`pip install -r requirements_mcp.txt`)
- ✅ `.env` file created with valid credentials
- ✅ Notion page shared with your integration
- ✅ Cursor settings updated with MCP config
- ✅ Cursor restarted
