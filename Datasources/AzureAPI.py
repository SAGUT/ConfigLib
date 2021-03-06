import logging
from ..LibFrame import applicationDict
import json
import requests
import time
import urllib.parse
from ..Objects.SourceSignal import SourceSignal
import numpy as np
import pandas as pd
class AzureAPI(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.tenantid = params['tenantid']
        self.clientid = params['clientid']
        self.client_secret=params['client_secret']
        self.resourceid=params['resourceid']
        self.baseurl=params['baseurl']
        
        self.pagesize=200
        self.token=None
        self.timeout=0
        self.defaultversion="v1/"
        
    def getToken(self):
        now=time.time()
        if not self.token:
            logging.debug("no token, getting one")
            self.token=self.requestNewToken()
            #logger.debug(self.token)
            self.timeout=now+int(self.token['expires_in'])
            
        else:
            if now>self.timeout-600:
                logging.debug("getting new one")
                self.token=self.requestNewToken()
                self.timeout=now+int(self.token['expires_in'])
            
            
        return self.token['access_token']   
            
    def requestNewToken(self):
        logging.debug("requestNewToken")
        url = 'https://login.microsoftonline.com/'+self.tenantid+'/oauth2/token'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'cache-control':'no-cache'
        }
        
        secret=urllib.parse.quote(self.client_secret)
        resourceidurl=urllib.parse.quote(self.resourceid)
        resourceidurl=resourceidurl.replace('/','%2F')
        data = 'client_id='+self.clientid+'&client_secret='+secret+'&grant_type=client_credentials&resource='+resourceidurl#https%3A%2F%2Fflsiotdev.onmicrosoft.com%2F2ccbc5b1-8505-4d86-8f65-ef9beec89213'
        response = requests.post(url,  data=data, headers=headers)
    
        response.raise_for_status()
        token=response.json()
        
        return token

    def getSourceSignals(self,moduleid,systemdbid):
        #start=time.time()
        flsobjects=dict()
        levelstring=""
        page=1
        hasMore=True
        counter=1
        while(hasMore):
            try:
                
                url=self.baseurl+self.defaultversion+"sourcesignals?page={0}&pageSize={1}&parentId={2}".format(page,100,moduleid)
                #print(url)
                access_token=self.getToken()
                headers = {'Authorization': 'Bearer ' + access_token}
                jsonresult = requests.get(url, headers=headers).json()
                #print(jsonresult)
                if 'totalCount' in jsonresult:
                    
                    totalcount=jsonresult['totalCount']
                    if counter<=totalcount:
                        print("reached max count:",counter,totalcount)
                        hasMore=True
                    
                        for objecte in jsonresult['sourceSignals']:
                            
                            flsobjects[objecte["id"]]=SourceSignal(
                                                            sourcesignal_azureid= objecte['id'],
                                                            sourcesignal_name= objecte['name'],
                                                            sourcesignal_description= objecte['description'],
                                                            sourcesignal_type= objecte['type'],
                                                            sourcesignal_realTime= objecte['realTime'],
                                                            sourcesignal_measurementType= objecte['measurementType'],
                                                            sourcesignal_sourceUnit= objecte['sourceUnit'],
                                                            sourcesignal_sourceIdentifier= objecte['sourceIdentifier'],
                                                            sourcesignal_systemHigh= objecte['systemHigh'],
                                                            sourcesignal_systemLow= objecte['systemLow'],
                                                            sourcesignal_parentId= objecte['parentId'],
                                                            sourcesignal_designation= objecte['designation'],
                                                            sourcesignal_metadata= json.dumps(objecte['metadata']),
                                                            sourcesignal_channel= None,
                                                            sourcesignal_systemid=systemdbid
                                                            )
                            #print(counter,objecte,objecte["id"])
                            counter+=1
                    else:
                        hasMore=False
                
                page=page+1
                
                
                
            except Exception as e:
                print("getSourceSignals error",str(e))
                if page>1:
                    page=page-1
                else:
                    page=1
        return flsobjects

    def getCalclatedSignals(self,moduleid):
        #start=time.time()
        flsobjects=dict()
        levelstring=""
        page=1
        hasMore=True
        counter=1
        while(hasMore):
            try:
                
                url=self.baseurl+self.defaultversion+"calculatedSignals?page={0}&pageSize={1}&moduleId={2}".format(page,100,moduleid)
                #print(url)
                access_token=self.getToken()
                headers = {'Authorization': 'Bearer ' + access_token}
                jsonresult = requests.get(url, headers=headers).json()
                #print(jsonresult)
                if 'totalCount' in jsonresult:
                    
                    totalcount=jsonresult['totalCount']
                    if counter<=totalcount:
                        print("reached max count:",counter,totalcount)
                        hasMore=True
                    
                        for objecte in jsonresult['calculatedSignalResponses']:
                            
                            flsobjects[objecte["id"]]=objecte
                            
                            counter+=1
                    else:
                        hasMore=False
                
                page=page+1
                
                
                
            except Exception as e:
                print("getCalclatedSignals error",str(e))
                if page>1:
                    page=page-1
                else:
                    page=1
        return flsobjects
    
    def getNonScalarEvents(self,azureid,starttime,page,pageSize=20):
        #start=time.time()
        flsobjects=[]
        
        try:
                
            url=self.baseurl+self.defaultversion+"events?page={0}&pageSize={1}&assetId={2}&orderBy=TIMESTAMP_ASC&since={3}".format(page,pageSize,azureid,starttime)
            #print(url)
            access_token=self.getToken()
            headers = {'Authorization': 'Bearer ' + access_token}
            jsonresult = requests.get(url, headers=headers).json()
            #print(jsonresult)
            if 'totalCount' in jsonresult:
                totalPages=jsonresult['totalPages']
                totalcount=jsonresult['totalCount']
                for objecte in jsonresult['events']:
                            
                    flsobjects.append(objecte)
                       
                
                
                
        except Exception as e:
            print("getNonScalarEvents error",str(e))
                
        return flsobjects,totalcount,totalPages

    def getNonScalarConfig(self,signalid):
        #start=time.time()
        flsobjects=[]
       
        try:
                
            url=self.baseurl+self.defaultversion+"nonScalarCalculatedSignalConfig/{0}".format(signalid)
            #print(url)
            access_token=self.getToken()
            headers = {'Authorization': 'Bearer ' + access_token}
            jsonresult = requests.get(url, headers=headers).json()
            #print(jsonresult)
            flsobjects=jsonresult
                
                
                
        except Exception as e:
            print("getNonScalarConfig error",str(e))
                
        return flsobjects

    def searchSite(self,searchstr):
        #start=time.time()
        flsobjects=dict()
        levelstring=""
        page=1
        hasMore=True
        counter=1
        while(hasMore):
            try:
                
                url=self.baseurl+self.defaultversion+"sites?page={0}&pageSize={1}&siteName={2}".format(page,100,searchstr)
                #print(url)
                access_token=self.getToken()
                headers = {'Authorization': 'Bearer ' + access_token}
                jsonresult = requests.get(url, headers=headers).json()
                #print(jsonresult)
                if 'totalCount' in jsonresult:
                    
                    totalcount=jsonresult['totalCount']
                    if counter<=totalcount:
                        print("reached max count:",counter,totalcount)
                        hasMore=True
                    
                        for objecte in jsonresult['values']:
                            
                            flsobjects[objecte["name"]]=objecte
                            
                            counter+=1
                    else:
                        hasMore=False
                
                page=page+1
                
                
                
            except Exception as e:
                print("searchSite error",str(e))
                if page>1:
                    page=page-1
                else:
                    page=1
        return flsobjects
    
    def getTimeseriesV2(self,signalid,starttime,endtime,includeBadQuality=False):
        access_token=self.getToken()
       
        incBadQ="false"
        if includeBadQuality:
            incBadQ="true"
        values=[]
        index=[]
        quality=[]
        try:
            headers = {'Authorization': 'Bearer ' + access_token}
            finalurl=self.baseurl+"v2/signals/{0}/timeseries?end={1}&includeBadQuality={2}&start={3}".format(signalid,endtime,incBadQ,starttime)
            response = requests.get(finalurl, headers=headers)
            jsonresult=response.json()
            counter=0
            if 'values' in jsonresult:
                print("no of values",len(jsonresult['values']))
                if len(jsonresult['values'])>0:
                    for object in jsonresult['values']:
                        #flsobjects[object["id"]]=object
                        lasttime=object['timestamp']
                        
                        if int(object['quality'])>0:
                            values.append(float(object['value']))
                            index.append(lasttime)
                            quality=object['quality']
                        else:
                            values.append(np.nan)
                            index.append(lasttime)
                            quality=object['quality']
            counter=len(values)
            qualityid=signalid+"_quality"
            dataframe=pd.DataFrame({'timestamps':index, signalid:values,qualityid:quality})
            dataframe['datetime']=pd.DatetimeIndex(pd.to_datetime(dataframe['timestamps'], unit='ms')).tz_localize('UTC' )
            dataframe=dataframe.set_index('datetime')
        except Exception as e:
            print("get getTimeseriesV2 error",str(e))
        
        return dataframe,counter
