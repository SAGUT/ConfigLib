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
from ..Objects.Channel import Channel,DDAU3Channel
from ..Objects.Signals import CalculatedSignal
from ..Objects.Sensor import Sensor,AccelerationSensor
from ..Objects.Mapping import Mapping
from ..Objects.SourceSignal import SourceSignal
from ..Objects.NonScalarConfig import NonScalarConfig
from ..Objects.SPM.SPMCondmasterServer import SPMCondmasterServer,SPMCondmasterDB,SPMCondmasterMP,SPMCondmasterFFTAS
from ..Objects.BKV.BKVTemplate import BKVTemplate
from ..Objects.BKV.BKVChannel import BKVChannel
from ..Objects.BKV.BKVPush import BKVPush
from ..Objects.BKV.BKVRegister import BKVRegister

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
    
    def getProject(self,projectid):
        return Project.query.get(projectid)

    def getSystem(self,systemid):
        return System.query.get(systemid)

    #CMS handling
    def addCMSSystem(self,cmssystem):
        db_session.add(cmssystem)
        db_session.commit()
        return cmssystem
    #sourcesignal handling
    def upsertSourceSignal(self,sourcesignal):
        #exists = db_session.query(exists().where(SourceSignal.sourcesignal_azureid == sourcesignal.sourcesignal_azureid)).scalar()
        exists = db_session.query(
                db_session.query(SourceSignal).filter_by(sourcesignal_azureid= sourcesignal.sourcesignal_azureid).exists()
                ).scalar()
        if exists:
            print("found it")
        else:
            print("make it new")
            db_session.add(sourcesignal)
        db_session.commit()
    
    def getSourceSignal(self,systemid):
        ssignals=db_session.query(SourceSignal).filter(SourceSignal.sourcesignal_systemid==systemid)
        return ssignals 
    
    def getSourceSignalByAzureID(self,azureid):
        logging.debug("query Sourcesignal: "+azureid)
        querystr="sourcesignal_azureid='{0}'".format(azureid)
        signal=db_session.query(SourceSignal).filter(text(querystr)).one()
        
        return signal
    
    def deleteSourceSignal(self,signalid):
        db_session.query(SourceSignal).filter(SourceSignal.sourcesignal_id==signalid).delete()
        db_session.commit()
    
    #sourcesignal handling
    def upsertCalculatedSignal(self,calcsignal):
        #exists = db_session.query(exists().where(SourceSignal.sourcesignal_azureid == sourcesignal.sourcesignal_azureid)).scalar()
        exists = db_session.query(
                db_session.query(CalculatedSignal).filter_by(signal_azureid= calcsignal.signal_azureid).exists()
                ).scalar()
        if exists:
            print("found it")
        else:
            print("make it new")
            db_session.add(calcsignal)
        db_session.commit()
    
    #BKV handling
    def addTemplate(self,template):
        db_session.add(template)
        db_session.commit()
        return template
