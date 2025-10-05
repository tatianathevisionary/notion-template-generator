# 🔧 Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Setup Issues

#### "Python not found" Error
**Problem**: Command line can't find Python
**Solution**: 
1. Install Python 3.8+ from [python.org](https://python.org)
2. Add Python to your system PATH
3. Restart your terminal/command prompt

#### "pip install failed" Error
**Problem**: Package installation fails
**Solution**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# If still failing, try:
pip install --user -r requirements.txt
```

#### "Permission denied" Error
**Problem**: Script can't write to directories
**Solution**:
```bash
# On Mac/Linux
chmod +x setup.py
./setup.py

# On Windows
python setup.py
```

### Notion Integration Issues

#### "Invalid API key" Error
**Problem**: Notion API key is incorrect
**Solution**:
1. Go to [notion.so/my-integrations](https://notion.so/my-integrations)
2. Create a new integration or check existing one
3. Copy the API key exactly (no extra spaces)
4. Update your `.env` file

#### "Page not found" Error
**Problem**: Parent page ID is incorrect
**Solution**:
1. Open your Notion page in browser
2. Copy the page ID from the URL (32-character string)
3. Update `NOTION_PARENT_PAGE_ID` in `.env`

#### "Permission denied" Error
**Problem**: Integration doesn't have access to page
**Solution**:
1. In Notion, click "Share" on your page
2. Click "Add people, emails, groups, or integrations"
3. Search for your integration name
4. Give it "Full access" permissions

### Database Issues

#### "Database creation failed" Error
**Problem**: Can't create databases in Notion
**Solution**:
1. Ensure your integration has database creation permissions
2. Check that the parent page allows database creation
3. Verify your API key is valid

#### "Schema modification failed" Error
**Problem**: Can't modify database properties
**Solution**:
1. Ensure you're using the correct database ID
2. Check that the database exists and is accessible
3. Verify your integration has edit permissions

### Performance Issues

#### "Slow loading" Problem
**Problem**: System is slow or unresponsive
**Solution**:
1. Check your internet connection
2. Reduce database size by archiving old content
3. Close other applications using Notion
4. Restart the MCP server

#### "Memory error" Problem
**Problem**: System runs out of memory
**Solution**:
1. Close other applications
2. Reduce batch sizes in scripts
3. Process data in smaller chunks
4. Upgrade your system RAM if possible

### Content Issues

#### "Voice discovery not working" Problem
**Problem**: Voice discovery questionnaire doesn't load
**Solution**:
1. Ensure all required pages are created
2. Check that the questionnaire database exists
3. Verify your Notion permissions

#### "Content generation failed" Problem
**Problem**: AI content generation doesn't work
**Solution**:
1. Check your internet connection
2. Verify the MCP server is running
3. Ensure all prompts are loaded correctly

## 🔍 Debug Mode

Enable debug mode for detailed error information:

```bash
# Set debug mode in .env
DEBUG=True
LOG_LEVEL=DEBUG

# Run with verbose output
python mcp_server.py --verbose
```

## 📊 System Diagnostics

Run the diagnostic script to check your system:

```bash
python 02_Core_System/scripts/test_tools.py
```

This will check:
- Python version compatibility
- Package installation
- Notion API connectivity
- Database accessibility
- MCP server functionality

## 🆘 Getting Help

### Before Contacting Support

1. **Check this guide** - Your issue might be covered here
2. **Run diagnostics** - Use the test script to identify problems
3. **Check logs** - Look for error messages in the console
4. **Try restarting** - Often fixes temporary issues

### When Contacting Support

Include this information:
- **Error message** (exact text)
- **Steps to reproduce** (what you were doing)
- **System info** (OS, Python version)
- **Diagnostic results** (from test script)

### Emergency Recovery

If everything breaks:
1. **Backup your data** - Export your Notion databases
2. **Fresh install** - Delete and reinstall the template
3. **Restore data** - Import your backed-up databases
4. **Contact support** - We'll help you recover

## 📈 Performance Optimization

### Database Optimization
- **Archive old content** - Keep databases lean
- **Use filters** - Reduce data loading
- **Batch operations** - Process multiple items together

### System Optimization
- **Close unused apps** - Free up system resources
- **Update regularly** - Keep everything current
- **Monitor usage** - Watch for resource consumption

---

**Still having issues?** Contact our support team with the diagnostic results! 🚀
