# 📁 Project Structure

## Overview

This document explains the organization of the Notion Template Generator project.

---

## 🗂️ Root Directory

Essential files that should remain at the project root:

```
notion_template_generator/
├── README.md                  # Main project documentation
├── QUICKSTART.md             # Quick start guide
├── requirements.txt          # Python dependencies
├── requirements_mcp.txt      # MCP-specific dependencies
├── setup.sh                  # Automated setup script
├── mcp_server.py            # Main MCP server (FastMCP)
├── notion_api_client.py     # Core Notion API wrapper
├── .env                     # Environment variables (gitignored)
└── .gitignore              # Git ignore rules
```

---

## 📚 /docs - Documentation

All project documentation organized by category.

### /docs/agents
- `AGENTS.md` - AI assistant rules, commands, and project context

### /docs/guides
- `API_MIGRATION_2025-09-03.md` - Notion API upgrade guide
- `ALL_BLOCK_TYPES_SHOWCASE.md` - Complete Notion block types reference
- `COMPLETE_SYSTEM_GUIDE.md` - Full LinkedIn Content OS guide
- `CONTENT_GUIDE.md` - Rich text content implementation guide
- `LINKEDIN_CONTENT_OS_GUIDE.md` - LinkedIn system user guide
- `UPDATE_SYSTEM_README.md` - Multi-format update generator guide

### /docs/mcp
- `MCP_CONVERSION_COMPLETE.md` - MCP server conversion summary
- `MCP_RESOURCES.md` - MCP documentation links and resources
- `MCP_SERVER_README.md` - MCP server setup and usage

### /docs/sessions
- `SESSION_SUMMARY_2025-10-05.md` - Development session summary
- `SUCCESS.md` - Project success documentation
- `FINAL_RESULT.md` - Final implementation results
- `WEEKLY_UPDATE_2025-10-05.md` - Example weekly update

### /docs/updates
- `notion_template_generator_blog_2025-10-05.md` - Blog post format
- `notion_template_generator_linkedin_2025-10-05.txt` - LinkedIn post
- `notion_template_generator_slack_2025-10-05.txt` - Slack update
- `notion_template_generator_update_2025-10-05.md` - Detailed update

---

## 🐍 /scripts - Python Scripts

All Python scripts organized by purpose.

### /scripts/generators
Main Notion template generators:
- `main.py` - AI Product Manager OS (4 databases)
- `linkedin_content_os.py` - LinkedIn OS basic (3 databases)
- `linkedin_content_os_complete.py` - LinkedIn OS complete (12+ pages)

**Usage:**
```bash
cd scripts/generators
python linkedin_content_os_complete.py
```

### /scripts/enhancements
Database enhancement tools:
- `apply_enhancements.py` - Original enhancement script
- `apply_enhancements_fixed.py` - Fixed version with proper property handling
- `notion_enhancer.py` - Advanced database analyzer and enhancer

**Usage:**
```bash
cd scripts/enhancements
python apply_enhancements_fixed.py
```

### /scripts/utilities
Utility scripts and tools:
- `test_retrieve_structure.py` - Database structure retrieval and display
- `export_all_linkedin_databases.py` - Export all LinkedIn OS databases
- `update_generator.py` - Multi-format update generator

**Usage:**
```bash
cd scripts/utilities
python update_generator.py ../templates/update_template.json
```

---

## 📄 /templates - JSON Templates

Template files for various purposes:
- `update_template.json` - Weekly update template structure

---

## 💾 /data - Generated Data

JSON exports and analysis reports:
- `linkedin_content_os_structure_20251005_005350.json` - Database structures
- `notion_enhancement_report_20251005_005706.json` - Enhancement analysis

---

## 💡 /prompts - MCP Prompts

Knowledge base prompts for the MCP server (`.prompt` files):
- `agents.prompt` - AI agent rules and commands
- `api_migration.prompt` - API migration guide
- `block_types.prompt` - Block types reference
- `system_guide.prompt` - Complete system guide
- `content_guide.prompt` - Content creation guide
- `linkedin_guide.prompt` - LinkedIn OS guide
- `quickstart.prompt` - Quick start guide
- `readme.prompt` - Main README
- `success.prompt` - Success stories
- `update_system.prompt` - Update system guide
- `session_summary.prompt` - Session summary
- `weekly_update.prompt` - Weekly update example

