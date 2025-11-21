# JSONDB — Lightweight JSON Database Engine
**FILENAME:** README.md  
**VERSION:** 1  
**AUTHOR:** Reid Stasiuk  
**DATE:** 10/20/2025  
**SUMMARY:** The README file for the JSONDB class (`jsondb_working.py`)

---

## TABLE OF CONTENTS
1. [QUICKSTART CODE](#quickstart-code)  
2. [DESCRIPTION](#description)  
3. [RELEASE PACKAGE](#release-package)  
4. [CLASS ATTRIBUTES](#class-attributes)  
5. [CLASS METHODS](#class-methods)  
6. [ERROR HANDLING](#error-handling)  
7. [DEPENDENCIES](#dependencies)  
8. [USAGE EXAMPLE](#usage-example)  
9. [VERSIONING / ROADMAP](#versioning--roadmap)

---

## QUICKSTART CODE
```python
db = JSONDB("data.json")
db.load()
db.addC("users")
db.addI("users", "Alice")
db.setValue("users", "Alice", "email", "alice@example.com")
db.save()
```

---

## DESCRIPTION

The JSONDB class is a python database engine that supports structured data in json format. It allows users to manage persistent json data by copying the data into a mutable python dictionary and allowing users to edit it before saving the altered data back to the json file. The database engine controls how data is structured, accessed, modified and persisted.

JSON (JavaScript Object Notation) is a lightweight text-based format that is used to represent structured data in a human-readable and machine-parseable way. It is widely used for data storage, configuration files and inter-system communication (particularly in web applications and APIs). JSON works by organizing data into key–value pairs and nested structures, allowing complex data to be transmitted or stored in a simple, language-independent format.

Version 1 of the database engine is single-threaded and implements the core design of the system. See the 'Versioning' section for upcoming features and additions (Atomic write, CLI, querying, multi-threading, etc).

In the current version (v1), json data is permitted to be structured in one way under a protected attribute called `_cache`:

```json
{
    "meta": {
        "version": "vX",
        "bytes": XX,
        "updated": "YYYY-MM-DDTHH:MM:SSZ"
    },
    "collections": {
        "collection_1": {
            "item_1": {"key_1": "value_1", ...},
            "item_2": {...}
        },
        "collection_2": {
            ...
        }
    }
}
```

The "meta" object is managed internally (json objects are enclosed with curly braces {}). The "collections" object is the actual database, which is defined as a python dictionary.

To be compatible with the database engine, json files must meet the following criteria:

1. Root structure must be a json object {}
2. Under the root structure, only json objects may exist (these are referred to as collections)
3. Under each collection, only json objects may exist (these are referred to as items)

Collections, items and the key:value pairs under each item are managed by the user.

When a JSONDB class is created, the user must provide a file name or path where the json file is to be accessed. If the file does not already exist at the path, it will be automatically created. This design demands that the initial state of the json file is considered.

1. **When a new json file is created or the existing file is empty:**  
   Upon deserializing, the database is assumed to be in the default state (meta data and empty database)

2. **When the existing file has "meta" and "collections" root structures:**  
   The file is already in the correct form, so the default structure is completely replaced with the file contents upon deserialization

3. **When the existing file is not empty, but is not structured:**  
   The file must go through validation steps to ensure it is compatible with the database engine before copying the file's root structure into an instance of JSONDB.

---

## RELEASE PACKAGE

The v1 release package includes five files and supports one data structure:

1. Class definition (`jsondb_v1.py`)
2. Exception handling classes (`jsondb_errorcode_v1.py`)
3. Program test (`jsondb_test_v1.py`)
4. JSON data (`data_v1.json`)
5. README file (`jsondb_README_v1.txt`)

Example `_cache` structure:

```
_cache = {                                  
    "meta": {                               
        "version": vX
        "bytes": XX
        "updated": YYYY-MM-DDTHH:MM:SSZ
    }

    "collections": {
        
        "collection_1": {

            "item_1": {"key_1": "value_1", ...}
            "item_2": {...}
            ...
        }

        "collection_2": {
            ...
        }
    }
}
```

---

## CLASS ATTRIBUTES

### `path`
- **Type:** Public  
- **Description:** Contains the database path or file name. Passed as argument during JSONDB instantiation.

### `_cache`
- **Type:** Protected  
- **Description:** An in-memory copy of the json file at the time that `load()` is called.

---

## CLASS METHODS

### `_validate`  
**Type:** Protected  
**Desc:** Determine if a json file is in a compatible format and how data should be de-serialized based on the structure of the file.

### `load`  
**Type:** Public  
**Desc:** Read the contents of the json file into the instance’s `_cache` protected attribute.

### `save`  
**Type:** Public  
**Desc:** Serialize the instance's data back to disk.

### `metaUpdate`  
**Type:** Protected  
**Desc:** Update meta data (file size and last save timestamp).

### `_getC`  
**Type:** Protected  
**Desc:** Returns a reference to a collection dictionary in `_cache`.

### `_getI`  
**Type:** Protected  
**Desc:** Returns a reference to an item within a collection in `_cache`.

### `addC`  
**Type:** Public  
**Desc:** Adds a data collection.

### `addI`  
**Type:** Public  
**Desc:** Adds an item to an existing collection.

### `getValue`  
**Type:** Public  
**Desc:** Retrieves the value associated with a key inside an item.

### `setValue`  
**Type:** Public  
**Desc:** Adds a new key:value pair to the specified item.

### `deleteC`  
**Type:** Public  
**Desc:** Deletes a collection and its items.

### `deleteI`  
**Type:** Public  
**Desc:** Deletes an item from a collection.

---

## ERROR HANDLING

1. **PathError:** Invalid path  
2. **FileError:** Permission or file-format issues  
3. **DataError:** Data handling failure (read/write/meta)  
4. **LookUpError:** Collection or item does not exist  
5. **InsertionError:** Failure creating collection or item  

---

## DEPENDENCIES

1. `json`  
2. `pathlib -> Path`  
3. `datetime`  
4. `sys`  
5. `jsondb_errorcode`  

---

## USAGE EXAMPLE

```python
db = JSONDB("data.json")   # create new database object
db.load()                  # read data into the object

db.addC("users")           # create collection
db.addI("users", "Bob")    # create item

bob = db.getI("users", "Bob")
bob["email"] = "bob@example.com"

db.save()
```

---

## VERSIONING / ROADMAP

```
Legend:
C - Current
P - In Progress
N - Not Started
```

### **v1 (C): Serial, Deserialize and CRUD**
- Basic CRUD  
- Basic (de)serialization  
- Basic error handling  

### **v2 (P): Atomic Write, Backups, Logging, Context Manager**
- Atomic writes  
- Automatic backups  
- Logging  
- `__enter__` and `__exit__` support  

### **v3 (N): CLI**
- Simple command line interface  

### **v4 (N): Querying and Transactions**
- Filtering  
- Searching  
- Sorting  
- Simple transactions  

### **v5 (N): Multi-Model Architecture**
- Table model  
- Graph model  
- Tree model  
- Collection model (current)

#### Example future interfaces:

```python
# Table model
db = JSONDB("data.json", model="table")
db.create_table("users", columns=["id", "name", "email"])
db.insert_row("users", [1, "Alice", "alice@example.com"])

# Collection model
db = JSONDB("data.json", model="collection")
db.addC("users")
db.addI("users", "Alice")
db.setValue("users", "Alice", "email", "alice@example.com")
```
