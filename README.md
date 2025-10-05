# 🏛️ Notion Template Generator MCP - Enhanced LinkedIn Content OS

A comprehensive Model Context Protocol (MCP) server that provides AI assistants with powerful tools for Notion automation, content generation, and LinkedIn content management. Now featuring **wiki management**, **intelligent page reorganization**, and **interactive content enhancement**.

## 🚀 What's New - Major Enhancements

### ✨ Latest Features (October 2025)
- **🏛️ Wiki Management System** - Convert pages to wikis with proper structure and verification
- **🎨 Interactive Page Enhancement** - Add engaging elements, toggles, callouts, and resource links
- **🤖 Intelligent Page Reorganization** - AI-powered content analysis and workspace optimization
- **📊 Comprehensive Analytics** - Advanced performance tracking and KPI monitoring
- **🔗 Resource Integration** - Curated links to 20+ professional tools and platforms
- **✅ Quality Assurance** - Page verification system with ownership tracking

## 📊 System Overview

### 🛠️ **39 MCP Tools** Across 8 Categories
- **5 Wiki Management Tools** - Convert, verify, and manage wiki structures
- **6 Page Management Tools** - Comprehensive page operations with full property support
- **3 Content Analysis Tools** - AI-powered semantic analysis and extraction
- **3 Intelligent Reorganization Tools** - Smart workspace optimization
- **3 Workspace Cleanup Tools** - Automated maintenance and consistency
- **7 Database Management Tools** - Advanced database operations and analysis
- **6 Core Page Operations** - Essential page CRUD operations
- **6 Research & Content Tools** - Web research and multi-format content generation

