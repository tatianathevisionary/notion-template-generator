# Notion Template Generator

A comprehensive Python automation tool for programmatically creating complete Notion systems via the Notion API. Supports **all 30+ Notion block types** including text, lists, media (images/video/audio), tables, columns, equations, embeds, and more!

**✨ NEW:** Complete block type implementation with full API parity! [See all block types →](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md)

## 🆕 New: Multi-Format Update Generator

Transform your weekly notes into professional updates across 4 formats automatically:
- **📄 Detailed Document** - Comprehensive stakeholder reports
- **💬 Slack Update** - Concise team updates
- **🔗 LinkedIn Post** - Engaging public updates
- **📝 Blog Post** - SEO-friendly long-form content

```bash
# Fill out the template
cp update_template.json my_update.json

# Generate all formats
python update_generator.py my_update.json
```

**[📖 Full Documentation](UPDATE_SYSTEM_README.md)**

---

## 🤖 New: MCP Server for AI Assistants

This project now includes a **Model Context Protocol (MCP) server** that enables AI assistants like Claude Desktop to access all project knowledge and capabilities!

**What is MCP?** An open standard by Anthropic that connects AI assistants to external tools and data sources.

### Quick Setup

```bash
# Install MCP dependencies
pip install -r requirements_mcp.txt

# Run the server
python mcp_server.py
```

### Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
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
```

### Capabilities

- **12 Prompts** - Complete project knowledge base
- **15 Tools** - Notion operations, database analysis, update generation, web research

**[📖 Full MCP Documentation](MCP_SERVER_README.md)** | **[🔗 MCP Resources](MCP_RESOURCES.md)**

---

## 🎯 What This Creates

This generator creates two complete Notion systems:

### 1. **AI Product Manager OS** (4 databases)
- **🎯 Opportunity Hub**: Track and evaluate product opportunities
- **📋 AI Product Spec Generator**: Create AI-powered product specifications
- **🧪 Experiment Tracker**: Monitor experiments and metrics
- **🚀 Launch & Growth Hub**: Manage launches and growth initiatives

### 2. **LinkedIn Content OS** (Complete Product Bundle) ⭐
- **🎨 Dashboard**: Beautiful cover page with navigation
- **📚 5-Day Onboarding**: Guided setup (Days 1-5 as separate pages)
- **📝 Content Hub**: Manage posts from idea to publish
- **🎯 Content Pillars**: Define your 3-5 core topics
- **🎤 Voice Discovery**: Interactive worksheet to find your voice
- **💡 Prompt Library**: 25+ ready-to-use AI prompts
- **📊 Weekly Review**: Track analytics and growth

**Total**: 12 pages, 5 databases, 300+ rich content blocks created!

## 🎨 Complete Block Type Support

Create rich Notion pages with **all 30+ block types**:

### Text & Lists
- Headings (3 levels, toggleable), Paragraphs, Quotes, Callouts
- Bulleted/Numbered lists, To-dos, Toggles

### Media & Files
- Images, Videos, Audio, PDFs, Files
- Bookmarks, Embeds

### Advanced
- Tables with rows/columns, Multi-column layouts
- LaTeX Equations, Synced blocks
- Table of Contents, Dividers, Breadcrumbs

**[📖 Complete Block Types Reference →](./docs/guides/COMPLETE_BLOCK_TYPES_REFERENCE.md)**

Example usage:
```python
from notion_api_client import heading_1, image, callout, table, code

blocks = [
    heading_1("My Project"),
    image("https://example.com/photo.jpg", caption="Screenshot"),
    callout("Important note!", icon="💡", color="blue_background"),
    code("print('Hello!')", language="python")
]

