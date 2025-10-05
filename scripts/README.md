# 🐍 Scripts Directory

All Python scripts organized by purpose.

## 📁 Subdirectories

### `/generators`
Main Notion template generators:
- `main.py` - AI Product Manager OS (4 databases)
- `linkedin_content_os.py` - LinkedIn OS basic (3 databases)
- `linkedin_content_os_complete.py` - LinkedIn OS complete (12+ pages, 5 databases)

**Usage:**
```bash
# From project root
cd scripts/generators
source ../../venv/bin/activate  # Activate venv first
python linkedin_content_os_complete.py
```

### `/enhancements`
Database enhancement and population tools:
- `apply_enhancements.py` - Original enhancement script
- `apply_enhancements_fixed.py` - Fixed version (recommended)
- `notion_enhancer.py` - Advanced analyzer and enhancer

**Usage:**
```bash
cd scripts/enhancements
source ../../venv/bin/activate
python apply_enhancements_fixed.py
```

### `/utilities`
Helper scripts and tools:
- `test_retrieve_structure.py` - Database structure retrieval
- `export_all_linkedin_databases.py` - Export all databases
- `update_generator.py` - Multi-format update generator

**Usage:**
```bash
cd scripts/utilities
source ../../venv/bin/activate
python update_generator.py ../../templates/update_template.json
```

## 🔧 Prerequisites

All scripts require:
1. **Virtual environment activated**:
   ```bash
   source venv/bin/activate  # from project root
   ```

2. **Environment variables set** (`.env` file):
   ```bash
   NOTION_API_KEY=secret_xxxxx
   NOTION_PARENT_PAGE_ID=xxxxx
   ```

3. **Dependencies installed**:
   ```bash
   pip install -r requirements.txt
   ```

## 📝 Import Adjustments

Since scripts are now in subdirectories, adjust imports:

```python
# Method 1: Add parent directory to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from notion_api_client import NotionTemplateClient

# Method 2: Relative imports
from ...notion_api_client import NotionTemplateClient
```

## 🎯 Quick Reference

**Create LinkedIn OS:**
```bash
cd scripts/generators && python linkedin_content_os_complete.py
```

**Enhance existing database:**
```bash
cd scripts/enhancements && python apply_enhancements_fixed.py
```

**Generate weekly update:**
```bash
cd scripts/utilities && python update_generator.py ../../templates/update_template.json
```

**Export database structure:**
```bash
cd scripts/utilities && python export_all_linkedin_databases.py
```

---

See `../docs/agents/AGENTS.md` for detailed commands and workflows.
