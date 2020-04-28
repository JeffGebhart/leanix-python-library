import LeanIX
import os

api_token = os.getenv("leanixapikey")
workspaceid = os.getenv("leanixworkspaceid")
baseurl = os.getenv("leanixurl")

lix = LeanIX.LeanIX(api_token=api_token,workspaceid=workspaceid,baseurl=baseurl)

gql = """
{
 allFactSheets(first:100)
  {
    totalCount
    edges {
      node {
        id
        type
        category
        name
        displayName
        fullName
        description
      }
    }
  }
}"""

fsid = lix.factsheets.getIdByNameAndType(name="Test Process",fstype="Process")

result = lix.factsheets.update(fsid=fsid,comment="TestUpdate",attributes={"/alias":{"value":"TestAlias"}},validateOnly=False)
fs = lix.factsheets.getFactSheetByNameAndType(name="Test Process",fstype="Process")
a=1

