# Quick Start Guide

## ✅ Configuration Complete!

Your `.env` file has been created with:
- **API Key**: `ntn_Y36581308888Vfh414I9aHzOwm8QgZFxHFeouPaJMWq8a3`
- **Parent Page ID**: `2830da0aa5c8807e9b5cf5c9411b445f`

## 🔑 Important: Share Your Page with the Integration

Before running the script, you **must** give your Notion integration access to the parent page:

1. **Open your Notion page**: [Open in Notion](https://www.notion.so/tatianathevisionary/2830da0aa5c8807e9b5cf5c9411b445f)

2. **Click the "..." menu** (top right of the page)

3. **Scroll down and click "Add connections"**

4. **Search for and select your integration** (the one you created with the API key above)

5. **Click "Confirm"** to grant access

> ⚠️ **Without this step, the script will fail with a "page not found" or "unauthorized" error!**

## 🚀 Run the Template Generator

### Option 1: Quick Setup with Script

```bash
cd "/Users/tatiana/Cloning me/notion_template_generator"
./setup.sh
python main.py
```

### Option 2: Manual Setup

```bash
cd "/Users/tatiana/Cloning me/notion_template_generator"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the generator
python main.py
```

## 📊 What Will Be Created

The script will create these four databases in your Notion workspace:

1. **🎯 Opportunity Hub**
   - Track and evaluate product opportunities
   - Properties: Status, Priority, Impact Score, Effort Score

2. **📋 AI Product Spec Generator**
   - Create structured product specifications
   - Properties: Status, Owner, Target Release, PRD Status

3. **🧪 Experiment Tracker**
   - Plan, track, and analyze experiments
   - Properties: Hypothesis, Success Metric, Result, Dates

4. **🚀 Launch & Growth Hub**
   - Manage launches and growth initiatives
   - Properties: Phase, Channel, Launch Date, Key Metrics

## 🎯 Expected Output

When you run `python main.py`, you should see:

```
============================================================
🎨 NOTION TEMPLATE GENERATOR
============================================================
Creating AI Product Manager OS templates...

🚀 Creating Opportunity Hub...
✅ Successfully created database: 🎯 Opportunity Hub

📋 Creating AI Product Spec Generator...
✅ Successfully created database: 📋 AI Product Spec

🧪 Creating Experiment Tracker...
✅ Successfully created database: 🧪 Experiment Tracker

🚀 Creating Launch & Growth Hub...
✅ Successfully created database: 🚀 Launch & Growth Hub

============================================================
✅ TEMPLATE CREATION COMPLETE!
============================================================

📊 Created Databases:
  • Opportunity Hub: [database_id]
  • AI Product Spec: [database_id]
  • Experiment Tracker: [database_id]
  • Launch & Growth Hub: [database_id]

🔗 Visit your Notion workspace to see the new templates!
```

## 🔧 Troubleshooting

### Error: "object not found" or "Could not find page"
- Make sure you've shared the parent page with your integration
- Double-check the page ID in `.env` matches your Notion page URL

### Error: "Unauthorized" or "API key is invalid"
- Verify your API key in `.env` is correct
- Check that your integration is active at https://www.notion.com/my-integrations

### Error: "Module not found"
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Run `pip install -r requirements.txt` again

## 📚 Next Steps

After successful creation:

1. **Explore the databases** in your Notion workspace
2. **Customize properties** by editing the JSON files in `templates/`
3. **Add sample data** to test the structure
4. **Extend functionality** by modifying `main.py` to add page templates, views, or relations between databases

## 💡 Tips

- The databases will be created as **siblings** to your parent page
- You can run the script multiple times (it will create duplicate databases)
- To avoid duplicates, delete old databases in Notion before re-running
- Check out the JSON templates to understand the database schemas

Ready to go? Run the script now! 🚀
