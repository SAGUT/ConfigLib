import logging
from ..LibFrame import applicationDict
import json
import requests
from requests.auth import HTTPBasicAuth
import time
import urllib.parse
from ..Objects.SPM.SPMCondmasterServer import SPMCondmasterMP
class SPMAPI(object):
    '''
    classdocs
    '''


    def __init__(self, spmserver):
        '''
        Constructor
        '''
        self.spmserver = spmserver
        self.baseurl="http://{0}:{1}/api/".format(self.spmserver.spmcondmaster_address,self.spmserver.spmcondmaster_port)
        self.pagesize=200
        self.token=None
        self.timeout=0
        self.defaultversion="v1/"

    def getMeasurementPoints(self,database):
        #start=time.time()
        measurementpoints=dict()
        
        try:
            url=self.baseurl+self.defaultversion+"databases/{0}/measuringpoints".format(database)
            #print(url)
            
            jsonresult = requests.get(url, auth=HTTPBasicAuth(self.spmserver.spmcondmaster_user, self.spmserver.spmcondmaster_pwd)).json()
            #print(jsonresult)
            for objecte in jsonresult['values']:
                #print(objecte)
                measurementpoints[objecte["Number"]]=SPMCondmasterMP(spmcondmastermp_server = self.spmserver.spmcondmaster_id,
                                                                    spmcondmastermp_number = objecte["Number"],
                                                                    spmcondmastermp_intno = objecte["IntNo"],
                                                                    spmcondmastermp_name = objecte["Name"],
                                                                    spmcondmastermp_assignment="{}")
                               
                
        except Exception as e:
            logging.error("getMeasurementPoints",str(e))
                
        return measurementpoints

    def getAssignments(self,database,mp):
        #start=time.time()
        assignments=None
        
        try:
            url=self.baseurl+self.defaultversion+"databases/{0}/measuringpoints/{1}/assignments".format(database,mp.spmcondmastermp_number)
            #print(url)
            
            jsonresult = requests.get(url, auth=HTTPBasicAuth(self.spmserver.spmcondmaster_user, self.spmserver.spmcondmaster_pwd)).json()
            #print(jsonresult)
            assignments= jsonresult
                               
                
        except Exception as e:
            logging.error("getAssignments",str(e))
                
        return assignments
