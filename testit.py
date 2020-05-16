import LeanIX
import os
import json
import uuid

api_token = os.getenv("leanixapikey")
workspaceid = os.getenv("leanixworkspaceid")
baseurl = os.getenv("leanixurl")

with open("C:/Users/gebjef/Documents/Py/leanix-python-library/appranking.json","r") as f:
    appranking = json.load(f)['runsurveys_forcerankapp']



lix = LeanIX.LeanIX(api_token=api_token,workspaceid=workspaceid,baseurl=baseurl)

prov = lix.factsheets.providers

ea = prov.getByName("LeanIX")


aa=1