---

## 🔧 /tools - MCP Tools

Python modules exposing callable functions via MCP:

### Tool Categories:
1. **Notion Operations** (`tools/notion_tool.py`)
   - `update_notion_page()` - Update page content
   - `query_notion_database()` - Query databases
   - `create_notion_database()` - Create databases
   - `get_database_schema()` - Retrieve schemas

2. **Research & Web** (`tools/research_tool.py`)
   - `search_web()` - Web search functionality
   - `analyze_content()` - Content analysis
   - `fetch_url_content()` - URL retrieval
   - `search_and_analyze()` - Combined search + analysis

3. **Update Generation** (`tools/update_tool.py`)
   - `generate_multi_format_update()` - Generate updates in multiple formats
   - `create_update_template()` - Create update templates
   - `validate_update_data()` - Validate update data

4. **Database Tools** (`tools/database_tool.py`)
   - `analyze_database()` - Analyze database structure and content
   - `enhance_database()` - Apply enhancements to databases
   - `export_database_structure()` - Export database schemas
   - `compare_databases()` - Compare two databases

---

## 🚀 Quick Navigation

### For Users:
- **Getting Started**: `README.md` → `QUICKSTART.md`
- **LinkedIn OS Guide**: `docs/guides/LINKEDIN_CONTENT_OS_GUIDE.md`
- **Update System**: `docs/guides/UPDATE_SYSTEM_README.md`

### For Developers:
- **API Rules**: `docs/agents/AGENTS.md`
- **API Migration**: `docs/guides/API_MIGRATION_2025-09-03.md`
- **Block Types**: `docs/guides/ALL_BLOCK_TYPES_SHOWCASE.md`

### For MCP Integration:
- **MCP Setup**: `docs/mcp/MCP_SERVER_README.md`
- **MCP Resources**: `docs/mcp/MCP_RESOURCES.md`
- **MCP Conversion**: `docs/mcp/MCP_CONVERSION_COMPLETE.md`

---

## 📝 Best Practices

### Adding New Files

**Documentation** → `/docs/[category]/`
```bash
# Add a new guide
mv my_new_guide.md docs/guides/
```

**Python Scripts** → `/scripts/[purpose]/`
```bash
# Add a new generator
mv my_generator.py scripts/generators/
```

**Data Exports** → `/data/`
```bash
# Save exports and reports
mv export_*.json data/
```

**Templates** → `/templates/`
```bash
# Add new templates
mv my_template.json templates/
```

### Importing from Other Directories

When importing from `scripts/`, adjust your Python imports:

```python
# If running from scripts/generators/
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from notion_api_client import NotionTemplateClient

# Or use relative imports
from ...notion_api_client import NotionTemplateClient
```

---

## 🔄 Git Workflow

Files to track:
- ✅ All Python scripts
- ✅ All documentation
- ✅ Templates
- ✅ README files

Files to ignore (already in `.gitignore`):
- ❌ `.env` (secrets)
- ❌ `venv/` (virtual environment)
- ❌ `__pycache__/` (Python cache)
- ❌ Generated data files in `/data/` (optional)

---

## 📊 Project Statistics

After reorganization:
- **Total Documentation Files**: 20+
- **Python Scripts**: 12
- **MCP Prompts**: 12
- **MCP Tools**: 15
- **Template Files**: 1+
- **Data Exports**: 2+

**Organization Benefits**:
- ✅ Clear separation of concerns
- ✅ Easy to find specific files
- ✅ Scalable structure for future additions
- ✅ Clean root directory
- ✅ Logical grouping by purpose

---

## 🎯 Maintenance

### Regular Updates
1. **Weekly**: Archive generated reports to `/data/`
2. **Monthly**: Review and consolidate session summaries
3. **Quarterly**: Update main documentation based on changes

### File Naming Conventions
- Documentation: `UPPERCASE_WITH_UNDERSCORES.md`
- Scripts: `lowercase_with_underscores.py`
- Data: `descriptive_name_YYYYMMDD_HHMMSS.json`
- Templates: `descriptive_name_template.json`

---

**Last Updated**: October 5, 2025
**Status**: ✅ Reorganized and Production Ready

