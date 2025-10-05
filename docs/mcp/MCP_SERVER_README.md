# Notion Template Generator MCP Server

This directory contains a fully functional **Model Context Protocol (MCP) server** that exposes prompts (knowledge base) and tools (capabilities) for AI assistants to help with Notion automation, content generation, and research.

## 🎯 What is an MCP Server?

The Model Context Protocol (MCP) is an open standard created by Anthropic that enables AI assistants to securely connect to external data sources and tools. This server acts as a bridge between AI assistants (like Claude Desktop) and your Notion workspace.

**Learn more:** https://www.anthropic.com/news/model-context-protocol

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Make sure you're in the project directory
cd "/Users/tatiana/Cloning me/notion_template_generator"

# Activate virtual environment (if not already active)
source venv/bin/activate

# Install MCP requirements
pip install -r requirements_mcp.txt
```

### 2. Configure Environment Variables

Make sure your `.env` file contains:

```bash
NOTION_API_KEY=your_notion_api_key_here
NOTION_PARENT_PAGE_ID=your_parent_page_id_here
```

### 3. Run the Server

```bash
# Test the server directly
python mcp_server.py
```

### 4. Connect to Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "notion-template-generator": {
      "command": "python",
      "args": [
        "/absolute/path/to/notion_template_generator/mcp_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "your_key_here",
        "NOTION_PARENT_PAGE_ID": "your_page_id_here"
      }
    }
  }
}
```

**Replace `/absolute/path/to/` with your actual project path!**

Then restart Claude Desktop.

## 📚 Server Capabilities

### Prompts (Knowledge Base)

The server exposes 12 strategic knowledge documents:

1. **agents_guide** - AI Assistant Rules & Commands
2. **api_migration_guide** - Notion API 2025-09-03 Migration Guide
3. **block_types_reference** - All 15 Notion block types with examples
4. **system_guide** - Complete system documentation
5. **content_creation_guide** - Content creation best practices
6. **linkedin_content_os_guide** - LinkedIn Content OS implementation
7. **quickstart** - Quick start guide
8. **project_overview** - High-level project overview
9. **success_stories** - Implementation examples
10. **update_system_guide** - Multi-format update generation
11. **session_summary** - Recent development work summary
12. **weekly_update_example** - Example high-quality weekly update

### Tools (Callable Functions)

The server exposes 15 tools across 4 categories:

#### Notion Tools (4)
- `update_page` - Update a Notion page with new content blocks
- `query_database` - Query a database with filters and sorting
- `create_database` - Create a new database with schema
- `get_schema` - Retrieve complete database schema

#### Research Tools (2)
- `web_search` - Perform web searches (placeholder)
- `analyze_text` - Analyze text content for insights

#### Update Tools (3)
- `generate_update` - Generate multi-format updates (Doc, Slack, LinkedIn, Blog)
- `get_update_template` - Get update template structure
- `validate_update` - Validate update data before generation

#### Database Tools (4)
- `analyze_db` - Analyze database structure and content
- `enhance_db` - Add rich content to databases
- `export_db_structure` - Export database schema to JSON
- `compare_dbs` - Compare two databases

## 💡 Usage Examples

### In Claude Desktop

Once connected, you can ask Claude:

```
"Show me the agents_guide prompt to understand how to work with this project"

"Use the create_database tool to create a new Task Tracker with Status and Priority properties"

"Generate a weekly update for my project using the generate_update tool"

"Analyze the database with ID abc123 and tell me about its structure"
```

### Command Line Testing

You can test individual tools by importing them in Python:

```python
from tools.notion_tool import get_database_schema
from tools.update_tool import create_update_template

# Get a database schema
result = get_database_schema("your_database_id")
print(result)

# Get update template
template = create_update_template()
print(template)
```

## 🏗️ Architecture

```
notion_template_generator/
├── mcp_server.py                # Main MCP server (FastMCP)
├── prompts/                     # Knowledge base (.prompt files)
│   ├── agents.prompt
│   ├── api_migration.prompt
│   └── ... (12 total)
├── tools/                       # Capabilities (Python functions)
│   ├── __init__.py
│   ├── notion_tool.py          # Notion API operations
│   ├── research_tool.py        # Web search capabilities
│   ├── update_tool.py          # Multi-format updates
│   └── database_tool.py        # Database analysis
└── requirements_mcp.txt        # MCP dependencies
```

## 🔧 Development

### Adding New Prompts

1. Create a new `.prompt` file in the `prompts/` directory
2. Add a new `@mcp.prompt()` function in `mcp_server.py`
3. Restart the server

### Adding New Tools

1. Add your function to the appropriate tool file in `tools/`
2. Export it from `tools/__init__.py`
3. Add a new `@mcp.tool()` wrapper in `mcp_server.py`
4. Restart the server

### Logging

The server logs to **stderr** (not stdout) to comply with STDIO transport requirements. View logs in Claude Desktop at:

- `~/Library/Logs/Claude/mcp-server-notion-template-generator.log`

## 📖 Resources

- **MCP Documentation:** https://modelcontextprotocol.io/
- **Build an MCP Server:** https://modelcontextprotocol.io/docs/develop/build-server
- **Build an MCP Client:** https://modelcontextprotocol.io/docs/develop/build-client
- **Building with LLMs:** https://modelcontextprotocol.io/tutorials/building-mcp-with-llms

## 🐛 Troubleshooting

### Server not showing up in Claude Desktop

1. Check that the path in `claude_desktop_config.json` is **absolute**, not relative
2. Verify Python is in your PATH: `which python`
3. Check Claude Desktop logs: `tail -f ~/Library/Logs/Claude/mcp*.log`
4. Restart Claude Desktop after config changes

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements_mcp.txt

# Verify mcp package is installed
pip list | grep mcp
```

### Environment variables not working

Make sure you're passing them in the `env` section of `claude_desktop_config.json`, not relying on shell environment.

## 🎉 Success!

Your MCP server is now ready to empower AI assistants with Notion automation capabilities!

---

**Created:** October 5, 2025  
**Status:** Production Ready ✅  
**Version:** 1.0.0
