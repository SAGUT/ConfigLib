import logging
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
            conn = self.getServerConnection()
            conn.connect(self.config['server_ip'],445)
            sharedfiles = conn.listPath(self.config['sharename'], self.config['rootdir'])
            for sharedfile in sharedfiles:
                if sharedfile.isDirectory and not sharedfile.filename in [".",".."]:
                    print(sharedfile.filename)
            conn.close()
        except Exception as e:
            logging.error(str(e))

    



    