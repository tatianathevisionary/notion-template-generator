# Multi-Format Update Generation System

Transform your weekly notes into professional updates across 4 formats automatically.

## 🎯 What This Does

Takes structured weekly update data and generates:
- **📄 Detailed Document** - Comprehensive Markdown report for stakeholders
- **💬 Slack Update** - Concise, emoji-rich team update (< 500 words)
- **🔗 LinkedIn Post** - Engaging public update with CTAs
- **📝 Blog Post** - SEO-friendly long-form content

## 🚀 Quick Start

### 1. Fill Out the Template

```bash
# Copy the template
cp update_template.json my_weekly_update.json

# Edit with your week's data
nano my_weekly_update.json  # or use any editor
```

### 2. Generate All Formats

```bash
python update_generator.py my_weekly_update.json
```

That's it! You'll get 4 ready-to-publish files.

## 📋 Template Structure

The `update_template.json` file has this structure:

```json
{
  "project_name": "Your Project Name",
  "date": "2025-10-05",
  "status": "on_track",  // or "at_risk" | "off_track"
  
  "highlight": "The single most important accomplishment",
  "next_priority": "The #1 priority for next week",
  
  "progress": [
    "Accomplishment 1",
    "Accomplishment 2",
    "Accomplishment 3"
  ],
  
  "goals": [
    "Priority 1 for next week",
    "Priority 2 for next week"
  ],
  
  "metrics": [
    {
      "name": "Metric Name",
      "value": "100",
      "change": "+10%"
    }
  ],
  
  "risks": [
    {
      "type": "blocker",  // or "risk"
      "description": "What's blocking progress"
    }
  ],
  
  "decisions": [
    "Key decision made this week"
  ],
  
  "learnings": [
    "Important insight learned"
  ],
  
  "asks": [
    "Specific help needed"
  ]
}
```

## 📊 Generated Output Examples

### Slack Update (concise, scannable)

```
*Notion Template Generator Weekly Update* • 2025-10-05

🟢 *Status:* On Track

*🎯 This Week's Win*
Successfully upgraded to Notion API 2025-09-03

*✅ What We Shipped*
• Upgraded to Notion API 2025-09-03
• Built Complete Database Retrieval System
• Enhanced Content Hub with 210 Rich Blocks

*🚀 Next Week*
• Build multi-format update generation system
• Enhance remaining 4 databases

*📊 Key Metrics*
• API Version: *2025-09-03* upgraded
• Databases Enhanced: *1 of 5* 20%

_Full details in thread_ 👇
```

### LinkedIn Post (engaging, public-facing)

```
🚀 Week in Review: Notion Template Generator

Successfully upgraded to Notion API 2025-09-03 and built
comprehensive database enhancement tools

Here's what we shipped this week:

✅ Upgraded to Notion API 2025-09-03
🎯 Built Complete Database Retrieval System
💡 Enhanced Content Hub with 210 Rich Blocks

💭 Key insight:
Data source IDs are mandatory in 2025-09-03

What's the biggest win from your week? 👇

#BuildInPublic #ProductDevelopment #TechUpdates
```

### Blog Post (comprehensive, SEO-friendly)

Full blog post with:
- SEO-optimized title
- Introduction with hook
- Detailed sections for each accomplishment
- Code blocks and technical details
- Challenges & solutions section
- What's next preview
- Conclusion with CTA

## 💡 Best Practices

### Writing Your Updates

**Progress Items:**
- ✅ Use action verbs: Built, Shipped, Completed, Created
- ✅ Include impact: "Enhanced Content Hub with 210 blocks"
- ❌ Avoid vague: "Worked on database stuff"

**Goals:**
- ✅ Keep to 3-5 items max
- ✅ Make them specific and measurable
- ✅ Focus on outcomes, not activities

**Metrics:**
- ✅ Include week-over-week change
- ✅ Show momentum: "+210 blocks created"
- ✅ Use relevant metrics for your audience

