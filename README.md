LeanIX Python Library
======================

Forked from leanix-public/leanix-python-library

Currently very basic functionality.

Useage
------

from LeanIX import LeanIX  

lix = LeanIX(api_token=api_token,workspaceid=workspaceid,baseurl=baseurl)  

There are three functions available to execute GraphQL against the LeanIX endpoint.   
raw = lix.graph.execGraphQL(<query>,<vars>)  # Returns the raw HTTP Response object for you to interpret  
parsed = lix.graph.execGraphQLParsed(<query>,<vars>) # Reads the response JSON and returns a dict  
trimmed = lix.graph.execGraphQLTrimmed(<query>,<vars>) # Takes the "parsed" output and remives the "edges" and "nodes" levesl from the dict  



