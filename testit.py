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

schema = lix.graph.get_schema()
fstypes = [
    'BusinessCapability',
    "Process",
    "UserGroup",
    "Project",
    "Application",
    "Interface",
    "DataObject",
    "ITComponent",
    "Provider"
    ,"TechnicalStack"
]

relationList = {""}
 
for t in fstypes:
    curt = schema[t.lower()]
    
    for f in curt['fields']:
        if f['name'].lower().startswith("rel") and not f['name'].startswith("release"):
            relationList.add(f['name'])

allrelations = list(relationList)

gql = """{
  allFactSheets(first: 15000) {
    edges {
      node {
        id
        type
        name
        ... on BusinessCapability {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relBusinessCapabilityToApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relBusinessCapabilityToProcess {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relBusinessCapabilityToProject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on Process {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProcessToApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProcessToBusinessCapability {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProcessToProject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on UserGroup {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relUserGroupToApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relUserGroupToITComponent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relUserGroupToProject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on Project {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProjectToApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProjectToUserGroup {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProjectToBusinessCapability {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProjectToITComponent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProjectToProcess {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProjectToProvider {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on Application {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relApplicationToUserGroup {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relApplicationToDataObject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relApplicationToITComponent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relApplicationToProject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProviderApplicationToInterface {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relConsumerApplicationToInterface {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relApplicationToProcess {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relApplicationToBusinessCapability {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on Interface {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relInterfaceToProviderApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relInterfaceToConsumerApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relInterfaceToDataObject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relInterfaceToITComponent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on DataObject {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relDataObjectToApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relDataObjectToInterface {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on ITComponent {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relITComponentToApplication {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relITComponentToTechnologyStack {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relITComponentToUserGroup {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relITComponentToProvider {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relITComponentToInterface {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relITComponentToProject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on Provider {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProviderToITComponent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relProviderToProject {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
        ... on TechnicalStack {
          relToParent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToChild {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequires {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToRequiredBy {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToSuccessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relToPredecessor {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
          relTechnologyStackToITComponent {
            edges {
              node {
                id
                type
                factSheet {
                  id
                  type
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}
"""


results = lix.graph.execGraphQLTrimmed(gql)
relationlist = []
for fs in results['data']['allFactSheets']:
    for r in allrelations:
        if currel := fs.get(r,None):
            for rel in currel:
                currelation = {
                    "type": rel['type'],
                    "source":fs['id'],
                    "dest":rel['factSheet']['id']
                }
                relationlist.append(currelation)

aaa=1


aa=1