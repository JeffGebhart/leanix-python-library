import LeanIX
import os

api_token = os.getenv("leanixapikey")
workspaceid = os.getenv("leanixworkspaceid")
baseurl = os.getenv("leanixurl")

lix = LeanIX.LeanIX(api_token=api_token,workspaceid=workspaceid,baseurl=baseurl)

u=lix.users.setPermission(email="jeff@gebhart.ca",role="ADMIN")
a=1