import logging
from ..LibFrame import applicationDict
import json
import requests
import time
import urllib.parse
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