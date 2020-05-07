import requests
import json

class Users:
    def __init__(self, lix):
      self.lix = lix

    def getUsers(self,permissions=True,pagesize=100):
        """Returns a list of user all objects"""
        
        if permissions:

            method=f"services/mtm/v1/workspaces/{self.lix.workspaceid}/permissions"
        else:
            method=f"services/mtm/v1/workspaces/{self.lix.workspaceid}/users"
        header=self.lix.header
        parameters = {
            "size":100,
            "page":1
        }
        

        return self.lix._sendrequest(method,parameters)

    def getUsersEmail(self,permissions=True,pagesize=100):
        """ Returns all users as a dict with the e-mail address as the key """
        if permissions:
            return {u['user']['email'].lower():u for u in self.getUsers(permissions,pagesize)}
        else:
            return {u['email'].lower():u for u in self.getUsers(permissions,pagesize)}

    def getUserByEmail(self,email,permissions=True,pagesize=100):
        """ Returns user based on email """
        if permissions:
            return {u['user']['email'].lower():u for u in self.getUsers(permissions,pagesize)}.get(email.lower(),None)
        else:
            return {u['email'].lower():u for u in self.getUsers(permissions,pagesize)}.get(email.lower(),None)
        
    def getUsersID(self,permissions=True,pagesize=100):
        """ Returns all users as a dict with the accountID address as the key """
        return {u['id'].lower():u for u in self.getUsers(permissions,pagesize)}

    def getUserByID(self,id,permissions=True,pagesize=100):
        """ Returns user based on accountID """
        return {u['id'].lower():u for u in self.getUsers(permissions,pagesize)}.get(id.lower(),None)
    
    def setRole(self,email,role="MEMBER"):
        """ Sets the permission level for the user identified by email to the role requested"""

        perms = self.getUsersEmail(permissions=True).get(email.lower())
        perms['user']['role'] = role

        perm = {
                    "id":perms['id'],
                    "workspace":{
                        "id":perms['workspace']['id']
                    },
                    "role":role,
                    "user":{
                        "id":perms['user']['id']
                    },
                    "status":perms['status']
                    }

        return self.lix._sendrequest(
                                    method=f'services/mtm/v1/permissions',
                                    data=perm,

                                    verb="post"
                                ).json()

    def addMember(self,email,given,surname,role="CONTACT"):
        """" Adds a new member to the workspace """

        # TODO