client.append_blocks(page_id, blocks)
```

## 📋 Prerequisites

- Python 3.8 or higher
- A Notion account with workspace owner permissions
- A Notion Integration (Internal) with API access

## 🆕 Latest Updates

**October 5, 2025**: Upgraded to **Notion API version 2025-09-03**
- ✅ Full support for multi-source databases
- ✅ Enhanced data source operations
- ✅ Backward compatible client wrapper
- ✅ All operations automatically handle data source IDs

See [API_MIGRATION_2025-09-03.md](API_MIGRATION_2025-09-03.md) for details.

## 🔧 Setup

### 1. Clone or Navigate to This Directory

```bash
cd "notion_template_generator"
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Notion credentials:
- **NOTION_API_KEY**: Your Notion Integration Secret (from https://www.notion.com/my-integrations)
- **NOTION_PARENT_PAGE_ID**: The ID of the parent page where templates will be created

### 5. Get Your Notion Integration Secret

1. Go to https://www.notion.com/my-integrations
2. Click **"+ New integration"**
3. Give it a name (e.g., "Template Generator")
4. Select your workspace
5. Click **"Submit"**
6. Copy the **"Internal Integration Secret"** and paste it into your `.env` file

### 6. Share Your Parent Page with the Integration

1. Open the Notion page where you want to create templates
2. Click **"Share"** in the top right
3. Invite your integration by name
4. Copy the page ID from the URL and add it to your `.env` file

**Example URL**: `https://www.notion.so/My-Workspace-abc123def456`  
**Page ID**: `abc123def456`

## 🚀 Usage

### Quick Start (Automated Setup)

```bash
./setup.sh
```

This will create a virtual environment and install all dependencies automatically.

### Create LinkedIn Content OS (Recommended) ⭐

```bash
source venv/bin/activate
python linkedin_content_os_complete.py
```

This creates the **complete LinkedIn Content OS** with:
- Dashboard cover page
- 5-day guided onboarding
- All 5 core databases
- Comprehensive examples throughout

### Create AI Product Manager OS

```bash
source venv/bin/activate
python main.py
```

This creates the **AI PM OS** with 4 databases showcasing product management workflows.

### Create LinkedIn Content OS (Basic Version)

```bash
source venv/bin/activate
python linkedin_content_os.py
```

This creates just the 3 core databases without onboarding.

## 📁 Project Structure

```
notion_template_generator/
│
├── 🐍 PYTHON SCRIPTS
│   ├── main.py                               # AI PM OS generator (4 databases)
│   ├── linkedin_content_os.py                # LinkedIn basic (3 databases)
│   ├── linkedin_content_os_complete.py       # LinkedIn FULL system (12 pages) ⭐
│   └── notion_api_client.py                  # Core API wrapper (15 block types)
│
├── 📄 JSON TEMPLATES
│   └── templates/
│       ├── opportunity_hub.json              # Opportunity tracking schema
│       ├── ai_product_spec.json              # Product spec schema
│       ├── experiment_tracker.json           # Experiment schema
│       └── launch_hub.json                   # Launch management schema
│
├── 📚 DOCUMENTATION
│   ├── README.md                             # This file
│   ├── QUICKSTART.md                         # Quick start guide
│   ├── ALL_BLOCK_TYPES_SHOWCASE.md           # All 15 block types explained
│   ├── CONTENT_GUIDE.md                      # Content breakdown
│   ├── LINKEDIN_CONTENT_OS_GUIDE.md          # LinkedIn system guide
│   ├── COMPLETE_SYSTEM_GUIDE.md              # Full system overview
│   ├── SUCCESS.md                            # Success stories
│   └── FINAL_RESULT.md                       # Results documentation
│
├── ⚙️ SETUP FILES
│   ├── requirements.txt                      # Python dependencies
│   ├── setup.sh                              # Auto-setup script
│   └── .gitignore                            # Git ignore rules
│
└── 🔐 CONFIG (Protected - not tracked)
    ├── .env                                  # Your API credentials
    └── venv/                                 # Python virtual environment
```

### What Each Script Does

| Script | Purpose | Creates |
|--------|---------|---------|
| `linkedin_content_os_complete.py` | **Full LinkedIn system** ⭐ | 1 dashboard + 5 onboarding pages + 5 databases |
| `main.py` | AI Product Manager OS | 4 databases with comprehensive examples |
| `linkedin_content_os.py` | LinkedIn basic | 3 core databases |
| `notion_api_client.py` | API wrapper & helpers | 15 block type functions |

## ✨ Features

### All 15 Notion Block Types Supported
- ✅ **Headings** (1, 2, 3) with colors and toggle capability
- ✅ **Paragraphs** with color options
- ✅ **Bulleted Lists** with colors
- ✅ **Numbered Lists** with colors
- ✅ **To-Do Checkboxes** (checked/unchecked)
- ✅ **Toggle Blocks** (collapsible sections)
- ✅ **Callouts** with custom icons and colors
- ✅ **Quotes** for testimonials and emphasis
- ✅ **Code Blocks** with 50+ language syntax highlighting
- ✅ **Table of Contents** (auto-generated navigation)
- ✅ **Bookmarks** (link previews)
- ✅ **Dividers** (section separators)

### Rich Content Features
- 20 color options (including backgrounds)
- Custom emoji icons for callouts
- Interactive checkboxes and toggles
- Syntax-highlighted code examples
- Comprehensive examples in every database

### Production-Ready Systems
- Not just empty templates - every database has detailed examples
- Step-by-step workflows built-in
- Best practices and pro tips throughout
- Ready to use immediately or sell as products

## 📊 By The Numbers

### LinkedIn Content OS Complete:
- **12 pages** (1 dashboard + 5 onboarding + 6 database samples)
- **5 databases** (Hub, Pillars, Voice, Prompts, Review)
- **300+ rich content blocks**
- **All 15 block types** demonstrated

### AI Product Manager OS:
- **4 databases** (Opportunity, Spec, Experiment, Launch)
- **4 comprehensive samples**
- **150+ rich content blocks**
- **12 block types** used

## 🔐 Security Best Practices

- **Never commit** your `.env` file to version control
- Keep your Notion API key secure and rotate it if exposed
- Use workspace-specific integrations (not shared across workspaces)
- Review integration permissions regularly

## 🎯 Example Output

When you run `linkedin_content_os_complete.py`, you get:

### Dashboard Page
```
🚀 LinkedIn Content OS - Welcome
├── Hero section with product overview
├── System features (all 6 modules)
├── "Start Here" guide
├── Quick navigation links
├── Before/After transformation
├── Pro tips with callouts
└── FAQ with toggles
```

### 5-Day Onboarding
```
📚 Day 1: Foundation → Define your LinkedIn goal
📚 Day 2: Voice Discovery → Find your authentic voice
📚 Day 3: Content Pillars → Choose 3-5 core topics
📚 Day 4: First Post → Write and structure content
📚 Day 5: Launch & Rhythm → Publish and build habits
```

### Core Databases
```
📝 Content Hub → Full post workflow (60+ blocks)
🎯 Content Pillars → Strategic planning (35+ blocks)
🎤 Voice Discovery → 6-section worksheet (50+ blocks)
💡 Prompt Library → AI prompts with examples (25+ blocks)
📊 Weekly Review → Analytics template (40+ blocks)
```

## 📚 Documentation

### User Guides
- **COMPLETE_SYSTEM_GUIDE.md** - Overview of the LinkedIn Content OS
- **ALL_BLOCK_TYPES_SHOWCASE.md** - Learn about all 15 block types
- **LINKEDIN_CONTENT_OS_GUIDE.md** - Detailed usage guide
- **QUICKSTART.md** - Quick reference

### Developer Guides
- **AGENTS.md** - 🤖 AI Assistant rules, commands, and patterns
- **API_MIGRATION_2025-09-03.md** - API upgrade documentation
- **README.md** - This file

## 🚀 Use Cases

### Personal Use
- Build your own LinkedIn presence
- Manage product development workflows
- Track experiments and launches
- Organize content creation

### As a Product
- The LinkedIn Content OS is a complete deliverable
- Ready to sell on Gumroad or similar platforms
- All examples included - no assembly required
- Professional quality with best practices built-in

## 📚 API Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Notion SDK for Python](https://github.com/ramnes/notion-sdk-py)
- [Working with Databases](https://developers.notion.com/docs/working-with-databases)
- [Working with Page Content](https://developers.notion.com/docs/working-with-page-content)
- [Block Reference](https://developers.notion.com/reference/block)

## 🤝 Contributing

This is a personal automation project, but feel free to fork and adapt it for your own use cases.

## 📝 License

MIT License - feel free to use this as a template for your own Notion automation projects.

---

## 🎉 Quick Start

```bash
# 1. Setup (one time)
cd notion_template_generator
./setup.sh

# 2. Configure
# Edit .env with your Notion API key and parent page ID

# 3. Create your system
source venv/bin/activate
python linkedin_content_os_complete.py

# 4. Open Notion and explore!
```

**Created with ❤️ for Product Managers and Content Creators**
