# AGENTS.MD - AI Assistant Rules & Commands

This file establishes the rules, commands, and context for AI assistants working on the Notion Template Generator project.

---

## 🎯 Project Overview

**Project Name**: Notion Template Generator  
**Purpose**: Programmatically create comprehensive Notion systems via the Notion API  
**API Version**: 2025-09-03 (Latest)  
**Language**: Python 3.8+  
**Key Framework**: notion-client SDK

### What This Project Creates

1. **AI Product Manager OS** - 4 databases for product management workflows
2. **LinkedIn Content OS** - Complete product bundle with 12 pages, 5 databases, 300+ blocks

---

## 🔐 Critical Rules for AI Agents

### 1. API Version Requirements

```python
# ✅ ALWAYS use this API version
API_VERSION = "2025-09-03"

# ✅ Initialize client with version
client = Client(auth=api_key, notion_version="2025-09-03")
```

**Why**: The 2025-09-03 version introduces data sources, which are NOT backwards compatible.

### 2. Data Source ID Pattern (MANDATORY)

```python
# ❌ OLD WAY (pre-2025-09-03) - DO NOT USE
page_data = {
    "parent": {"database_id": database_id}
}

# ✅ NEW WAY (2025-09-03+) - ALWAYS USE THIS
# Step 1: Get data_source_id from database
database = client.get_database(database_id)
data_source_id = database["data_sources"][0]["id"]

# Step 2: Use data_source_id as parent
page_data = {
    "parent": {"type": "data_source_id", "data_source_id": data_source_id}
}
```

### 3. Database Creation Pattern

```python
# ✅ CORRECT: Use initial_data_source wrapper
response = client.databases.create(
    parent={"type": "page_id", "page_id": parent_id},
    title=[{"type": "text", "text": {"content": "My Database"}}],
    initial_data_source={
        "properties": {
            "Name": {"title": {}},
            "Status": {"select": {"options": [...]}}
        }
    }
)
```

### 4. File Naming Convention

```
✅ notion_api_client.py    (NOT notion_client.py - conflicts with package)
✅ main.py                 (AI PM OS generator)
✅ linkedin_content_os_complete.py  (Full LinkedIn system)
```

### 5. Block Helper Functions

**ALWAYS** use the helper functions from `notion_api_client.py`:

```python
from notion_api_client import (
    heading_1, heading_2, heading_3,    # Headings
    paragraph,                           # Paragraphs
    bullet_list_item, numbered_list_item,  # Lists
    to_do,                              # Checkboxes
    toggle,                             # Collapsible sections
    callout,                            # Highlighted boxes
    quote,                              # Quotes
    code,                               # Code blocks
    table_of_contents,                  # Auto TOC
    divider,                            # Separators
    bookmark                            # Link previews
)
```

### 6. Never Commit Secrets

```bash
# ❌ NEVER commit these files
.env
venv/
__pycache__/
*.pyc

# ✅ .gitignore is properly configured
```

---

## 📋 Available Commands

### Setup & Installation

```bash
# Quick setup (recommended)
cd "/Users/tatiana/Cloning me/notion_template_generator"
./setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with NOTION_API_KEY and NOTION_PARENT_PAGE_ID
```

### Generate Templates

```bash
# Activate environment first
source venv/bin/activate

# Create LinkedIn Content OS (recommended)
python linkedin_content_os_complete.py

# Create AI Product Manager OS
python main.py

# Create LinkedIn basic (3 databases only)
python linkedin_content_os.py
```

### Development Commands

```bash
# Check Python version
python --version  # Must be 3.8+

# View installed packages
pip list

# Update dependencies
pip install --upgrade -r requirements.txt

# Test connection (Python REPL)
python
>>> from notion_api_client import NotionTemplateClient
>>> client = NotionTemplateClient()
>>> # Should initialize without errors
```

---

## 🏗️ Project Architecture

### File Structure

```
notion_template_generator/
├── notion_api_client.py           # Core API wrapper (UPDATE THIS FOR API CHANGES)
├── main.py                        # AI PM OS (4 databases)
├── linkedin_content_os.py         # LinkedIn basic (3 databases)
├── linkedin_content_os_complete.py # LinkedIn full (12 pages) ⭐
├── templates/*.json               # Schema definitions
├── requirements.txt               # Dependencies
├── setup.sh                       # Automated setup
├── .env                          # Secrets (never commit!)
├── .gitignore                    # Git ignore rules
└── *.md                          # Documentation
```

### Key Classes & Methods

#### `NotionTemplateClient` (notion_api_client.py)

