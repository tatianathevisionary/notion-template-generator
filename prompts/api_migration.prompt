# API Migration Guide: Upgrading to Notion API 2025-09-03

## 📋 Overview

This document describes the migration of the Notion Template Generator from older API versions to **Notion API version 2025-09-03**, which introduces first-class support for multi-source databases.

**Migration Date**: October 5, 2025  
**Status**: ✅ Complete

---

## 🎯 What Changed

### Key Changes in 2025-09-03

1. **Data Sources**: Databases now contain one or more data sources
2. **New Endpoints**: Operations moved from `/databases/*` to `/data_sources/*`
3. **Parent References**: Pages now use `data_source_id` instead of `database_id`
4. **Database Creation**: Properties wrapped in `initial_data_source` object
5. **Query Operations**: Now operate on data sources, not databases directly

### Why This Matters

The new architecture enables:
- Multiple linked data sources within a single database
- More flexible data organization
- Better support for complex workflows
- Enhanced database relationships

**⚠️ Not Backwards Compatible**: Old integrations will fail if users add multiple data sources to a database.

---

## 🔄 Migration Changes Made

### 1. Client Initialization

**Before:**
```python
client = Client(auth=api_key)
```

**After:**
```python
client = Client(auth=api_key, notion_version="2025-09-03")
```

**File**: `notion_api_client.py:44`

---

### 2. Database Creation

**Before:**
```python
response = self.client.databases.create(
    parent={"type": "page_id", "page_id": parent_id},
    title=[{"type": "text", "text": {"content": title}}],
    properties=properties  # Direct properties
)
```

**After:**
```python
response = self.client.databases.create(
    parent={"type": "page_id", "page_id": parent_id},
    title=[{"type": "text", "text": {"content": title}}],
    initial_data_source={
        "properties": properties  # Wrapped in initial_data_source
    },
    icon=icon,  # Optional
    cover=cover  # Optional
)

# Response now includes data_sources array
data_source_id = response["data_sources"][0]["id"]
```

**File**: `notion_api_client.py:54-119`

---

### 3. Getting Data Source ID (NEW)

**New Helper Method:**
```python
def get_data_source_id(self, database_id: str, index: int = 0) -> str:
    """
    Get the data source ID for a database.
    Essential for 2025-09-03 API operations.
    """
    database = self.get_database(database_id)
    data_sources = database.get("data_sources", [])
    
    if not data_sources:
        raise ValueError(f"No data sources found for database {database_id}")
    
    return data_sources[index]["id"]
```

**File**: `notion_api_client.py:245-270`

---

### 4. Creating Pages in Database

**Before:**
```python
page_data = {
    "parent": {"database_id": database_id},
    "properties": properties
}
```

**After:**
```python
# Step 1: Get data_source_id
data_source_id = self.get_data_source_id(database_id)

# Step 2: Use data_source_id as parent
page_data = {
    "parent": {"type": "data_source_id", "data_source_id": data_source_id},
    "properties": properties
}
```

**File**: `notion_api_client.py:159-205`

---

### 5. Querying Database

**Before:**
```python
response = self.client.databases.query(
    database_id=database_id,
    filter=filter_conditions
)
```

**After:**
```python
# Step 1: Get data_source_id
data_source_id = self.get_data_source_id(database_id)

# Step 2: Query data source endpoint
response = self.client.request(
    method="POST",
    path=f"data_sources/{data_source_id}/query",
    body={"filter": filter_conditions} if filter_conditions else {}
)
```

**File**: `notion_api_client.py:301-336`

---

### 6. Retrieving Data Source (NEW)

**New Method:**
```python
def retrieve_data_source(self, data_source_id: str) -> Dict[str, Any]:
    """
    Retrieve a data source by ID to get its schema/properties.
    """
    response = self.client.request(
        method="GET",
        path=f"data_sources/{data_source_id}"
    )
    return response
```

**File**: `notion_api_client.py:272-291`

---

### 7. Updating Data Source (NEW)

**New Method:**
```python
def update_data_source(
    self,
    data_source_id: str,
    properties: Optional[Dict[str, Any]] = None,
    title: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Update a data source's schema or title.
    Use this instead of update_database for schema changes.
    """
    update_body = {}
    if properties:
        update_body["properties"] = properties
    if title:
        update_body["title"] = title
    
    response = self.client.request(
        method="PATCH",
        path=f"data_sources/{data_source_id}",
        body=update_body
    )
    return response
```

**File**: `notion_api_client.py:338-371`

---

## 📊 Files Modified

| File | Changes | Lines Modified |
|------|---------|---------------|
| `notion_api_client.py` | Core API wrapper upgrade | ~150 lines |
| `requirements.txt` | No changes (SDK compatible) | 0 |
| `main.py` | Works automatically with updated client | 0* |
| `linkedin_content_os.py` | Works automatically with updated client | 0* |
| `linkedin_content_os_complete.py` | Works automatically with updated client | 0* |

*No changes needed because they use the client wrapper methods, which handle the new API internally.

---

## ✅ Backward Compatibility Strategy

### Automatic Data Source ID Resolution

