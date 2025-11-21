'''
FILENAME: jsondb_v1.py
VERSION: 1
AUTHOR: Reid Stasiuk
ORG: None (Personal Project)
DATE: 10/26/2025
SUMMARY: The JSONDB class definition. See README file.
'''

# dependencies
import json
from pathlib import Path
import datetime
import sys
import jsondb_errorcode_v1 as err
    

class JSONDB:

    def __init__(self, path): # class constructor
        ''' Class constructor - executes upon instantiation of a JSONDB object. Sets up a JSONDB object by defining attributes and validating 
        the 'path' argument. Also defines the structure of the database.

        Args:
            path (str): The path where the .json file exists or should be created (file name if working in current directory)

        Returns:
            None

        Raises:
            PathError: If the path argument does not point to a .json file or there is an error opening the file
        '''

        self.path = Path(path)      # define path attribute as a pathlib path object
        self._cache = {             # data structure (enforced)
            "meta": {"version": 1, 
                     "bytes": 0, 
                     "updated": datetime.datetime.now().isoformat()},
            "collections": {}    
        }

        if self.path.suffix.lower() != ".json": # check if path attibute points to a .json file
            raise err.PathError(f"The file at '{self.path}' is not a .json file.")
        
        try:
            with open(self.path, 'a'): # create a new json file on the disk if it doesn't already exist
                pass
        except Exception as e:
            raise err.PathError(f"The file at '{self.path}' could not be created or opened successfully ({e})")
            

    def _validate(self, data):
        ''' Validates the structure of a json file in the case that a user passes a path that points to a non-empty and unstructured json file.
        To be used before deserializing data.

        Args:
            data (any): Python representation of the contents of a .json file (obtained using json.load() method)

        Returns:
            True: If the data's root structure is a json object and the contents can be structured into collections and items

        Raises:
            DataError: If the user passed a filepath that points to a json file with an incompatible data strucutre
        '''

        if not isinstance(data, dict): # check if the root structure of the file is a json object
            raise err.DataError(f"Invalid database structure: The root element of the file at '{self.path}' must be a json object")
        
        for collection in data.keys(): # verify that all collections in root structure are also json objects
            if not isinstance(data[collection], dict):
                raise err.DataError(f"Invalid database structure: The '{collection}' collection must be a json object")
            
            for item in data[collection]: # for each collection, verify that all items within are json objects
                if not isinstance(data[collection][item], dict):
                    raise err.DataError(f"Invalid database structure: The '{item}' item in the '{collection}' collection must be a json object")
                
        return True # don't care what is inside of each item
    

    def load(self):
        ''' Deserializes .json data from the file at the instance's path into Python dictionary (nested) format.
        
        Reads the data of the .json file into the instance's protected _cache attribute. Validates whether the .json file is in the
        correct format. After this method is called, if there are no validation issues, the instance will possess a copy of the most
        recent .json file state in dictionary form.

        Args:
            None
        
        Return:
            None

        Raises:
            FileError: If there is an error opening or reading from the file
        '''
        
        try:
            with open(self.path, 'r') as f:     # open the .json file at the instance's path attribute

                if not f.read().strip():        # if the file is not empty (must be checked before json.load to avoid JSONDecodeError)
                    return                      # if the file is empty, the data structure defined in the class constructor can be used
                f.seek(0)                       # move back to the start of the file before loading
                d = json.load(f)                # load file data into temp nested dictionary called 'd'

                if (len(d) == 2 and             # check to see if the file is already formatted to the database strucutre 
                    "meta" in d.keys() and 
                    "collections" in d.keys()): 
                    if self._validate(d["collections"]):    # validate object structure of the json file
                        self._cache = d                     # replace entire _cache with the existing file contents
                
                else:
                    if self._validate(d):                   # validate object structure of the json file
                        self._cache["collections"] = d      # replace _cache "collections" dictionary with file contents
       
        except Exception as e:
            raise err.FileError(f"The file at '{self.path}' could not be opened or read from successfully ({e})")


    def save(self):
        ''' Serializes data from the instance's _cache attribute (in memory) to the .json file at the instance's path.

        Writes the data from instance's _cache attribute to the .json file. Note that if the original file did not have any meta data,
        the save function will add a new document to the .json structure called 'meta'. After this method is called, the .json file will
        will be updated with any changes made to the database while in memory.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            FileError: If there is an error opening or writing to the .json file
        '''

        try:
            self.metaUpdate()                               # update meta data upon serialization
            with open(self.path, 'w') as f:                 # open file at path atrribute for writing
                json.dump(self._cache, f, indent=2)         # write contents of _cache attribute to the file

        except Exception as e:
            raise err.FileError(f"The file at '{self.path}' could not be opened or written to successfully ({e})")


    def metaUpdate(self):
        ''' Updates the instance's meta data (size in bytes and timestamp of the most recent save).

        Args:
            None

        Returns:
            None
        
        Raises:
            DataError: If the meta data can't be updated due to a KeyError (meta data could not be found)
        '''

        self._cache["meta"]["bytes"] = sys.getsizeof(self._cache["collections"])    # update file size
        self._cache["meta"]["updated"] = datetime.datetime.now().isoformat()        # update timestamp

        

    def _getC(self, collection):
        ''' Returns a reference to the specified collection (mutations are carrried into the instance's _cache attribute). This method is
        meant for internal use only since it directly accesses the in-memory database copy.

        Args:
            collection (str): The name of the collection to be retrieved

        Returns:
            c (Dictionary): A reference to the specified collection in the database

        Raises:
            LookUpError: If the specified collection name could not be found in the database
        '''

        if collection in self._cache["collections"].keys():     # if the collection is found in the protected _cache attribute
            c = self._cache["collections"][collection]          # return the reference
            return c
        else:
            raise err.LookUpError(f"No collections called '{collection}' could be found")

    
    def _getI(self, collection, item):
        ''' Returns a reference to the specified item (mutations are carried into the instance's _cache attribute). This method is meant
        for internal use only since it directly accesses the in-memory database copy. 

        Args:
            collection (str): The name of the collection where the item resides
            item (UserDef): The name of the item to be retreived

        Returns:
            i (Dictionary): A reference to the specified item in the database

        Raises:
            LookUpError: If the specified item or collection could not be found the in the database
        '''

        if collection in self._cache["collections"].keys():                 # if the collection is found in the protected _cache attribute
            if item in self._cache["collections"][collection].keys():       # if the collection is found in _cache and the item in the collection
                i = self._cache["collections"][collection][item]            # return reference
                return i
            else:
                raise err.LookUpError(f"No items called '{item}' found in the '{collection}' collection")
        else:
            raise err.LookUpError(f"No collections called '{collection}' could be found")
        

    def addC(self, newCollectionName):
        ''' Adds a new collection to the database and verifies that the new collection has a unique name (no duplicates).
        
        Args:
            NewCollectionName (str): The name of the new collection

        Returns:
            None

        Raises:
            InsertionError: If a collection does not have a unique name or the new collection name is not a string type
        '''
        if not isinstance(newCollectionName, str) or not newCollectionName.strip():     # lightweight validation for collection naming
            raise err.InsertionError("Collection name must be a non-empty string.")
        
        if newCollectionName not in self._cache["collections"].keys():                  # verify uniqueness
            self._cache["collections"][newCollectionName] = {}                          # add new collection dictionary to database
        else:
            raise err.InsertionError(f"The database already contains a collection called {newCollectionName}")


    def addI(self, collection, newItemName):
        ''' Adds a new item to the specified collection and verifies that the new item has a unique name (within the collection).

        Args:
            collection (str): The name of the collection that the new item should be added to
            newItemName (str): The name of the new item

        Returns:
            None

        Raises:
            InsertionError: If the new item does not have a unique name or the new item name is not a string type
        '''

        if not isinstance(newItemName, str) or not newItemName.strip():             # lightweight validation for item naming
            raise err.InsertionError("Item name must be a non-empty string.")
        
        if newItemName not in self._cache["collections"][collection].keys():        # verify uniqueness
            self._cache["collections"][collection][newItemName] = {}                # add new item to specified collection
        else:
            raise err.InsertionError(f"The '{collection}' collection already contains an item called {newItemName}")
        

    def getValue(self, collection, item, key):
        ''' Retrieve the value at the specified key of an item dictionary.

        Args:
            collection (str): The name of the collection to look in
            item (str): The name of the item to look in
            key (str): The key to return the value of

        Returns:
            value (UserDef): The value at the specified key

        Raises:
            LookUpError: If the requested key could not be found in the specified item dictionary
        '''

        i = self._getI(collection, item)    # obtain reference to the specified item
        if key in i.keys():                 # verify that the key exists in the item dict              
            value = i[key]                  # return the value associated with the key
            return value
        else:
            raise err.LookUpError(f"A key called '{key}' could not be found under the specified item dictionary")
        


    def setValue(self, collection, item, key, value):
        ''' Creates a key:value pair under the specified item dictionary.

        Args:
            collection (str): The name of the collection to be accessed
            item (str): The name of the item to add a new key:value pair to
            key (str): The name of the new key to be added to the item dictionary
            value (UserDef): The value to be associated with the new key

        Returns:
            None

        Raises:
            InsertionError: If the new key name is not unique or the key:value pair could not be created due to 
        '''

        i = self._getI(collection, item)    # obtain reference to the specified item
        if key not in i.keys():             # verify that the key does not already exist under the specified item
            i[key] = value                  # set the key:value pair
        else:
            raise err.InsertionError(f"The key name '{key}' is not unique in the specified item dictionary")


    def deleteC(self, collection):
        ''' Deletes a collection and all items under it. 

        Args:
            collection (str): The name of the collection to delete

        Returns:
            None
        
        Raises:
            DataError: If the collection does not exist.
        '''

        if collection in self._cache["collections"].keys():     # verify that the collection resides in the database
            del self._cache["collections"][collection]          # delete collection
        else:
            raise err.DataError(f"The collection '{collection}' could not be deleted because it was not found in the database")
        
    
    def deleteI(self, collection, item):
        ''' Deletes an item and all values under it.

        Args:
            collection (str): The name of the collection to delete an item from
            item (str): The name of the item to delete

        Returns:
            None
        
        Raises:
            DataError: If the collection does not exist.
        '''

        if item in self._cache["collections"][collection].keys():   # verify that the item exists under the specified collection
            del self._cache["collections"][collection][item]        # delete item
        else:
            raise err.DataError(f"The item '{item}' could not be deleted because it was not found in the '{collection}' collection")