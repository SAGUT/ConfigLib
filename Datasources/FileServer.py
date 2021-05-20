import logging
import json
import os
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
        conn = SMBConnection(self.config['shareuser'],self.config['sharepwd'],self.clientname,self.config['server_name'],self.config['domain']) 
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

               



    