### 📚 **12 Knowledge Prompts** for AI Assistance
- **4 System & Development Prompts** - Setup, migration, and architecture guidance
- **4 Reference & Documentation Prompts** - Complete guides and troubleshooting
- **4 LinkedIn & Content Prompts** - Specialized content creation and strategy guides

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [MCP Tools](#-mcp-tools)
- [Wiki Management](#-wiki-management)
- [Interactive Enhancements](#-interactive-enhancements)
- [LinkedIn Content OS](#-linkedin-content-os)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

### 🏛️ Wiki Management
- **Convert pages to wikis** with proper navigation structure
- **Page verification system** with expiration dates and ownership
- **Database views** for comprehensive page management
- **Content organization** with Getting Started, Knowledge Base, and Tools sections

### 🎨 Interactive Page Enhancement
- **Engaging visual elements** - colorful callouts, toggles, and progress trackers
- **Resource integration** - direct links to professional tools and platforms
- **Interactive workshops** - step-by-step guides and assessments
- **Performance dashboards** - KPI tracking and success metrics

### 🤖 Intelligent Reorganization
- **AI-powered content analysis** using semantic understanding
- **Automated page consolidation** with content preservation
- **Duplicate detection and removal** with smart merging
- **Professional workspace optimization** for business presentation

### 📊 Core Notion Tools
- **Database operations** - create, query, modify schemas
- **Page management** - create, update, move, duplicate, delete
- **Content extraction** - comprehensive block type support
- **File uploads** - handle media and documents
- **Advanced properties** - all Notion property types supported

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Notion API key
- Model Context Protocol compatible AI assistant (Claude, etc.)

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/notion-template-generator-mcp.git
cd notion-template-generator-mcp
```

2. **Install dependencies:**
```bash
pip install -r 02_Core_System/requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your Notion API key
```

4. **Set up MCP configuration:**
```bash
# Add to your MCP client configuration
{
  "mcpServers": {
    "notion-template-generator": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/notion-template-generator-mcp"
    }
  }
}
```

## ⚡ Quick Start

### 1. Create a Wiki from Existing Page
```python
# Using MCP tool
create_wiki_from_page(
    page_id="your-page-id",
    wiki_title="My Knowledge Base",
    description="Comprehensive resource hub"
)
```

### 2. Enhance Pages with Interactive Elements
```python
# The system automatically adds:
# - Interactive toggles and callouts
# - Resource links and tool recommendations
# - Progress tracking checklists
# - Professional visual elements
```

### 3. Intelligent Workspace Reorganization
```python
# Analyze and reorganize workspace
analyze_notion_workspace_cleanup(root_page_id="your-root-page")
execute_notion_workspace_cleanup(root_page_id="your-root-page", confirm_deletion=True)
```

## 🛠️ MCP Tools Reference

The Notion Template Generator MCP provides **39 comprehensive tools** organized into 8 categories:

### 🏛️ Wiki Management Tools (5 tools)
- **`create_wiki_from_page`** - Convert any page into a comprehensive wiki with navigation structure, database views, and content organization
- **`verify_page_with_ownership`** - Add verification status with ownership tracking, expiration dates, and quality assurance workflow
- **`remove_page_verification`** - Remove verification status from pages while maintaining ownership information
- **`convert_wiki_to_page`** - Undo wiki conversion and return to regular page format with content preservation
- **`get_workspace_verified_pages`** - Retrieve and manage all verified pages across the workspace with filtering options

### 📄 Comprehensive Page Management Tools (6 tools)
- **`create_notion_page_comprehensive`** - Create pages with full property support, parent relationships, and content blocks
- **`get_page_hierarchy_comprehensive`** - Retrieve complete page hierarchies with nested relationships and metadata
- **`extract_page_properties_comprehensive`** - Extract all property types (title, rich_text, select, date, people, etc.) with type safety
- **`update_page_property_comprehensive`** - Update any property type with validation and error handling
- **`move_page_comprehensive`** - Move pages between parents with relationship preservation
- **`analyze_page_structure_intelligent`** - AI-powered analysis of page structure and optimization recommendations

### 🔍 Content Extraction & Analysis Tools (3 tools)
- **`extract_full_page_content`** - Extract complete page content including all 25+ supported block types
- **`extract_complete_hierarchy`** - Get full page hierarchy with all content, properties, and relationships
- **`analyze_content_semantically`** - AI-powered semantic analysis using sentence transformers and NLP

### 🤖 Intelligent Reorganization Tools (3 tools)
- **`extract_pages_with_complete_content`** - Bulk extraction of pages with full content for analysis and reorganization
- **`create_intelligent_reorganization_plan`** - Generate AI-powered reorganization plans using semantic clustering
- **`execute_intelligent_reorganization`** - Execute reorganization plans with content preservation and duplicate handling

### 🧹 Workspace Cleanup Tools (3 tools)
- **`analyze_notion_workspace_cleanup`** - Analyze workspace for duplicates, inconsistencies, and optimization opportunities
- **`execute_notion_workspace_cleanup`** - Execute cleanup with content migration, duplicate removal, and structure optimization
- **`fix_notion_emoji_consistency`** - Fix emoji placement ensuring proper icon fields vs title consistency

### 🗄️ Database Management Tools (7 tools)
- **`query_notion_database`** - Advanced database queries with filtering, sorting, and property selection
- **`create_notion_database`** - Create databases with comprehensive property schemas and configurations
- **`get_database_schema`** - Retrieve complete database schemas with property definitions and relationships
- **`modify_database_schema`** - Update database properties, add/remove columns, and modify configurations
- **`analyze_database`** - Analyze database structure, usage patterns, and optimization opportunities
- **`enhance_database`** - Add advanced properties, views, and automation to existing databases
- **`export_database_structure`** - Export database schemas for backup, migration, or documentation
- **`compare_databases`** - Compare database structures and identify differences or inconsistencies

### 📝 Core Page Operations (6 tools)
- **`update_notion_page`** - Update page content, properties, and metadata with comprehensive block support
- **`move_notion_page`** - Move pages between parents with relationship and content preservation
- **`duplicate_notion_page`** - Clone pages with all content, properties, and nested relationships
- **`delete_notion_page`** - Safely delete pages with confirmation and recovery options
- **`restore_notion_page`** - Restore deleted pages from trash with content recovery
- **`upload_file_to_notion`** - Handle file uploads including images, documents, and media with proper embedding

### 🔬 Research & Content Tools (6 tools)
- **`search_web`** - Perform web research with multiple search engines and content extraction
- **`analyze_content`** - Analyze web content, documents, and text for insights and summarization
- **`generate_multi_format_update`** - Generate updates in multiple formats (Slack, LinkedIn, Blog, Document)
- **`create_update_template`** - Create reusable templates for consistent update formatting
- **`validate_update_data`** - Validate update content for completeness, accuracy, and formatting

## 📚 MCP Prompts Reference

The system provides **12 comprehensive knowledge prompts** covering all aspects of Notion automation:

### 🤖 System & Development Prompts
- **`agents_guide`** - AI Assistant Rules & Commands for the Notion Template Generator project
- **`api_migration_guide`** - Notion API 2025-09-03 Migration Guide with data sources architecture
- **`system_guide`** - Complete system guide covering all features, workflows, and best practices
- **`project_overview`** - High-level project overview, architecture, and feature capabilities

### 📖 Reference & Documentation Prompts  
- **`block_types_reference`** - Complete reference of all 25+ Notion block types with examples and usage
- **`quickstart`** - Quick start guide for rapid setup and immediate productivity
- **`content_creation_guide`** - Guidelines for creating engaging Notion content with rich elements
- **`success_stories`** - Implementation examples, case studies, and proven success patterns

### 🎯 LinkedIn & Content Prompts
- **`linkedin_content_os_guide`** - Complete LinkedIn Content OS guide (12 pages, 5 databases, 300+ blocks)
- **`update_system_guide`** - Multi-format update generation system for various platforms
- **`session_summary`** - Detailed development session summaries and progress tracking
- **`weekly_update_example`** - High-quality weekly update templates and examples

### 🔧 Prompt Usage
All prompts are accessible through the MCP protocol and provide:
- **Contextual knowledge** for AI assistants
- **Step-by-step workflows** for complex operations  
- **Best practices** and optimization techniques
- **Troubleshooting guides** for common issues
- **Code examples** and implementation patterns

## 💡 Tool Usage Examples

### Wiki Management Examples
```python
# Create a comprehensive wiki
result = create_wiki_from_page(
    page_id="2830da0aa5c8807e9b5cf5c9411b445f",
    wiki_title="Team Knowledge Base",
    description="Central hub for all team resources and documentation"
)

# Verify critical pages with ownership
verify_page_with_ownership(
    page_id="page-id",
    owner_ids=["user-1", "user-2"],
    expires_in_days=90  # Review every 3 months
)

# Get all verified pages for audit
verified_pages = get_workspace_verified_pages()
```

### Content Analysis Examples
```python
# Extract complete page content for analysis
content = extract_full_page_content(page_id="your-page-id")

# Analyze content semantically for insights
analysis = analyze_content_semantically(
    page_id="your-page-id",
    analysis_type="comprehensive"
)

# Get complete hierarchy with all content
hierarchy = extract_complete_hierarchy(root_page_id="root-id")
```

### Workspace Optimization Examples
```python
# Analyze workspace for cleanup opportunities
analysis = analyze_notion_workspace_cleanup(root_page_id="workspace-root")

# Execute comprehensive cleanup
cleanup_result = execute_notion_workspace_cleanup(
    root_page_id="workspace-root",
    confirm_deletion=True
)

# Fix emoji consistency across workspace
fix_notion_emoji_consistency(root_page_id="workspace-root")
```

### Database Management Examples
```python
# Create advanced database with multiple property types
db_result = create_notion_database(
    parent_id="parent-page-id",
    title="Project Tracker",
    properties={
        "Name": {"type": "title"},
        "Status": {"type": "select", "options": ["Not Started", "In Progress", "Complete"]},
        "Due Date": {"type": "date"},
        "Assignee": {"type": "people"},
        "Priority": {"type": "select", "options": ["Low", "Medium", "High"]}
    }
)

# Query database with advanced filtering
results = query_notion_database(
    database_id="db-id",
    filter_conditions={
        "Status": {"select": {"equals": "In Progress"}},
        "Priority": {"select": {"equals": "High"}}
    },
    sorts=[{"property": "Due Date", "direction": "ascending"}]
)

# Analyze database for optimization
db_analysis = analyze_database(database_id="your-db-id")
```

### Page Management Examples
```python
# Create comprehensive page with properties and content
page = create_notion_page_comprehensive(
    parent_id="parent-id",
    title="Project Overview",
    properties={
        "Status": {"type": "select", "value": "Draft"},
        "Created": {"type": "date", "value": "2025-10-05"}
    },
    content_blocks=[
        {
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "Project Goals"}}]}
        },
        {
            "type": "paragraph", 
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Define project objectives..."}}]}
        }
    ]
)