**Risks & Blockers:**
- ✅ Be transparent - surface problems early
- ✅ Include mitigation plans if possible
- ✅ Specify if it's a "risk" (potential) or "blocker" (current)

**Decisions & Learnings:**
- ✅ Document the "why" for future reference
- ✅ These become your knowledge base
- ✅ Be specific and actionable

**Asks:**
- ✅ Make requests actionable
- ✅ Specify exactly what you need
- ✅ Include context for why it's needed

## 🛠️ Advanced Usage

### Custom Output Directory

```bash
python update_generator.py my_update.json ./updates/week_42/
```

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Generate weekly update
  run: python update_generator.py update_template.json ./outputs/
  
- name: Post to Slack
  run: |
    curl -X POST $SLACK_WEBHOOK_URL \
      -H 'Content-Type: application/json' \
      -d @outputs/*_slack_*.txt
```

### Programmatic Usage

```python
from update_generator import UpdateGenerator

# Create generator
generator = UpdateGenerator("My Project", "2025-10-05")

# Load data
generator.load_from_template({
    "status": "on_track",
    "highlight": "Shipped feature X",
    # ... rest of data
})

# Generate specific format
slack_text = generator.generate_slack_update()
linkedin_text = generator.generate_linkedin_post()

# Or generate all
files = generator.generate_all("./output")
```

## 📁 File Organization

Recommended structure:

```
project/
├── updates/
│   ├── 2025-10-05/
│   │   ├── template.json
│   │   ├── document.md
│   │   ├── slack.txt
│   │   ├── linkedin.txt
│   │   └── blog.md
│   └── 2025-10-12/
│       └── ...
└── templates/
    └── update_template.json
```

## 🎨 Customization

### Modify Format Templates

Edit `update_generator.py` to customize:

1. **Slack Format**: Adjust emoji usage, section order
2. **LinkedIn Format**: Change hashtags, hook style
3. **Blog Format**: Modify SEO elements, structure
4. **Document Format**: Adjust sections, detail level

### Add New Formats

```python
def generate_twitter_thread(self) -> str:
    """Generate Twitter/X thread format."""
    # Your custom format here
    pass
```

## 🔍 Tips for Each Format

### Slack
- **Keep it brief**: Under 500 words
- **Use emojis**: Visual scanning is key
- **Link to details**: Use threads for more context
- **Status up front**: Team needs to know status immediately

### LinkedIn
- **Hook in first 2 lines**: Most people don't click "see more"
- **Line breaks matter**: After every 1-2 sentences
- **Ask a question**: Drives engagement
- **3-5 hashtags**: More looks spammy

### Blog
- **SEO-friendly title**: Include keywords and date
- **Clear structure**: H2/H3 headings for scanning
- **Code blocks**: Show technical details
- **Conclusion with CTA**: What should readers do next?

### Document
- **Comprehensive but scannable**: Use bullet points
- **Link to references**: Previous updates, PRs, issues
- **Metrics with context**: WoW change, trend direction
- **Document decisions**: Future you will thank present you

## 📚 Examples

See the `examples/` directory for real weekly updates in all formats:

- `example_week_1_ontrack.json` - Successful sprint
- `example_week_2_atrisk.json` - Handling blockers
- `example_week_3_offt track.json` - Crisis management

## 🤝 Contributing

To improve the generator:

1. Add new format generators
2. Enhance existing templates
3. Add format-specific best practices
4. Create example templates

## 📝 License

MIT License - feel free to use and modify for your projects.

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `python update_generator.py` | Run demo with example data |
| `python update_generator.py template.json` | Generate from template |
| `python update_generator.py template.json ./out/` | Custom output directory |

| Status Options | Emoji | When to Use |
|----------------|-------|-------------|
| `on_track` | 🟢 | Meeting goals, no major blockers |
| `at_risk` | 🟡 | Some blockers, may miss deadlines |
| `off_track` | 🔴 | Significant issues, needs attention |

---

**Created:** October 5, 2025  
**Last Updated:** October 5, 2025  
**Version:** 1.0.0
