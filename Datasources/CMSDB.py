import logging
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from ..LibFrame import applicationDict
from ..Database import Base,engine,db_session
from ..Objects.ProjectObject import Project
from ..Objects.CMSSystem import CMSSytem
from ..Objects.BKV.DDAU3 import DDAU3

class CMSDB(object):

    def __init__(self):
        self.config=applicationDict['config']['dbsetup']
        #self._getEngine()
        self._initDB()
        self.test()

    def test(self):
        project=Project(project_name = "SmartKiln",
         project_site = "Indocement",
          project_country = "Indonesia",project_description="Dies ist")
        db_session.add(project)
        db_session.commit()

    def _initDB(self):
        
        Base.metadata.create_all(engine) 
        #Base.metadata.bind = self.engine
        Base.query = db_session.query_property()

    def _getEngine(self):
        if self.config['type']=="mariadb":
            logging.debug("_getEngine mariadb")
            link="mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4".format(self.config['user'],
                                                                                        self.config['pwd'],
                                                                                        self.config['server'],
                                                                                        self.config['port'],
                                                                                        self.config['database'])
            logging.debug(link)
            self.engine = create_engine(link, echo=True)
            self.db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.engine))

    #def insertNewProject(self,project):