The updated client **automatically handles data source IDs**, so existing code continues to work:

```python
# This still works! Client fetches data_source_id internally
client.create_page_in_database(
    database_id=database_id,  # Can still pass database_id
    properties=properties,
    children=children
)
```

The client:
1. Accepts `database_id` as before
2. Internally calls `get_data_source_id(database_id)`
3. Uses the data source ID in the API call
4. Returns the same response structure

### Optional Explicit Control

For advanced use cases, you can provide `data_source_id` directly:

```python
# Explicit control for multi-source databases
data_source_id = client.get_data_source_id(database_id, index=1)  # 2nd source

client.create_page_in_database(
    database_id=database_id,
    data_source_id=data_source_id,  # Use specific source
    properties=properties
)
```

---

## 🧪 Testing Results

### Test 1: Database Creation
```bash
✅ Successfully created database: Content Hub
   📊 Data source ID: 248104cd-477e-80af-bc30-000bd28de8f9
   📊 Data source name: Content Hub
```

### Test 2: Page Creation
```bash
✅ Created page: Example Post Title
```

### Test 3: Query Operation
```bash
📊 Database has 1 data source(s)
✅ Found 5 pages in query results
```

### Test 4: Data Source Retrieval
```bash
✅ Retrieved data source schema
   - 7 properties defined
   - Parent database: 6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b
```

---

## 📚 New Capabilities

### 1. Multi-Source Database Support

```python
# Get all data sources in a database
database = client.get_database(database_id)
for ds in database["data_sources"]:
    print(f"Data Source: {ds['name']} (ID: {ds['id']})")
```

### 2. Data Source-Specific Operations

```python
# Query specific data source
results = client.query_database(
    database_id=database_id,
    data_source_id=specific_source_id
)

# Update specific data source schema
client.update_data_source(
    data_source_id=specific_source_id,
    properties={"NewField": {"rich_text": {}}}
)
```

### 3. Database Structure Retrieval

```python
# Get full database structure
database = client.get_database(database_id)
print(f"Database: {database['title']}")
print(f"Parent: {database['parent']}")
print(f"Data Sources: {len(database['data_sources'])}")

# Get detailed schema from data source
data_source_id = database["data_sources"][0]["id"]
data_source = client.retrieve_data_source(data_source_id)
print(f"Properties: {list(data_source['properties'].keys())}")
```

---

## 🚨 Breaking Changes to Watch

### 1. Direct Database API Calls

If you were using direct API calls (not through our client), update them:

```python
# ❌ Old - Will fail
response = requests.post(
    "https://api.notion.com/v1/databases/DB_ID/query",
    headers={"Notion-Version": "2022-06-28"}
)

# ✅ New - Use data source endpoint
response = requests.post(
    "https://api.notion.com/v1/data_sources/DS_ID/query",
    headers={"Notion-Version": "2025-09-03"}
)
```

### 2. Parent Object Structure

```python
# ❌ Old
parent = {"database_id": database_id}

# ✅ New
parent = {"type": "data_source_id", "data_source_id": data_source_id}
```

### 3. Database Properties

```python
# ❌ Old - Direct properties
database_create_params = {
    "properties": {...}
}

# ✅ New - Wrapped in initial_data_source
database_create_params = {
    "initial_data_source": {
        "properties": {...}
    }
}
```

---

## 📖 Reference Links

- [Official Upgrade Guide](https://developers.notion.com/docs/upgrade-guide-2025-09-03)
- [Data Sources FAQ](https://developers.notion.com/docs/upgrade-guide-2025-09-03#faqs-version-2025-09-03)
- [Notion API Reference](https://developers.notion.com/reference)
- [notion-client SDK](https://github.com/ramnes/notion-sdk-py)

---

## 🎯 Migration Checklist

- [x] Update client initialization with API version
- [x] Wrap properties in `initial_data_source` for database creation
- [x] Add `get_data_source_id()` helper method
- [x] Update `create_page_in_database()` to use data_source_id
- [x] Update `query_database()` to use data source endpoints
- [x] Add `retrieve_data_source()` method
- [x] Add `update_data_source()` method
- [x] Update `get_database()` to handle data_sources array
- [x] Add logging for data source information
- [x] Maintain backward compatibility
- [x] Test all database operations
- [x] Document changes in AGENTS.md
- [x] Create this migration guide
- [x] Update README with API version info

---

## ✨ Benefits

### For Developers
- ✅ Future-proof code
- ✅ Support for multi-source databases
- ✅ Better error handling
- ✅ More flexible data relationships

### For Users
- ✅ More powerful database capabilities
- ✅ Better organization options
- ✅ Enhanced workflows
- ✅ No disruption (backward compatible client)

---

## 🤝 Support

If you encounter issues after the migration:

1. Check that `.env` has correct credentials
2. Verify API version in client initialization
3. Review AGENTS.md for patterns
4. Check error messages for data source issues
5. Ensure databases were created with 2025-09-03 API

---

**Migration Completed**: October 5, 2025  
**Status**: ✅ Production Ready  
**Next Review**: When Notion releases next API version
