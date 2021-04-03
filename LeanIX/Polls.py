import LeanIX
import requests
import datetime 
import dateutil.parser
import json
import uuid


class Polls:
    def __init__(self,lix):
        self.auth_header = lix._auth_header
        self.lix = lix

    def startPollRun(self,pollrun):
        apiendpoint = "services/poll/v2/pollRuns?type=LIVE"
        url = self.lix.baseurl+ apiendpoint

        pr = {}
        pr['additionalFactSheetCheckEnabled'] = True
        pr['endTime'] = None
        pr['id'] = str(uuid.uuid4())
        pr['legacyId'] = None

        pr['poll'] = pollrun['poll']
        pr['pollCopy'] = pollrun['pollCopy']
        pr['pollResultType'] = "PER_FACTSHEET"
        pr['pollRunType'] = "LIVE"
        pr['progress'] = None
        pr['sendChangeNotifications'] = True
        pr['users'] = None
        pr['status'] = 'STARTED'
        pr['startTime'] = datetime.datetime.utcnow().isoformat().split(".")[0]+"Z"
        

        pollrun['status'] = "STARTED"
        pollrun['startTime'] = datetime.datetime.utcnow().isoformat().split(".")[0]+"Z"
        pollrun['endTime'] = None
        #pollrun['id'] = None
        retstatus =  requests.post(url,headers=self.lix.header,data=json.dumps(pr))
        a=1

    
    def getPolls(self,query=None):
        apiendpoint = "services/poll/v2/polls"
        url = self.lix.baseurl+ apiendpoint

        if query:
            return requests.get(url,headers=self.lix.header,params={"q",query}).json()
        else:
            return requests.get(url,headers=self.lix.header).json()


    def getPollRuns(self,pollid):
        apiendpoint = f"services/poll/v2/polls/{pollid}/pollRuns"
        url = self.lix.baseurl+ apiendpoint
        return requests.get(url,headers=self.lix.header).json()        
        a=1

    def getPollRunReminders(self,pollrunid):
        apiendpoint = f"services/poll/v2/pollRuns/{pollrunid}/reminders"
        url = self.lix.baseurl+ apiendpoint        
        return requests.get(url,headers=self.lix.header).json()

    def endPollRun(self,pollrun):
        apiendpoint = f"services/poll/v2/pollRuns/{pollrun['id']}"
        url = self.lix.baseurl+ apiendpoint
        # updatedata = {
        #         "id": pollrunid,
        #         "endTime": datetime.datetime.utcnow().isoformat().split(".")[0]+"Z",
        #         "status": "FINISHED",
        #         "language": "en"

        # }
        pollrun['status'] = "FINISHED"
        pollrun['endTime'] = datetime.datetime.utcnow().isoformat().split(".")[0]+"Z"
        retstatus =  requests.put(url,headers=self.lix.header,data=json.dumps(pollrun))
        return retstatus

    def deletePollRun(self,pollrunid):
        apiendpoint = f"services/poll/v2/pollRuns/{pollrunid}"
        url = self.lix.baseurl+ apiendpoint
        updatedata = {
            "status": "FINISHED",
            "language": "en",
            "endTime": datetime.datetime.utcnow().isoformat().split(".")[0]+".000Z"
        }
        retstatus =  requests.delete(url,headers=self.lix.header)
        return retstatus
    def sendPollReminder(self,pollrun):
        apiendpoint = f"services/poll/v2/pollRuns/{pollrun['id']}/reminder"
        url = self.lix.baseurl+ apiendpoint

        pollreminder = {
            "pollRunId": pollrun['id'],
            "subject": f"[REMINDER] {pollrun['poll']['introductionSubject']}",
            "message": pollrun['poll']['introductionText']
        }

        retval =  requests.post(url=url,headers=self.lix.header,data=json.dumps(pollreminder))
        return retval
        aa=1


if __name__=="__main__":
    pass

