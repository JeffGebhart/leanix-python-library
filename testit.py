import LeanIX
import os
import json
import uuid

api_token = os.getenv("leanixapikey")
workspaceid = os.getenv("leanixworkspaceid")
baseurl = os.getenv("leanixurl")

lix = LeanIX.LeanIX(api_token=api_token,workspaceid=workspaceid,baseurl=baseurl)

allitc = lix.factsheets.getAllByType("ITComponent")
someitc = lix.factsheets.getByContainsName("a")
a=1