**Core Methods:**
- `create_database(title, properties, icon, cover)` - Create database with data source
- `get_database(database_id)` - Get database with data_sources array
- `get_data_source_id(database_id, index=0)` - Helper to extract data source ID
- `retrieve_data_source(data_source_id)` - Get data source schema
- `create_page_in_database(database_id, properties, children, data_source_id)` - Create page/row
- `query_database(database_id, filter_conditions, data_source_id)` - Query data source
- `update_data_source(data_source_id, properties, title)` - Update schema
- `append_blocks(block_id, children)` - Add content to pages

#### Block Helper Functions (notion_api_client.py)

All return `Dict[str, Any]` - ready to use in `children` arrays:

```python
heading_1(text, color="default", is_toggleable=False)
heading_2(text, color="default", is_toggleable=False)
heading_3(text, color="default", is_toggleable=False)
paragraph(text, color="default")
bullet_list_item(text, color="default")
numbered_list_item(text, color="default")
to_do(text, checked=False, color="default")
toggle(text, color="default")
callout(text, icon="💡", color="default")
quote(text, color="default")
code(code_text, language="python")
table_of_contents(color="default")
divider()
bookmark(url, caption="")
```

**Supported Colors:**
`"default"`, `"gray"`, `"brown"`, `"orange"`, `"yellow"`, `"green"`, `"blue"`, `"purple"`, `"pink"`, `"red"`, and `"_background"` variants (e.g., `"blue_background"`)

---

## 🔄 Common Workflows

### 1. Creating a New Database

```python
from notion_api_client import NotionTemplateClient

client = NotionTemplateClient()

# Define schema
properties = {
    "Name": {"title": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Not Started", "color": "gray"},
                {"name": "In Progress", "color": "blue"},
                {"name": "Complete", "color": "green"}
            ]
        }
    },
    "Priority": {
        "select": {
            "options": [
                {"name": "Low", "color": "gray"},
                {"name": "Medium", "color": "yellow"},
                {"name": "High", "color": "red"}
            ]
        }
    },
    "Due Date": {"date": {}},
    "Tags": {
        "multi_select": {
            "options": [
                {"name": "Urgent", "color": "red"},
                {"name": "Important", "color": "blue"}
            ]
        }
    }
}

# Create database
response = client.create_database(
    title="Task Tracker",
    properties=properties,
    icon={"emoji": "✅"}
)

# Extract IDs for later use
database_id = response["id"]
data_source_id = response["data_sources"][0]["id"]
```

### 2. Adding Pages with Rich Content

```python
from notion_api_client import (
    NotionTemplateClient,
    heading_1, heading_2, paragraph, callout,
    bullet_list_item, to_do, code, divider
)

client = NotionTemplateClient()

# Define page properties
properties = {
    "Name": {
        "title": [{"text": {"content": "Implement User Authentication"}}]
    },
    "Status": {"select": {"name": "In Progress"}},
    "Priority": {"select": {"name": "High"}},
    "Due Date": {"date": {"start": "2025-10-15"}},
    "Tags": {
        "multi_select": [
            {"name": "Urgent"},
            {"name": "Important"}
        ]
    }
}

# Define rich content
children = [
    heading_1("🎯 Overview"),
    paragraph("Implement secure user authentication with JWT tokens."),
    
    divider(),
    
    heading_2("✅ Tasks"),
    to_do("Set up authentication routes", checked=True),
    to_do("Implement JWT token generation", checked=True),
    to_do("Add password hashing", checked=False),
    to_do("Create login/logout endpoints", checked=False),
    
    divider(),
    
    heading_2("📋 Technical Details"),
    callout("Remember to use environment variables for secrets!", "🔐", "yellow_background"),
    
    heading_3("Dependencies"),
    bullet_list_item("bcrypt for password hashing"),
    bullet_list_item("jsonwebtoken for JWT"),
    bullet_list_item("express-session for sessions"),
    
    heading_3("Code Example"),
    code('''
const jwt = require('jsonwebtoken');

function generateToken(user) {
    return jwt.sign(
        { id: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: '24h' }
    );
}
''', "javascript")
]

# Create page
page = client.create_page_in_database(
    database_id=database_id,
    properties=properties,
    children=children
)
```

### 3. Querying a Database

```python
# Get all high-priority tasks
results = client.query_database(
    database_id=database_id,
    filter_conditions={
        "property": "Priority",
        "select": {
            "equals": "High"
        }
    }
)

print(f"Found {len(results)} high-priority tasks")
```

### 4. Updating a Data Source Schema

```python
# Add a new property to the data source
data_source_id = client.get_data_source_id(database_id)

updated_schema = {
    "Assignee": {
        "people": {}
    }
}

client.update_data_source(
    data_source_id=data_source_id,
    properties=updated_schema
)
```

---

## 🚨 Error Handling

### Common Errors & Solutions

#### 1. `APIResponseError: body failed validation`

**Cause**: Using old API patterns with 2025-09-03 version

**Solution**: 
```python
# ❌ Wrong
parent = {"database_id": db_id}

# ✅ Correct
data_source_id = client.get_data_source_id(db_id)
parent = {"type": "data_source_id", "data_source_id": data_source_id}
```

