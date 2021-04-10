import logging
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session,sessionmaker
from ..LibFrame import applicationDict
from ..Database import Base,engine,db_session
from ..Objects.Project import Project
from ..Objects.CMSSystem import CMSSytem
from ..Objects.BKV.DDAU3 import DDAU3

class CMSDB(object):

    def __init__(self):
        self.config=applicationDict['config']['dbsetup']
        #self._getEngine()
        self._initDB()
        

    def _initDB(self):
        
        Base.metadata.create_all(engine) 
        #Base.metadata.bind = self.engine
        Base.query = db_session.query_property()

    #project handling
    def addProject(self,project):
        db_session.add(project)
        db_session.commit()
        return project

    def getAllProjects(self):
        projects=db_session.query(Project).filter().order_by(text('project_country, project_site'))
        #projects = query_obj.order_by(Project.project_country)
        
        return projects
    


    #CMS handling
    def addCMSSystem(self,cmssystem):
        db_session.add(cmssystem)
        db_session.commit()
        return cmssystem

    #BKV handling

