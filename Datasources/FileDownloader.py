import logging
import json
import os
from pathlib import Path
from datetime import date, datetime
import urllib.request
from ..LibFrame import applicationDict

class FileDownloader(object):

    def __init__(self):
        self.tempdir=Path(applicationDict["config"]["filesystem"]["tempdir"]+"/nonscalar")
        self.tempdir.mkdir(parents=True, exist_ok=True)


    def  downloadFile(self,url,calcsignal):
        result={'status':False}
        try:
            with urllib.request.urlopen(url) as response:
                data = str(response.read().decode()).replace("'","\"")
                nonscalar=json.loads(data)
                start_timestamp=nonscalar['start_timestamp']
                dirdate=datetime.utcfromtimestamp(start_timestamp/1000).strftime('%Y_%m_%d')
                filedate=datetime.utcfromtimestamp(start_timestamp/1000).strftime('%Y_%m_%d_%H_%M')
                name=calcsignal.signal_name#nonscalar['name']
                channel=nonscalar['channel']
                channelname=nonscalar['channelname']
                #workaround for sorting
                if len(channelname)==3 and str(channelname).find("ch")==0:
                    channelname="ch{:02}".format(int(channelname[2]))

                filename=channelname+"_"+str(name).replace(".","_")+"_"+filedate+".json"
                target=self.tempdir / filename
                fp=open(target,"w")
                json.dump(nonscalar,fp)
                fp.close()
                if "spectrumtype" in nonscalar:
                    result['type']=nonscalar['spectrumtype']
                    result['basedir']="spectra"
                    result['datatype']="spectrum"
                elif "TWFtype" in nonscalar:
                    result['type']=nonscalar['TWFtype']
                    result['basedir']="twf"
                    result['datatype']="twf"
                result['name']=name
                result['filename']=filename
                result['filelink']=target
                result['channel']=channel
                result['channelname']=channelname
                result['unit']=nonscalar['unit']
                result['speed']=nonscalar['speed']
                result['speedunit']=nonscalar['speedunit']
                result['RPM_Avg']=nonscalar['RPM_Avg']
                result['RPM_Max']=nonscalar['RPM_Max']
                result['RPM_Min']=nonscalar['RPM_Min']
                result['size']=os.path.getsize(target)
                result['status']=True
        except Exception as e:
            logging.error(str(e))
        return result