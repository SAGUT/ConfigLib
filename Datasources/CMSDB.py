import logging
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.sql.expression import table
from ..LibFrame import applicationDict
from ..Database import Base,engine,db_session
from ..Objects.Project import Project
from ..Objects.System import System
from ..Objects.BKV.DDAU3 import DDAU3
from ..Objects.SPM.SPMSystems import SPMLarge
from ..Objects.Channel import Channel
from ..Objects.Signals import Signal,CalculatedSignal
from ..Objects.Sensor import Sensor,AccelerationSensor
from ..Objects.Mapping import Mapping
class CMSDB(object):

    def __init__(self):
        self.config=applicationDict['config']['dbsetup']
        #self._getEngine()
        self._initDB()
        

    def _initDB(self):
        
        Base.metadata.create_all(engine) 
        #Base.metadata.bind = self.engine
        Base.query = db_session.query_property()

    
    def initDBValues(self,initdict):
        for tablename,values in initdict.items():
            try:
                if tablename=="tab_mapping":
                    for entry in values:
                        mapping=Mapping(mapping_position =entry['mapping_position'] ,mapping_short =entry['mapping_short'] , mapping_long =entry['mapping_long'] , mapping_description=entry['mapping_description'])
                        db_session.add(mapping)
                    db_session.commit()
            except Exception as e:
                logging.error(str(e))


    #----------------------------------------------------
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

