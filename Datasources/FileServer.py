import logging
import json
import os
from pathlib import Path
from datetime import date, datetime
from ..LibFrame import applicationDict
from smb.SMBConnection import SMBConnection
from ..Objects.ScalarFile import ScalarFile
from ..Objects.NonScalarFile import NonScalarFile
import tempfile
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import socket


class FileServer(object):

    def __init__(self):
        #logging.getLogger("SMBConnection").setLevel(logging.ERROR)
        self.config=applicationDict['config']['smbshare']
        self.clientname = socket.gethostname()
        logging.debug(self.clientname)
        
    def getServerConnection(self):
        conn = SMBConnection(self.config['shareuser'],self.config['sharepwd'],self.clientname,self.config['server_name'],"WORKGROUP") 
        return conn

    def initFileShare(self):
        try:
            dire = os.path.dirname(__file__)
            filename= os.path.join(dire, '../config/fileserver.json')
            fp=open(filename,"r")
            self.subdirs=json.load(fp)
            fp.close()
        except:
            logging.error("could not load subdirs")
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            subdirs=["Projects"]
            for subdir in subdirs:
                newdir="{0}/{1}".format(self.config['rootdir'],subdir)
                self.checkNCreate(conn,newdir)
            conn.close()
        except Exception as e:
            logging.error(str(e))
    
    #store project data
    def checkProject(self,projectid):
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            #conn.createDirectory(self.config['sharename'],"CMSData/Projects/{0}".format(projectid))
            subdirs=["reports","configuration","data","data/scalar","data/twf","data/spectra","plots","plots/scalar","plots/nonscalar","reports/status"]
            newdir="CMSData/Projects/{0}".format(projectid)
            self.checkNCreate(conn,newdir)
            for subdir in self.subdirs['subdirs']:
                newdir="CMSData/Projects/{0}/{1}".format(projectid,subdir)
                self.checkNCreate(conn,newdir)
            conn.close()
        except Exception as e:
            logging.error(str(e))
    '''
    def storeScalarData(self,projectid,datestr,sourcefilelink):
        p = Path(sourcefilelink)
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            scalardir="CMSData/Projects/{0}/data/scalar/{1}".format(projectid,datestr)
            self.checkNCreate(conn,scalardir)
            path=scalardir+"/"+p.name
            with open(p, 'rb') as file_obj:
                conn.storeFile(service_name=self.config['sharename'],  # It's the name of shared folder
                        path=path,
                        file_obj=file_obj)
            
            conn.close()
        except Exception as e:
            logging.error(str(e))
    '''
    def storeScalarData(self,projectid,resultfiles):
        
        #p = Path(sourcefilelink)
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            for datestr,filelist in resultfiles.items():
                scalardir="CMSData/Projects/{0}/data/scalar/{1}".format(projectid,datestr)
                self.checkNCreate(conn,scalardir)
                for sourcefile in filelist:
                    p = Path(sourcefile['filelink'])
                    path=scalardir+"/"+p.name
                    with open(p, 'rb') as file_obj:
                        conn.storeFile(service_name=self.config['sharename'],  # It's the name of shared folder
                                path=path,
                                file_obj=file_obj)
                    result=ScalarFile(scalarfile_name = p.name,
                                        scalarfile_type = sourcefile['scalarfile_type'],
                                        scalarfile_project_id=sourcefile['scalarfile_project_id'],
                                        scalarfile_system_id=sourcefile['scalarfile_system_id'],
                                        scalarfile_signal_id=sourcefile['scalarfile_signal_id'],
                                        scalarfile_link = str(path),
                                        scalarfile_no_meas = sourcefile['scalarfile_no_meas'],
                                        scalarfile_size = sourcefile['scalarfile_size'],
                                        scalarfile_year = sourcefile['scalarfile_year'],
                                        scalarfile_month = sourcefile['scalarfile_month'],
                                        scalarfile_day=sourcefile['scalarfile_day'] )
                    applicationDict["dbconn"].upsertScalarFiles(result)
                    os.remove(p)
            conn.close()
        except Exception as e:
            logging.error(str(e))
    
    def storeNonScalarData(self,projectid,result):
        
        #p = Path(sourcefilelink)
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            datestr="{0}-{1}-{2}".format(result['year'],result['month'],result['day'])
            scalardir="CMSData/Projects/{0}/data/{2}/{1}".format(projectid,datestr,result['basedir'])
            self.checkNCreate(conn,scalardir)
            
            p = Path(result['filelink'])
            path=scalardir+"/"+p.name
            with open(p, 'rb') as file_obj:
                    conn.storeFile(service_name=self.config['sharename'],  # It's the name of shared folder
                                path=path,
                                file_obj=file_obj)
            storageresult=NonScalarFile(nonscalarfile_name = p.name,
                                    nonscalarfile_type = result['type'],
                                    nonscalarfile_project_id=result['project_id'],
                                    nonscalarfile_system_id=result['system_id'],
                                    nonscalarfile_signal_id=result['signal_id'],
                                    nonscalarfile_link = path,
                                    nonscalarfile_size = result['size'],
                                    nonscalarfile_channel = result['channel'],
                                    nonscalarfile_channelname = result['channelname'],
                                    nonscalarfile_speed =result['speed'],
                                    nonscalarfile_speedunit = result['speedunit'],
                                    nonscalarfile_RPM_Avg =result['RPM_Avg'],
                                    nonscalarfile_RPM_Max = result['RPM_Max'],
                                    nonscalarfile_RPM_Min = result['RPM_Min'],
                                    nonscalarfile_year = result['year'],
                                    nonscalarfile_month = int(result['month']),
                                    nonscalarfile_day= int(result['day']),
                                    nonscalarfile_hour = int(result['hour']),
                                    nonscalarfile_minute = int(result['minute']),
                                    nonscalarfile_timestamp=result['timestamp'])
            applicationDict["dbconn"].upsertNonScalarFiles(storageresult)
            os.remove(p)
            conn.close()
        except Exception as e:
            logging.error(str(e))



    def storeBKVTemplate(self,application,filelink):
        p = Path(filelink)
        outputpath=""
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            newdir="CMSData/BKVModels".format()
            self.checkNCreate(conn,newdir)
            newdir="CMSData/BKVModels/{0}".format(application)
            self.checkNCreate(conn,newdir)
            file_obj=open(filelink,"r")
            templatedata=json.load(file_obj)
            file_obj.close()
            template_id=templatedata["heading"][0]["template_id"]
            logging.debug("templat id: "+str(template_id))
            newdir="CMSData/BKVModels/{0}/{1}".format(application,template_id)
            self.checkNCreate(conn,newdir)
            
            path=newdir+"/"+p.name
            with open(p, 'rb') as file_obj:
                conn.storeFile(service_name=self.config['sharename'],  # It's the name of shared folder
                        path=path,
                        file_obj=file_obj)
            
            conn.close()
            outputpath=path

        except Exception as e:
            logging.error(str(e))
        return outputpath

    def checkNCreate(self,conn,sourcedir):
        temp=str(sourcedir).split("/")
        subdir=temp[-1]
        temp.pop()
        parentdir="/".join(temp)
        print("checking: "+parentdir)
        sharedfiles = conn.listPath(self.config['sharename'], parentdir)
        makeit=True
        for sharedfile in sharedfiles:
            if sharedfile.isDirectory and sharedfile.filename==subdir:
                print("found it")
                makeit=False
        if makeit:
            newdir=parentdir+"/"+subdir
            conn.createDirectory(self.config['sharename'],newdir)

    def getScalarDataframe(self,link):
        conn = self.getServerConnection()
        conn.connect(self.config['server_ip'],445)
        file_obj = tempfile.NamedTemporaryFile()
        file_attributes, filesize = conn.retrieveFile(self.config['sharename'], link, file_obj)
        dt=pd.read_parquet(file_obj)
        file_obj.close()
        conn.close()
        return dt
    
    def getNonScalarData(self,link):
        conn = self.getServerConnection()
        conn.connect(self.config['server_ip'],445)
        file_obj = tempfile.NamedTemporaryFile()
        file_attributes, filesize = conn.retrieveFile(self.config['sharename'], link, file_obj)
        #print(filesize)
        file_obj.seek(0, 0)
        data=json.load(file_obj)
        file_obj.close()
        conn.close()
        
        return data



    