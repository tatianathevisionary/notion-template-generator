# Notion Template Generator

> A comprehensive Python toolkit for building complete Notion systems programmatically using the Notion API 2025-09-03

[![Notion API](https://img.shields.io/badge/Notion%20API-2025--09--03-black)](https://developers.notion.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Block Types](https://img.shields.io/badge/Block%20Types-30%2B-green)](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md)

---

## 🎯 What We've Built

This project provides **three powerful components** for working with Notion:

### 1. 🎨 Complete Block Type Library (30+ Types)

A production-ready Python library supporting **all creatable Notion block types** with full API parity:

**Text & Lists (11 types)**
- Headings (3 levels, toggleable), Paragraphs, Quotes, Callouts, Code blocks
- Bulleted/Numbered lists, To-dos, Toggles, Table of Contents

**Media & Files (6 types)**
- Images, Videos, Audio, PDFs, Files, Embeds

**Advanced Layouts (8 types)**
- Tables with rows/columns, Multi-column layouts (column lists & columns)
- LaTeX Equations, Synced blocks, Dividers, Breadcrumbs, Bookmarks

```python
from notion_api_client import heading_1, image, callout, table, equation, column_list, column

# Create rich content with any block type
blocks = [
    heading_1("My Project", is_toggleable=True),
    image("https://example.com/photo.jpg", caption="Screenshot"),
    callout("Important!", icon="💡", color="blue_background"),
    equation("e=mc^2"),
    table(table_width=3, has_column_header=True)
]
```

**[📖 See All 30+ Block Types →](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md)**

---

### 2. 📦 Ready-to-Deploy Notion Systems

Two complete, production-ready Notion systems that you can deploy instantly:

#### **AI Product Manager OS** (4 Databases)
- 🎯 Opportunity Hub - Track and evaluate opportunities
- 📋 AI Product Spec Generator - Create product specs
- 🧪 Experiment Tracker - Monitor experiments
- 🚀 Launch & Growth Hub - Manage launches

#### **LinkedIn Content OS** ⭐ (12 Pages, 5 Databases)
- 🎨 Dashboard - Beautiful cover page
- 📚 5-Day Onboarding - Guided setup journey
- 📝 Content Hub - Full post workflow
- 🎯 Content Pillars - Strategic planning
- 🎤 Voice Discovery - Find your voice
- 💡 Prompt Library - 25+ AI prompts
- 📊 Weekly Review - Analytics tracking

**Total: 300+ rich content blocks across 12 pages and 5 databases!**

---

### 3. 🤖 MCP Server for AI Assistants

A Model Context Protocol (MCP) server that connects AI assistants like Claude to your Notion workspace:

**12 Knowledge Prompts** - Complete project documentation
- System guides, API references, block type examples
- Best practices and implementation patterns

**15 Callable Tools** - Powerful operations
- Notion database and page operations
- Database analysis and enhancement
- Multi-format update generation
- Web research capabilities

**[📖 MCP Server Documentation →](./docs/mcp/MCP_SERVER_README.md)**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Notion account with workspace owner permissions
- A Notion Integration (Internal) with API access

### Installation

```bash
# 1. Clone or navigate to the directory
cd notion_template_generator

# 2. Run automated setup (creates venv, installs dependencies)
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. **Create a Notion Integration**
   - Go to https://www.notion.com/my-integrations
   - Click "New integration"
   - Name it (e.g., "Template Generator")
   - Copy the Integration Secret

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env and add:
   # NOTION_API_KEY=your_integration_secret
   # NOTION_PARENT_PAGE_ID=your_page_id
   ```

3. **Share a Notion Page with Your Integration**
   - Open a Notion page
   - Click "Share" → Invite your integration
   - Copy the page ID from the URL

---

## 💻 Usage Examples

### Create Complete Notion Systems

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Deploy LinkedIn Content OS (Full system - RECOMMENDED)
python scripts/generators/linkedin_content_os_complete.py

# Deploy AI Product Manager OS
python scripts/generators/main.py

# Deploy LinkedIn Content OS (Basic - 3 databases only)
python scripts/generators/linkedin_content_os.py
```

### Use the Block Type Library

```python
from notion_api_client import (
    NotionTemplateClient,
    heading_1, heading_2, paragraph, callout,
    bullet_list_item, to_do, code, image, table
)

# Initialize client
client = NotionTemplateClient()

# Build rich content
page_blocks = [
    # Text blocks
    heading_1("Project Documentation"),
    paragraph("Welcome to our comprehensive guide."),
    callout("Key insight!", icon="💡", color="yellow_background"),
    
    # Lists
    heading_2("Features"),
    bullet_list_item("Fast and reliable"),
    bullet_list_item("Easy to use"),
    to_do("Complete setup", checked=True),
    
    # Media
    image("https://example.com/diagram.png", caption="Architecture"),
    
    # Code
    code(
        "from notion_api_client import NotionTemplateClient\n"
        "client = NotionTemplateClient()",
        language="python"
    )
]

# Create page
page = client.create_page(
    parent_id=database_id,
    title="Getting Started",
    children=page_blocks
)
```

### Generate Multi-Format Updates

```bash
# Fill out the template
cp templates/update_template.json my_update.json
# Edit my_update.json with your project data

# Generate all formats (Document, Slack, LinkedIn, Blog)
python scripts/utilities/update_generator.py my_update.json
```

**[📖 Update System Guide →](./docs/guides/UPDATE_SYSTEM_README.md)**

### Use the MCP Server with Claude Desktop

```bash
# Install MCP dependencies
pip install -r requirements_mcp.txt

# Add to Claude Desktop config (~/.../claude_desktop_config.json):
{
  "mcpServers": {
    "notion-template-generator": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {
        "NOTION_API_KEY": "your_key",
        "NOTION_PARENT_PAGE_ID": "your_page_id"
      }
    }
  }
}

# Restart Claude Desktop and start using Notion tools!
```

**[📖 Full MCP Setup Guide →](./docs/mcp/MCP_SERVER_README.md)**

---

## 📁 Project Structure

```
notion_template_generator/
├── 📘 Core Library
│   ├── notion_api_client.py          # 27 block type helpers + API wrapper
│   ├── mcp_server.py                 # MCP server for AI assistants
│   └── requirements.txt              # Python dependencies
│
├── 🐍 Scripts (Organized by Purpose)
│   ├── generators/                   # Template generators
│   │   ├── linkedin_content_os_complete.py  # Full LinkedIn system ⭐
│   │   ├── main.py                   # AI PM OS (4 databases)
│   │   └── linkedin_content_os.py    # LinkedIn basic (3 databases)
│   ├── enhancements/                 # Database enhancement tools
│   │   ├── notion_enhancer.py        # Advanced analyzer & enhancer
│   │   └── apply_enhancements_fixed.py  # Batch enhancement tool
│   └── utilities/                    # Helper scripts
│       ├── update_generator.py       # Multi-format updates
│       ├── test_retrieve_structure.py
│       └── export_all_linkedin_databases.py
│
├── 📚 Documentation (Comprehensive Guides)
│   ├── guides/                       # Implementation guides
│   │   ├── COMPLETE_BLOCK_TYPES_REFERENCE.md  # All 30+ block types ⭐
│   │   ├── API_MIGRATION_2025-09-03.md
│   │   ├── ALL_BLOCK_TYPES_SHOWCASE.md
│   │   ├── COMPLETE_SYSTEM_GUIDE.md
│   │   ├── CONTENT_GUIDE.md
│   │   ├── LINKEDIN_CONTENT_OS_GUIDE.md
│   │   ├── UPDATE_SYSTEM_README.md
│   │   └── README.md                 # Guide navigation
│   ├── mcp/                          # MCP server docs
│   │   ├── MCP_SERVER_README.md      # Complete MCP guide
│   │   ├── MCP_RESOURCES.md          # External resources
│   │   └── MCP_CONVERSION_COMPLETE.md
│   ├── agents/                       # AI assistant rules
│   │   └── AGENTS.md
│   ├── sessions/                     # Session summaries
│   └── updates/                      # Generated update examples
│
├── 🗂️ MCP Components
│   ├── prompts/                      # 12 knowledge base documents
│   │   ├── agents.prompt
│   │   ├── api_migration.prompt
│   │   ├── complete_system_guide.prompt
│   │   └── ... (9 more)
│   └── tools/                        # 15 callable tools
│       ├── notion_tool.py            # Notion operations
│       ├── research_tool.py          # Web research
│       ├── update_tool.py            # Update generation
│       └── database_tool.py          # Database analysis
│
├── 📦 Data & Templates
│   ├── data/                         # JSON exports and reports
│   └── templates/                    # JSON templates
│
├── 📄 Root Documentation
│   ├── README.md                     # This file
│   ├── QUICKSTART.md                 # Quick reference
│   ├── PROJECT_STRUCTURE.md          # Detailed structure
│   ├── NOTION_API_COMPLETE_IMPLEMENTATION.md  # API implementation
│   ├── COMPLETION_SUMMARY.md         # Task summary
│   └── REORGANIZATION_SUMMARY.md     # File organization
│
└── ⚙️ Configuration
    ├── .env                          # Your credentials (not tracked)
    ├── .env.example                  # Template for .env
    ├── requirements.txt              # Main dependencies
    ├── requirements_mcp.txt          # MCP dependencies
    └── setup.sh                      # Automated setup script
```

---

## 🎨 What You Can Build

### 📄 Rich Documentation Pages

```python
blocks = [
    table_of_contents(),
    heading_1("Documentation"),
    callout("Quick start guide", icon="🚀"),
    code("npm install", language="bash"),
    image("https://example.com/architecture.png"),
    table(table_width=3, has_column_header=True)
]
```

### 🎬 Media-Rich Galleries

```python
blocks = [
    heading_1("Project Gallery"),
    video("https://youtube.com/watch?v=demo"),
    image("https://example.com/screenshot1.png", caption="Feature A"),
    audio("https://example.com/podcast.mp3", caption="Episode 1"),
    pdf("https://example.com/whitepaper.pdf", caption="Research")
]
```

### 📊 Complex Data Layouts

```python
# Multi-column layout
col_list = column_list()
# With custom width ratios
col1 = column(width_ratio=0.67)  # 2/3 width
col2 = column(width_ratio=0.33)  # 1/3 width

# Tables with formatted data
tbl = table(table_width=4, has_column_header=True)
rows = [
    table_row([["Name"], ["Email"], ["Status"], ["Notes"]]),
    table_row([["John"], ["john@ex.com"], ["Active"], ["VIP"]])
]
```

### 🔬 Technical Content

```python
blocks = [
    heading_2("Mathematical Proof"),
    equation("\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}"),
    paragraph("This demonstrates..."),
    code("def solve(): return result", language="python"),
    synced_block(children=[paragraph("Synced across pages!")])
]
```

---

## 📚 Complete Documentation

### Quick Reference
- **[QUICKSTART.md](./QUICKSTART.md)** - Get started in 5 minutes
- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - Detailed file structure
- **[COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md)** - What we've built

### Block Types & API
- **[COMPLETE_BLOCK_TYPES_REFERENCE.md](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md)** ⭐ - All 30+ block types
- **[ALL_BLOCK_TYPES_SHOWCASE.md](./docs/guides/ALL_BLOCK_TYPES_SHOWCASE.md)** - Visual examples
- **[API_MIGRATION_2025-09-03.md](./docs/guides/API_MIGRATION_2025-09-03.md)** - API version guide

### System Guides
- **[COMPLETE_SYSTEM_GUIDE.md](./docs/guides/COMPLETE_SYSTEM_GUIDE.md)** - Full system overview
- **[LINKEDIN_CONTENT_OS_GUIDE.md](./docs/guides/LINKEDIN_CONTENT_OS_GUIDE.md)** - LinkedIn system
- **[UPDATE_SYSTEM_README.md](./docs/guides/UPDATE_SYSTEM_README.md)** - Update generator

### MCP Server
- **[MCP_SERVER_README.md](./docs/mcp/MCP_SERVER_README.md)** - Complete MCP guide
- **[MCP_RESOURCES.md](./docs/mcp/MCP_RESOURCES.md)** - External resources
- **[MCP_CONVERSION_COMPLETE.md](./docs/mcp/MCP_CONVERSION_COMPLETE.md)** - Implementation

### AI Assistant
- **[AGENTS.md](./docs/agents/AGENTS.md)** - AI assistant rules and commands

---

## 📊 By The Numbers

### Block Type Library
- **30+ block types** fully implemented
- **27 helper functions** ready to use
- **100% API parity** with Notion 2025-09-03
- **50+ code examples** in documentation

### Ready-to-Deploy Systems
- **2 complete systems** (AI PM OS + LinkedIn OS)
- **12 pages** with rich content
- **9 databases** with comprehensive examples
- **300+ content blocks** pre-built

### MCP Server
- **12 knowledge prompts** (complete documentation)
- **15 callable tools** (Notion + research + analysis)
- **Production-ready** for Claude Desktop

### Documentation
- **1,400+ lines** of code added
- **900+ lines** of documentation
- **15+ comprehensive guides**
- **Full API coverage** documented

---

## ✨ Key Features

### Production-Ready Code
- ✅ All block types validated against official API
- ✅ Type hints and docstrings throughout
- ✅ Error handling and logging
- ✅ Backward compatible with API updates

### Comprehensive Examples
- ✅ Every database includes detailed examples
- ✅ Step-by-step workflows built-in
- ✅ Best practices demonstrated
- ✅ Ready to use or customize

### Developer-Friendly
- ✅ Clean, organized project structure
- ✅ Extensive documentation with code examples
- ✅ Easy-to-extend architecture
- ✅ Well-commented code

### AI Assistant Integration
- ✅ MCP server for Claude Desktop
- ✅ Complete project knowledge accessible to AI
- ✅ Callable tools for automation
- ✅ Prompt library included

---

## 🎯 Use Cases

### For Developers
- Build custom Notion integrations
- Automate workspace setup
- Create template marketplaces
- Generate documentation programmatically

### For Product Managers
- Deploy AI PM OS for product workflow
- Track opportunities and experiments
- Manage launches and growth initiatives
- Create product specifications

### For Content Creators
- Deploy LinkedIn Content OS
- Manage content pipeline
- Track performance metrics
- Build content strategy

### For Businesses
- Automate workspace provisioning
- Create team templates
- Build internal tools
- Integrate with existing systems

---

## 🔐 Security Best Practices

- ✅ Never commit `.env` files to version control
- ✅ Rotate API keys regularly
- ✅ Use workspace-specific integrations
- ✅ Review integration permissions
- ✅ Keep dependencies updated

---

## 📖 Learning Resources

### Start Here
1. [QUICKSTART.md](./QUICKSTART.md) - Get running in 5 minutes
2. [COMPLETE_BLOCK_TYPES_REFERENCE.md](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md) - Learn all block types
3. [COMPLETE_SYSTEM_GUIDE.md](./docs/guides/COMPLETE_SYSTEM_GUIDE.md) - Understand the systems

### Go Deeper
- Deploy a complete system and explore the code
- Read the block types showcase
- Try building your own pages with the library
- Set up the MCP server with Claude

### External Resources
- [Notion API Documentation](https://developers.notion.com)
- [Notion SDK for Python](https://github.com/ramnes/notion-sdk-py)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

## 🆕 Latest Updates

**October 5, 2025**
- ✅ Complete block type implementation (30+ types)
- ✅ Upgraded to Notion API 2025-09-03
- ✅ Full MCP server with 12 prompts + 15 tools
- ✅ Reorganized project structure
- ✅ Comprehensive documentation (900+ lines)
- ✅ Production-ready for all use cases

**[See Detailed Changelog →](./COMPLETION_SUMMARY.md)**

---

## 🤝 Contributing

This is a personal automation project, but you're welcome to:
- Fork and adapt for your needs
- Submit issues for bugs
- Share your implementations
- Suggest improvements

---

## 📝 License

MIT License - Free to use for personal and commercial projects.

---

## 🎉 Get Started Now

```bash
# 1. Setup
cd notion_template_generator
./setup.sh

# 2. Configure
cp .env.example .env
# Edit .env with your Notion API key and page ID

# 3. Deploy a system
source venv/bin/activate
python scripts/generators/linkedin_content_os_complete.py

# 4. Or use the library
python
>>> from notion_api_client import heading_1, callout, image
>>> # Start building!
```

**Questions?** Check out the [documentation](./docs/guides/README.md) or explore the [code examples](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md).

---

**Created with ❤️ for Developers, Product Managers, and Content Creators**

*Making Notion automation accessible to everyone.*