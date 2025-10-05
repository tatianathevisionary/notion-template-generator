# Complete Notion Block Types Reference

This guide provides a comprehensive reference for all Notion block types supported by the `notion_api_client.py` module, based on the official Notion API documentation.

## Table of Contents

1. [Text Blocks](#text-blocks)
2. [List Blocks](#list-blocks)
3. [Media Blocks](#media-blocks)
4. [Embed Blocks](#embed-blocks)
5. [Advanced Blocks](#advanced-blocks)
6. [Container Blocks](#container-blocks)
7. [Special Blocks](#special-blocks)

---

## Text Blocks

### Headings

Three levels of headings with optional color and toggle functionality.

```python
from notion_api_client import heading_1, heading_2, heading_3

# Basic headings
h1 = heading_1("Main Title")
h2 = heading_2("Section Title", color="blue")
h3 = heading_3("Subsection", color="gray_background")

# Toggleable headings (can contain child blocks)
toggle_h1 = heading_1("Collapsible Section", is_toggleable=True)
toggle_h2 = heading_2("Details", is_toggleable=True)
```

**Supported Colors:**
- `"default"`, `"gray"`, `"brown"`, `"orange"`, `"yellow"`, `"green"`, `"blue"`, `"purple"`, `"pink"`, `"red"`
- Background variants: `"gray_background"`, `"brown_background"`, etc.

### Paragraph

Basic text block with optional styling.

```python
from notion_api_client import paragraph

p = paragraph("This is a paragraph with some text.")
p_colored = paragraph("Highlighted text", color="yellow_background")
```

### Quote

Styled quote block for emphasizing text.

```python
from notion_api_client import quote

q = quote("To be or not to be, that is the question.")
q_colored = quote("Important note", color="blue_background")
```

### Callout

Attention-grabbing block with emoji icon.

```python
from notion_api_client import callout

info = callout("Important information", icon="💡")
warning = callout("Be careful!", icon="⚠️", color="red_background")
tip = callout("Pro tip", icon="✨", color="green_background")
```

### Code

Code block with syntax highlighting.

```python
from notion_api_client import code

python_code = code("def hello():\n    print('Hello, World!')", language="python")
js_code = code("const x = 10;", language="javascript")
```

**Supported Languages:**
- `"python"`, `"javascript"`, `"typescript"`, `"java"`, `"c"`, `"c++"`, `"c#"`, `"go"`, `"rust"`
- `"php"`, `"ruby"`, `"swift"`, `"kotlin"`, `"scala"`, `"r"`, `"sql"`, `"shell"`, `"bash"`
- `"html"`, `"css"`, `"json"`, `"yaml"`, `"xml"`, `"markdown"`
- And many more (see full list in API docs)

---

## List Blocks

### Bulleted List Item

```python
from notion_api_client import bullet_list_item

item1 = bullet_list_item("First bullet point")
item2 = bullet_list_item("Second bullet point", color="blue")
```

### Numbered List Item

```python
from notion_api_client import numbered_list_item

item1 = numbered_list_item("First numbered item")
item2 = numbered_list_item("Second numbered item")
```

### To-Do (Checkbox)

```python
from notion_api_client import to_do

todo1 = to_do("Incomplete task", checked=False)
todo2 = to_do("Completed task", checked=True, color="green")
```

### Toggle

Collapsible block that can contain child blocks.

```python
from notion_api_client import toggle

t = toggle("Click to expand", color="default")
```

---

## Media Blocks

### Image

Embed images from external URLs or file uploads.

```python
from notion_api_client import image

# External image
img1 = image("https://example.com/image.png", caption="Beautiful landscape")

# File upload (after uploading via File Upload API)
img2 = image(file_upload_id, caption="Uploaded image", is_external=False)
```

**Supported Formats:**
- `.bmp`, `.gif`, `.heic`, `.jpeg`, `.jpg`, `.png`, `.svg`, `.tif`, `.tiff`

### Video

Embed videos from URLs or file uploads.

```python
from notion_api_client import video

# External video
vid1 = video("https://example.com/video.mp4", caption="Tutorial video")

# YouTube video
vid2 = video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# File upload
vid3 = video(file_upload_id, caption="Uploaded video", is_external=False)
```

**Supported Formats:**
- `.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`
- YouTube URLs (embed or watch format)

### Audio

Embed audio files.

```python
from notion_api_client import audio

# External audio
aud1 = audio("https://example.com/podcast.mp3", caption="Episode 42")

# File upload
aud2 = audio(file_upload_id, caption="Voice memo", is_external=False)
```

**Supported Formats:**
- `.mp3`, `.wav`, `.ogg`, `.oga`, `.m4a`

### PDF

Embed PDF documents.

```python
from notion_api_client import pdf

# External PDF
doc1 = pdf("https://example.com/document.pdf", caption="Project specification")

# File upload
doc2 = pdf(file_upload_id, caption="Contract", is_external=False)
```

### File

Generic file attachment.

```python
from notion_api_client import file

# External file
f1 = file(
    "https://example.com/data.csv",
    name="Sales Data Q4",
    caption="Latest export"
)

# File upload
f2 = file(
    file_upload_id,
    name="Report.docx",
    caption="Final draft",
    is_external=False
)
```

---

## Embed Blocks

### Bookmark

Create a visual bookmark link.

```python
from notion_api_client import bookmark

bm = bookmark("https://notion.so", caption="Notion Homepage")
```

### Embed

Embed external content (iFrame).

```python
from notion_api_client import embed

# Embed a website
emb1 = embed("https://example.com")

# Embed Figma, Miro, etc.
emb2 = embed("https://figma.com/file/...")
```

**Note:** Notion uses iFramely for embed validation. Not all URLs may render correctly.

---

## Advanced Blocks

### Table

Create tables with rows and columns.

```python
from notion_api_client import table, table_row

# Create table with 3 columns
tbl = table(
    table_width=3,
    has_column_header=True,
    has_row_header=False
)

# Create table rows
row1 = table_row([["Header 1"], ["Header 2"], ["Header 3"]])
row2 = table_row([["Data 1"], ["Data 2"], ["Data 3"]])
row3 = table_row([["More data"], ["Even more"], ["Last cell"]])

# Append to page
client.append_blocks(page_id, [
    {**tbl, "table": {**tbl["table"], "children": [row1, row2, row3]}}
])
```

**Important Notes:**
- `table_width` cannot be changed after creation
- Must have at least one `table_row` child when created
- Cell contents must match the `table_width`

### Equation

LaTeX/KaTeX mathematical equations.

```python
from notion_api_client import equation

eq1 = equation("e=mc^2")
eq2 = equation("\\frac{a}{b}")
eq3 = equation("\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}")
```

### Synced Block

Create blocks that sync content across multiple locations.

```python
from notion_api_client import synced_block, paragraph

# Create original synced block with content
original = synced_block(children=[
    paragraph("This content will be synced everywhere!")
])

# After creating original, get its ID and create duplicates
duplicate = synced_block(block_id="original_block_id_here")
```

**Note:** Original must be created before duplicates.

---

## Container Blocks

### Column List & Columns

Create multi-column layouts.

```python
from notion_api_client import column_list, column, paragraph

# Create column list with 2 equal-width columns
col_list = column_list()

col1 = column()  # Equal width (default)
col2 = column()

# Or specify width ratios (must add up to 1)
col1_wide = column(width_ratio=0.67)
col2_narrow = column(width_ratio=0.33)

# Build the structure with children
client.append_blocks(page_id, [{
    **col_list,
    "column_list": {
        "children": [
            {**col1, "column": {"children": [paragraph("Left column content")]}},
            {**col2, "column": {"children": [paragraph("Right column content")]}}
        ]
    }
}])
```

**Important Notes:**
- Must have at least 2 columns when created
- Width ratios should add up to 1.0
- Columns can contain any block type except other columns

---

## Special Blocks

### Divider

Horizontal line separator.

```python
from notion_api_client import divider

div = divider()
```

### Breadcrumb

Navigation breadcrumb trail.

```python
from notion_api_client import breadcrumb

bc = breadcrumb()
```

### Table of Contents

Auto-generated table of contents based on headings.

```python
from notion_api_client import table_of_contents

toc = table_of_contents(color="default")
```

---

## Complete Example: Rich Page Creation

Here's a complete example showing multiple block types:

```python
from notion_api_client import (
    NotionTemplateClient,
    heading_1, heading_2, paragraph, divider,
    bullet_list_item, numbered_list_item, to_do,
    callout, code, quote, image, table_of_contents
)

# Initialize client
client = NotionTemplateClient()

# Build page content
page_blocks = [
    # Header
    heading_1("Project Documentation"),
    table_of_contents(),
    divider(),
    
    # Introduction
    heading_2("Overview"),
    paragraph("Welcome to the project documentation."),
    callout("This is a living document.", icon="📝"),
    
    # Features list
    heading_2("Key Features"),
    bullet_list_item("Fast and reliable"),
    bullet_list_item("Easy to use"),
    bullet_list_item("Well documented"),
    
    # Tasks
    heading_2("Action Items"),
    to_do("Complete setup", checked=True),
    to_do("Review documentation", checked=False),
    to_do("Deploy to production", checked=False),
    
    # Code example
    heading_2("Quick Start"),
    code(
        "from notion_api_client import NotionTemplateClient\nclient = NotionTemplateClient()",
        language="python"
    ),
    
    # Quote
    divider(),
    quote("Simplicity is the ultimate sophistication. - Leonardo da Vinci"),
]

# Create page with all blocks
page = client.create_page(
    parent_id=database_id,
    title="Complete Documentation",
    children=page_blocks
)

print(f"✅ Created page with {len(page_blocks)} blocks!")
```

---

## Working with Child Blocks

Some block types support nested children:

```python
from notion_api_client import toggle, bullet_list_item, paragraph

# Toggle with children
toggle_block = {
    **toggle("Details"),
    "toggle": {
        **toggle("Details")["toggle"],
        "children": [
            paragraph("Hidden content 1"),
            paragraph("Hidden content 2")
        ]
    }
}

# Nested lists
bullet_with_children = {
    **bullet_list_item("Parent item"),
    "bulleted_list_item": {
        **bullet_list_item("Parent item")["bulleted_list_item"],
        "children": [
            bullet_list_item("Child item 1"),
            bullet_list_item("Child item 2")
        ]
    }
}

client.append_blocks(page_id, [toggle_block, bullet_with_children])
```

**Blocks that support children:**
- Paragraph
- Bulleted list item
- Numbered list item
- To-do
- Toggle
- Quote
- Callout
- Headings (when `is_toggleable=True`)
- Column
- Synced block (original only)
- Table

---

## API Conventions & Best Practices

### Rich Text Objects

All text blocks use rich text objects internally:

```python
{
    "type": "text",
    "text": {
        "content": "Your text here",
        "link": None  # or {"url": "https://..."}
    },
    "annotations": {
        "bold": False,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default"
    }
}
```

### Color Options

All color-supporting blocks accept these values:
- **Text colors:** `"default"`, `"gray"`, `"brown"`, `"orange"`, `"yellow"`, `"green"`, `"blue"`, `"purple"`, `"pink"`, `"red"`
- **Background colors:** `"{color}_background"` (e.g., `"blue_background"`)

### File Uploads

For uploading files (images, videos, PDFs, etc.):

1. Use the [File Upload API](https://developers.notion.com/reference/file-upload)
2. Get the `file_upload_id` from the response
3. Pass it to block functions with `is_external=False`

```python
# Pseudo-code for file upload flow
file_upload_response = client.upload_file("path/to/image.jpg")
file_upload_id = file_upload_response["id"]

# Use in block
img_block = image(file_upload_id, caption="My image", is_external=False)
```

### Block Limitations

- **Table width** cannot be changed after creation
- **Column lists** must have at least 2 columns
- **Synced blocks** require original to exist before creating duplicates
- **Link preview blocks** are read-only (cannot be created via API)
- Some blocks in the Notion UI may not be supported (will appear as `"unsupported"`)

---

## References

- [Notion API Block Reference](https://developers.notion.com/reference/block)
- [Notion API Pagination](https://developers.notion.com/reference/intro#pagination)
- [Notion API Examples](https://developers.notion.com/page/examples)
- [File Upload API](https://developers.notion.com/reference/file-upload)

---

**Last Updated:** October 5, 2025  
**API Version:** 2025-09-03  
**Status:** ✅ Complete
