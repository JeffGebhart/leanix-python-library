# LeanIX Python Library


## Forked from leanix-public/leanix-python-library

Currently very basic functionality.

LeanIX Class will do your authentication and token management.  It will return an object with a number of subclasses:

#graph: A class for managing GraphQL stuff.
```
-execGraphQL(query,variables) - Executes GraphQL, returns raw HTTP Response object
-execGraphQLParsed(query,variables) - same as above, but returns a dict with the JSON of the response parsed out
-execGraphQLTrimmed(query,variables) - Same, as parsed, but removes the superfluous "edge" and "node" levels in the dict
```
#factsheets: A class for working with factsheets
```
-create(name*,fstype*,attributes,validateOnly)-creates a factsheet. Attributes is a dict with key/value pairs for attribs like "/alias":"Alias to add". validateOnly defaults to "false", but you can send a create to only test.
-update(fsid*,attributes*,comment*,validateOnly)
-delete(fsid*,comment*,validateOnly)
-deleteByNameAndType(name*,fstype*,comment*,validateOnly)
-getByContainsName(name*) - Returns multiple factsheets that conain the string in name
-getFactSheetByNameAndType(name*,fstype*) - returns a dict with Factsheet info by name and type - exact match only
-getIdByNameAndType(name*,fstype*) - returns a single id as a string from query
-getAllByType(fstype*) - returns all factsheets of a specific type
```

#users:  A class for working with users
```
getUsers:  Gets all users into a list
getUsersEmail:  Gets all users into a dict with a key of the user's e-mail address
getUserByEmail: Gets a single user based on e-mail
getUsersID:  Gets all users into a dict with a key of the user's Account ID (GUID)
getUserByID: Gets a single user by ID
setRole:  Sets a user's role by e-mail. Roles are ADMIN,MEMBER,VIEWER, and CONTACT

```
TODO:
------
LOTS!

Useage
------
```
from LeanIX import LeanIX  

lix = LeanIX(api_token=api_token,workspaceid=workspaceid,baseurl=baseurl)  

# There are three functions available to execute GraphQL against the LeanIX endpoint.   
raw = lix.graph.execGraphQL(<query>,<vars>)  # Returns the raw HTTP Response object for you to interpret  
parsed = lix.graph.execGraphQLParsed(<query>,<vars>) # Reads the response JSON and returns a dict  
trimmed = lix.graph.execGraphQLTrimmed(<query>,<vars>) # Takes the "parsed" output and remives the "edges" and "nodes" levesl from the dict  
```



