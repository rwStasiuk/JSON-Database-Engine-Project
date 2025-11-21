'''
FILENAME: jsondb_errorcode_v1.py
VERSION: 1
AUTHOR: Reid Stasiuk
ORG: None (Personal Project)
DATE: 10/26/2025
SUMMARY: Exception handling classes for the JSONDB class.
'''


class JsonDbError(Exception):
    '''Base exception class for JSONDB class-specific exceptions. Inherits from the python built-in Exception class'''
    
    code = 1000    # fallback code

    def __init__(self, message=None):                       # initialize the exception with an optional message
        self.message = message or self.__class__.__name__
        super().__init__(self.message)

    def __str__(self):                                      # triggered to print when the exception is raised
        return f"{self.message} [Error Code: {self.code}]"  # return formatted string with error message and code




'''JSONDB derived exceptions. Error codes are redefined and messages are defined at the time that an exception is raised. 
   Inherit from the JsonDbError base class'''

class PathError(JsonDbError):
    code = 1001

class FileError(JsonDbError):
    code = 1002

class DataError(JsonDbError):
    code = 1003

class LookUpError(JsonDbError):
    code = 1004

class InsertionError(JsonDbError):
    code = 1005