# Move page with relationship preservation
move_result = move_page_comprehensive(
    page_id="page-to-move",
    new_parent_id="new-parent-id"
)

# Duplicate page with all content and properties
duplicate = duplicate_notion_page(
    page_id="source-page-id",
    new_title="Copy of Original Page"
)
```

## 🏛️ Wiki Management

### Creating a Wiki
Transform any Notion page into a comprehensive wiki:

```python
result = create_wiki_from_page(
    page_id="2830da0aa5c8807e9b5cf5c9411b445f",
    wiki_title="LinkedIn Content OS Wiki",
    description="Complete LinkedIn content strategy resource"
)
```

**Features Added:**
- 🏠 **Home view** with organized navigation
- 📄 **All Pages database** for complete management
- 👤 **Pages I Own database** for ownership tracking
- 🏷️ **Content categorization** system
- ✅ **Verification workflow** for quality assurance

### Page Verification
Ensure content quality with verification system:

```python
verify_page_with_ownership(
    page_id="page-id",
    owner_ids=["user-id-1", "user-id-2"],
    expires_in_days=90,  # or indefinite=True
)
```

## 🎨 Interactive Enhancements

### Automatic Enhancements
The system automatically adds engaging elements to pages:

#### 🎯 Brand Strategy Pages
- Interactive brand personality assessments
- Progress tracking checklists
- Resource links to LinkedIn Creator Hub
- Brand canvas workshops

#### 📝 Content Creation Pages
- Content type explorers with templates
- Tool recommendations (Canva, Grammarly, etc.)
- 50+ proven post templates
- Video content strategies

#### 📅 Scheduling Pages
- Optimal posting time calculators
- Platform comparison guides
- 30-day content calendar templates
- Automation workflow builders

#### 📊 Analytics Pages
- KPI tracking dashboards
- Professional tool directories
- Performance benchmarks
- Success metrics monitoring

## 📱 LinkedIn Content OS

### Complete System Included
The enhanced LinkedIn Content OS provides:

#### 🎯 **Brand Strategy & Discovery**
- Interactive brand workshops
- Target audience analysis
- Value proposition development
- Visual brand identity guides

#### 📝 **Content Planning & Creation**
- Content idea generators
- Template libraries
- Visual design resources
- Writing optimization tools

#### 📅 **Content Calendar & Scheduling**
- Smart scheduling systems
- Platform integration guides
- Timing optimization
- Batch content creation

#### 📈 **Performance & Analytics**
- Comprehensive KPI tracking
- Analytics tool comparisons
- ROI measurement systems
- Growth optimization strategies

#### 🤖 **Automation & Systems**
- Workflow automation guides
- Tool integration setups
- Efficiency optimization
- Scale management systems

### Professional Benefits
- ✅ **Sale-ready presentation** for clients and stakeholders
- 📚 **Comprehensive knowledge base** with searchable content
- 🎯 **Actionable guidance** with step-by-step workflows
- 🔗 **Curated resources** worth thousands in consulting value
- 📊 **Performance tracking** for measurable ROI
- 🤖 **Scalable systems** for growth management

## ⚙️ Configuration

### Environment Variables
```bash
# Required
NOTION_API_KEY=your_notion_api_key_here

