import logging
import json
import os
from pathlib import Path
from datetime import date, datetime
from ..LibFrame import applicationDict
from smb.SMBConnection import SMBConnection
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
    def createNewProject(self,projectid):
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

    def storeScalarData(self,projectid,datestr,sourcefilelink):
        try:
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            scalardir="CMSData/Projects/{0}/data/scalar/{1}".format(projectid,datestr)
            self.checkNCreate(conn,scalardir)

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

               



    