#### 2. `ImportError: cannot import name 'Client' from partially initialized module`

**Cause**: Filename conflict with installed package

**Solution**: Ensure your file is named `notion_api_client.py` (NOT `notion_client.py`)

#### 3. `ValueError: Notion API key not found`

**Cause**: `.env` file not configured

**Solution**:
```bash
# Create .env file
cp .env.example .env

# Add credentials
echo "NOTION_API_KEY=secret_your_key_here" >> .env
echo "NOTION_PARENT_PAGE_ID=your-page-id-here" >> .env
```

#### 4. `No data sources found for database`

**Cause**: Database created with old API version

**Solution**: Database must be created with 2025-09-03 API to have data_sources

---

## 🎨 Best Practices for AI Agents

### 1. Always Read Before Write

```python
# ✅ Good practice
database = client.get_database(database_id)
data_sources = database["data_sources"]
print(f"Found {len(data_sources)} data source(s)")

# Then proceed with operations
```

### 2. Use Helper Functions

```python
# ❌ Don't manually construct blocks
block = {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Hello"}}]
    }
}

# ✅ Use helpers
block = paragraph("Hello")
```

### 3. Validate IDs

```python
# ✅ Validate before using
def validate_uuid(id_string):
    import re
    pattern = r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$'
    return bool(re.match(pattern, id_string.replace('-', '')))

if not validate_uuid(database_id):
    raise ValueError(f"Invalid database ID: {database_id}")
```

### 4. Log Progress

```python
# ✅ Use informative logging
print(f"🔍 Retrieving database: {database_id}")
print(f"📊 Found {len(data_sources)} data source(s)")
print(f"✅ Created page: {page_title}")
print(f"❌ Error: {error_message}")
```

### 5. Handle Rate Limits

```python
import time
from notion_client.errors import APIResponseError

def create_with_retry(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except APIResponseError as e:
            if e.code == "rate_limited" and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⏳ Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

## 📚 Quick Reference

### Property Types

| Type | Usage | Example |
|------|-------|---------|
| `title` | Page title (required) | `{"title": {}}` |
| `rich_text` | Multi-line text | `{"rich_text": {}}` |
| `number` | Numbers | `{"number": {"format": "dollar"}}` |
| `select` | Single choice | `{"select": {"options": [...]}}` |
| `multi_select` | Multiple choices | `{"multi_select": {"options": [...]}}` |
| `date` | Date or date range | `{"date": {}}` |
| `people` | User references | `{"people": {}}` |
| `checkbox` | Boolean | `{"checkbox": {}}` |
| `url` | URLs | `{"url": {}}` |
| `email` | Email addresses | `{"email": {}}` |
| `phone_number` | Phone numbers | `{"phone_number": {}}` |
| `relation` | Links to other database | `{"relation": {"data_source_id": "..."}}` |
| `created_time` | Auto timestamp | `{"created_time": {}}` |
| `last_edited_time` | Auto timestamp | `{"last_edited_time": {}}` |

### Color Options

All block types support these colors:
- Basic: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`
- Backgrounds: `gray_background`, `brown_background`, etc.

### Code Languages

Common languages for `code()` blocks:
`python`, `javascript`, `typescript`, `java`, `c`, `cpp`, `csharp`, `php`, `ruby`, `go`, `rust`, `sql`, `html`, `css`, `json`, `yaml`, `markdown`, `bash`, `shell`

---

## 🔗 External Resources

- [Notion API Reference](https://developers.notion.com/)
- [2025-09-03 Upgrade Guide](https://developers.notion.com/docs/upgrade-guide-2025-09-03)
- [notion-client Python SDK](https://github.com/ramnes/notion-sdk-py)
- [Block Type Reference](https://developers.notion.com/reference/block)
- [Database Properties](https://developers.notion.com/reference/property-object)

---

## 🎯 Agent Instructions Summary

When working on this project, AI agents must:

1. ✅ **Always use API version 2025-09-03**
2. ✅ **Always get data_source_id before creating pages**
3. ✅ **Use helper functions for blocks**
4. ✅ **Never commit .env or secrets**
5. ✅ **Validate IDs before use**
6. ✅ **Log progress with emoji indicators**
7. ✅ **Handle errors gracefully**
8. ✅ **Follow the established patterns in existing code**
9. ✅ **Document new functions thoroughly**
10. ✅ **Test with small examples first**

---

## 📝 Version History

- **v1.0.0** (2025-10-05): Initial AGENTS.md creation
  - Upgraded to Notion API 2025-09-03
  - Added data source support
  - Documented all patterns and workflows

---

**Last Updated**: October 5, 2025  
**Maintained By**: AI Assistant Team  
**Project Status**: Production Ready ✅