# Optional (for enhanced features)
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

### MCP Server Configuration
```json
{
  "mcpServers": {
    "notion-template-generator": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/notion-template-generator-mcp",
      "env": {
        "NOTION_API_KEY": "your_key_here"
      }
    }
  }
}
```

## 🔧 Development

### Project Structure
```
notion-template-generator-mcp/
├── mcp_server.py                 # Main MCP server
├── 02_Core_System/              # Core functionality
│   ├── tools/                   # MCP tools
│   │   ├── wiki_management_tool.py
│   │   ├── content_extraction_tool.py
│   │   ├── working_reorganization_tool.py
│   │   └── cleanup_tool.py
│   └── scripts/                 # Utility scripts
├── 03_Templates/               # Notion templates
├── 04_Documentation/           # Guides and references
└── 06_Support/                # Support resources
```

### Adding New Tools
1. Create tool function in appropriate module
2. Add MCP decorator in `mcp_server.py`
3. Update `tools/__init__.py`
4. Test with MCP client

## 🐛 Troubleshooting

### Common Issues

#### MCP Server Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Verify dependencies
pip install -r 02_Core_System/requirements.txt

# Test server directly
python mcp_server.py
```

#### Notion API Errors
```bash
# Verify API key
echo $NOTION_API_KEY

# Check permissions
# Ensure integration has access to target pages/databases
```

#### Wiki Creation Fails
- Ensure page exists and integration has access
- Check that page isn't already a database
- Verify sufficient permissions for child page creation

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Optimization Features
- **Intelligent caching** for repeated API calls
- **Batch operations** for bulk updates
- **Rate limiting** compliance with Notion API
- **Error handling** with automatic retries

### Scalability
- Handles workspaces with 1000+ pages
- Efficient content analysis algorithms
- Optimized database operations
- Memory-efficient processing

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install development dependencies
4. Run tests before committing

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive docstrings
- Write tests for new features

### Submitting Changes
1. Ensure all tests pass
2. Update documentation
3. Create detailed pull request
4. Include example usage

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Notion API Team** - For the powerful platform
- **MCP Community** - For the protocol specification
- **Contributors** - For ongoing improvements and feedback

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/yourusername/notion-template-generator-mcp/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/notion-template-generator-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/notion-template-generator-mcp/discussions)

---

**🚀 Transform your Notion workspace into an interactive, professional knowledge management system with the enhanced Notion Template Generator MCP!**
