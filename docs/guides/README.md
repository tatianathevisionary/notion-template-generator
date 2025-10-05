# 📖 Guides Directory

Comprehensive guides for using the Notion Template Generator.

## 📑 Available Guides

### Core Guides

#### [COMPLETE_BLOCK_TYPES_REFERENCE.md](./COMPLETE_BLOCK_TYPES_REFERENCE.md)
**Complete Notion Block Types Reference**
- ✅ **Newly Added** - Comprehensive guide to all 30+ Notion block types
- Text blocks (headings, paragraphs, quotes, callouts)
- List blocks (bullets, numbers, to-dos, toggles)
- Media blocks (images, videos, audio, PDFs, files)
- Advanced blocks (tables, equations, synced blocks, columns)
- Complete code examples for every block type
- Based on official Notion API documentation

#### [API_MIGRATION_2025-09-03.md](./API_MIGRATION_2025-09-03.md)
**Notion API Version 2025-09-03 Migration Guide**
- New multi-source database model
- `data_source_id` concept and usage
- Breaking changes from previous versions
- Migration patterns and examples

#### [ALL_BLOCK_TYPES_SHOWCASE.md](./ALL_BLOCK_TYPES_SHOWCASE.md)
**Block Types Showcase**
- Visual examples of all supported block types
- Real-world usage patterns
- Styling and customization options

#### [COMPLETE_SYSTEM_GUIDE.md](./COMPLETE_SYSTEM_GUIDE.md)
**Complete System Implementation Guide**
- End-to-end system architecture
- Database creation workflows
- Page generation patterns
- Error handling and debugging

#### [CONTENT_GUIDE.md](./CONTENT_GUIDE.md)
**Content Creation Guide**
- Content strategy and planning
- Template design patterns
- Best practices for Notion workspaces

#### [LINKEDIN_CONTENT_OS_GUIDE.md](./LINKEDIN_CONTENT_OS_GUIDE.md)
**LinkedIn Content Operating System Guide**
- Complete LinkedIn Content OS setup
- Database schemas for content management
- Workflow automation tips

#### [UPDATE_SYSTEM_README.md](./UPDATE_SYSTEM_README.md)
**Multi-Format Update Generation System**
- Generate updates in 4 formats: Document, Slack, LinkedIn, Blog
- Template-based update creation
- Best practices for each format

---

## 🎯 Quick Navigation

### By Use Case

**Setting up a new project:**
1. [API_MIGRATION_2025-09-03.md](./API_MIGRATION_2025-09-03.md) - Understand the latest API
2. [COMPLETE_BLOCK_TYPES_REFERENCE.md](./COMPLETE_BLOCK_TYPES_REFERENCE.md) - Learn all available blocks
3. [COMPLETE_SYSTEM_GUIDE.md](./COMPLETE_SYSTEM_GUIDE.md) - Implement the full system

**Creating rich content:**
1. [COMPLETE_BLOCK_TYPES_REFERENCE.md](./COMPLETE_BLOCK_TYPES_REFERENCE.md) - All block types with examples
2. [ALL_BLOCK_TYPES_SHOWCASE.md](./ALL_BLOCK_TYPES_SHOWCASE.md) - Visual examples
3. [CONTENT_GUIDE.md](./CONTENT_GUIDE.md) - Content strategy

**Building for LinkedIn:**
1. [LINKEDIN_CONTENT_OS_GUIDE.md](./LINKEDIN_CONTENT_OS_GUIDE.md) - Complete LinkedIn setup
2. [UPDATE_SYSTEM_README.md](./UPDATE_SYSTEM_README.md) - Generate LinkedIn posts

---

## 🔧 Block Types Reference

The **COMPLETE_BLOCK_TYPES_REFERENCE.md** includes all Notion block types:

### Text Blocks (7 types)
- Headings (1, 2, 3) with toggle support
- Paragraph, Quote, Callout, Code

### List Blocks (4 types)
- Bulleted list, Numbered list, To-do, Toggle

### Media Blocks (6 types)
- Image, Video, Audio, PDF, File, Embed

### Advanced Blocks (5 types)
- Table & Table Row
- Equation (LaTeX/KaTeX)
- Synced Block
- Column List & Column

### Special Blocks (4 types)
- Divider, Breadcrumb, Bookmark, Table of Contents

---

## 📚 Additional Resources

### Code Examples

Each guide includes working code examples. Here's a quick sampler:

```python
# Import all block helpers
from notion_api_client import (
    heading_1, paragraph, bullet_list_item,
    image, video, table, callout, code
)

# Create rich content
blocks = [
    heading_1("My Page Title"),
    paragraph("Introduction text..."),
    callout("Important note!", icon="💡", color="blue_background"),
    bullet_list_item("First point"),
    bullet_list_item("Second point"),
    image("https://example.com/photo.jpg", caption="Beautiful view"),
    code("print('Hello, World!')", language="python")
]

# Append to page
client.append_blocks(page_id, blocks)
```

### API Reference

All guides are based on:
- **Notion API Version:** 2025-09-03
- **Official Docs:** https://developers.notion.com
- **SDK:** notion-client 2.2.1

---

## 💡 Tips for Using These Guides

1. **Start with the Block Types Reference** - It's the most comprehensive and includes all capabilities
2. **Use the search feature** - All guides are searchable via `Cmd/Ctrl + F`
3. **Copy code examples** - All examples are tested and ready to use
4. **Check API version** - Ensure you're using API version 2025-09-03
5. **Refer to official docs** - For the absolute latest changes

---

## 🆕 What's New

### October 5, 2025
- ✅ Added **COMPLETE_BLOCK_TYPES_REFERENCE.md** with all 30+ block types
- ✅ Extended `notion_api_client.py` with 14 new block helper functions
- ✅ Added support for: image, video, audio, pdf, file, embed, table, column, equation, synced_block, breadcrumb
- ✅ Complete API parity with Notion API 2025-09-03

---

## 🤝 Contributing

Found an issue or want to improve a guide?
1. Note the specific guide and section
2. Suggest improvements with code examples
3. Ensure examples follow API version 2025-09-03

---

**Last Updated:** October 5, 2025  
**Project Version:** 1.1.0  
**Status:** 📚 Complete & Current
