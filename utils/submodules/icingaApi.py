import requests
from requests.auth import HTTPDigestAuth
import glob
import os

class IcingaApi:
    connection = {"baseUrl": "https://:5665/v1", "user": "", "password":''}

    def __init__(self, baseUrl=connection["baseUrl"], user=connection["user"], password=connection["password"]):
        self.URL      = baseUrl
        self.HEADERS  = {
            'content-type' : 'application/json',
            'Accept':        'application/json'
        }
        self.AUTH=(user, password)
    
    def call(self, call="get", url='', verify=False):
        url = self.URL + url
        response = getattr(requests, call)(url, headers=self.HEADERS, auth=self.AUTH, verify=False)
        return response.json()

    # Takes: a directory location of a package.
    # Does:  Searches for all ..*conf files in the dir, and puts them into a hash. The newlines must be removed from the content.
    def uploadPackage(self, directory=''):
        fileList = glob.glob(directory+"/*conf")
        data = {}
        for filePath in fileList:
            with open(filePath, 'r') as f:
                data["files."+filePath] = f.read().replace('\n','')

        return fileList
            



i = IcingaApi()
fnret = i.uploadPackage(directory="package-test")
print(fnret)