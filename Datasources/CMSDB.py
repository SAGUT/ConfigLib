import json
import logging
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine,update
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.sql.expression import table
from ..LibFrame import applicationDict
from ..Database import Base,engine,db_session
from ..Objects.Project import Project
from ..Objects.System import System
from ..Objects.BKV.DDAU3 import DDAU3
from ..Objects.IoT.OPCServer import OPC
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
from ..Objects.IoT.FieldAgent import FieldAgent,FieldAgentModule,FieldAgentModuleVersion
from ..Objects.IoT.Hierarchy import Hierarchy
from ..Objects.ScalarFile import ScalarFile
from ..Objects.Reporting.ProjectReport import Report
from ..Objects.Reporting.ChannelReport import ChannelStatus
from ..Objects.Reporting.ChannelPlots import ChannelPlots
from ..Objects.NonScalarFile import NonScalarFile
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
    def addObject(self,ormobject):
        db_session.add(ormobject)
        db_session.commit()
        return ormobject

    def getReport(self,report_id):
        return Report.query.get(report_id)
    
    def getChannelsStatus(self,report_id):
        channelsstatus=db_session.query(ChannelStatus).filter(ChannelStatus.channel_status_report_id==report_id)
        return channelsstatus
    
    def getChannelPlots(self,report_id,channel_id):  
        querystr="channel_plot_report_id={0} and channel_plot_channel_id={1}".format(report_id,channel_id)
        ssignals=db_session.query(ChannelPlots).filter(text(querystr)).all()
        
        return ssignals 
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
    
    def getProjectByName(self,name):
        project=None
        logging.debug("query Project: "+name)
        exists = db_session.query(
                db_session.query(Project).filter_by(project_name= name).exists()
                ).scalar()
        if exists:
            print("found it")

            querystr="project_name='{0}'".format(name)
            project=db_session.query(Project).filter(text(querystr)).one()
        
        return project

    def getSystem(self,systemid):
        return System.query.get(systemid)
    
    def getSystemsByProjectID(self,projectid):
        systems=db_session.query(System).filter(System.system_project_id==projectid)
        return systems
    
    def getChannel(self,channelid):
        return Channel.query.get(channelid)
    
    def getDDAUChannelsBySystemID(self,systemid):
        channels=db_session.query(DDAU3Channel).filter(DDAU3Channel.channel_system_id==systemid)
        return channels

    #CMS handling
    def checkCMS(self,cmssystem):
        #querystr="system_project_id={0} and system_name='{1}'".format(cmssystem.system_project_id,cmssystem.system_name)
        exists = db_session.query(db_session.query(System).filter_by(system_project_id= cmssystem.system_project_id,system_name= cmssystem.system_name).exists()).scalar()
        print(exists,cmssystem.system_name,cmssystem.system_project_id)
        return exists

    def addCMSSystem(self,cmssystem):
        db_session.add(cmssystem)
        db_session.commit()
        return cmssystem

    def addDDAU3(self,ddau3):
        db_session.add(ddau3)
        db_session.commit()
        return ddau3

    
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
        exists = db_session.query(
                db_session.query(SourceSignal).filter_by(sourcesignal_azureid= azureid).exists()
                ).scalar()
        if exists:
            querystr="sourcesignal_azureid='{0}'".format(azureid)
            signal=db_session.query(SourceSignal).filter(text(querystr)).one()
        else:
            signal=None
        return signal
    
    def deleteSourceSignal(self,signalid):
        db_session.query(SourceSignal).filter(SourceSignal.sourcesignal_id==signalid).delete()
        db_session.commit()
    
    #calculatedsignal handling
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
    
    def getCalculatedSignals(self,systemid):
        ssignals=db_session.query(CalculatedSignal).filter(CalculatedSignal.signal_system_id==systemid)
        return ssignals 
    
    def getCalculatedSignalsBType(self,systemid,type):
        querystr="signal_system_id={0} and signal_signalType='{1}'".format(systemid,type)
        ssignals=db_session.query(CalculatedSignal).filter(text(querystr)).all()
        
        return ssignals 
    
    def getCalculatedSignal(self,signal_id):
        return CalculatedSignal.query.get(signal_id)
        
    
    def updateCalculatedSignalChannel(self,signalid,channelid):
        db_session.execute(update(CalculatedSignal).where(CalculatedSignal.signal_id ==signalid).values(signal_channel_id=channelid))
        db_session.commit()
    
    def getCalculatedSignalsByChannel(self,channel_id):  
        querystr="signal_channel_id={0}".format(channel_id)
        ssignals=db_session.query(CalculatedSignal).filter(text(querystr)).all()
        
        return ssignals 

    #BKV handling
    def addTemplate(self,template):
        db_session.add(template)
        db_session.commit()
        return template
    
    def addHierarchy(self,hierarchy):
        db_session.add(hierarchy)
        db_session.commit()
        return hierarchy

    def updateHierarchy(self,hierarchy):
        db_session.execute(update(Hierarchy).where(Hierarchy.hierarchy_id ==hierarchy.hierarchy_id).values(hierarchy_dbparent=hierarchy.hierarchy_dbparent))
        db_session.commit()

    def getDDAU3TemplateChannels(self,templateid):
        result=dict()
        channels=db_session.query(BKVChannel).filter(BKVChannel.bkvchannel_templateid==templateid)
        for channel in channels:
            result[channel.bkvchannel_idstr]=channel
        return result

    def getDDAU3ChannelsByBKVID(self,systemid):
        result=dict()
        channels=db_session.query(DDAU3Channel).filter(DDAU3Channel.channel_system_id==systemid)
        for channel in channels:
            result[channel.ddauchannel_bkvid]=channel
        return result
    
    def getDDAU3ChannelsByName(self,systemid):
        result=dict()
        channels=db_session.query(DDAU3Channel).filter(DDAU3Channel.channel_system_id==systemid)
        for channel in channels:
            result[channel.channel_name]=channel
        return result
    
    def addDDAU3Channel(self,ddau3channel):
        db_session.add(ddau3channel)
        db_session.commit()
        return ddau3channel
    
    #SPM handling
    def getSPMServerByID(self,ID):
        logging.debug("query getSPMServerByID: "+ID)
        querystr="spmcondmaster_id={0}".format(ID)
        server=db_session.query(SPMCondmasterServer).filter(text(querystr)).one()
        
        return server
    
    def addSPMAssignment(self,assignment):
        db_session.add(assignment)
        db_session.commit()
        return assignment
    '''
    def upsertSPMAssignment(self,assignment):
        querystr="spmcondmasterfftas_dbid={0} and spmcondmasterfftas_techid={1}".format(assignment.spmcondmasterfftas_dbid,assignment.spmspmcondmasterfftas_techidmastermp_intno)
        mp =  db_session.query(SPMCondmasterFFTAS).filter(text(querystr)).first()
        print(mp)
        
        if not mp is None:
            db_session.execute(update(ScalarFile).where(ScalarFile.scalarfile_id ==dbsig.scalarfile_id).values(
                scalarfile_size=scalarfile.scalarfile_size,
                scalarfile_link=scalarfile.scalarfile_link
                ))
        else:
            print("make it new")
            db_session.add(assignment)
            db_session.flush()
            
        db_session.commit()
    '''

    def getSPMServers(self):
        logging.debug("query getSPMServer")
        result=dict()
        #projects=db_session.query(Project).filter().order_by(text('project_country, project_site'))
        servers=db_session.query(SPMCondmasterServer).filter().all()
        for server in servers:
            result[server.spmcondmaster_name]=server
                
        return result

    def getSPMDatabaseByName(self,serverid,databasename):
        querystr="spmcondmasterdb_server={0} and spmcondmasterdb_name='{1}'".format(serverid,databasename)
        db=db_session.query(SPMCondmasterDB).filter(text(querystr)).first()
        return db


    def getSPMDatabases(self):
        logging.debug("query getSPMDatabases")
        result=dict()
        #projects=db_session.query(Project).filter().order_by(text('project_country, project_site'))
        dbs=db_session.query(SPMCondmasterDB).filter().all()
        for db in dbs:
            if not db.spmcondmasterdb_server in result:
                result[db.spmcondmasterdb_server]=dict()
            result[db.spmcondmasterdb_server][db.spmcondmasterdb_name]=db
                
        return result
    
    def getSPMFFTASSByechID(self,dbid,techid):
        logging.debug("query getSPMFFTASS")
        querystr="spmcondmasterfftas_dbid={0} and spmcondmasterfftas_techid='{1}'".format(dbid,techid)
        ass=db_session.query(SPMCondmasterFFTAS).filter(text(querystr)).first()
        return ass
                
        return result

    def upsertSPMMP(self,spmmp):
        #exists = db_session.query(exists().where(SourceSignal.sourcesignal_azureid == sourcesignal.sourcesignal_azureid)).scalar()
        querystr="spmcondmastermp_server={0} and spmcondmastermp_intno={1}".format(spmmp.spmcondmastermp_server,spmmp.spmcondmastermp_intno)
        mp =  db_session.query(SPMCondmasterMP).filter(text(querystr)).first()
        print(mp)
        
        if not mp is None:
            print("found it",mp.spmcondmastermp_id,mp.spmcondmastermp_name)
            mp.spmcondmastermp_name=spmmp.spmcondmastermp_name
            mp.spmcondmastermp_number=spmmp.spmcondmastermp_number
            db_session.flush()
            key=mp.spmcondmastermp_id
        else:
            print("make it new")
            db_session.add(spmmp)
            db_session.flush()
            key=spmmp.spmcondmastermp_id
        db_session.commit()
        return key

    def getUpdateAssignment(self,mp):
        logging.debug("query getUpdateAssignment ")
        print("id: ",mp.spmcondmastermp_id)
        dbmp=db_session.query(SPMCondmasterMP).filter(SPMCondmasterMP.spmcondmastermp_id==mp.spmcondmastermp_id).first()
        print(dbmp)
        dbmp.spmcondmastermp_assignment=mp.spmcondmastermp_assignment
        db_session.flush()
        db_session.commit()
        return dbmp

    #fileserver data
    def addScalarFile(self,scalarfile):
        '''
        exists = db_session.query(
                db_session.query(ScalarFile).filter_by(scalarfile_signal_id= scalarfile.scalarfile_signal_id,
                scalarfile_year= scalarfile.scalarfile_year,
                scalarfile_month= scalarfile.scalarfile_month,
                scalarfile_day= scalarfile.scalarfile_day).exists()
                ).scalar()
        '''
        dbsig=db_session.query(ScalarFile).filter_by(scalarfile_signal_id= scalarfile.scalarfile_signal_id,
                scalarfile_year= scalarfile.scalarfile_year,
                scalarfile_month= scalarfile.scalarfile_month,
                scalarfile_day= scalarfile.scalarfile_day).first()
        if not dbsig is None:
            print("found it")
            db_session.execute(update(ScalarFile).where(ScalarFile.scalarfile_id ==dbsig.scalarfile_id).values(
                scalarfile_size=scalarfile.scalarfile_size,
                scalarfile_no_meas=scalarfile.scalarfile_no_meas,
                scalarfile_link=scalarfile.scalarfile_link
                ))
        else:
            print("make it new")
            db_session.add(scalarfile)
        db_session.commit()
        return scalarfile
    
    def getNonScalarFileByDate(self,signal_id,year,month,day,hour):
        querystr="nonscalarfile_signal_id={0} \
        and nonscalarfile_year={1} \
        and nonscalarfile_month={2} \
        and nonscalarfile_day={3} \
        and nonscalarfile_hour={4}".format(signal_id,year,month,day,hour)
        return db_session.query(NonScalarFile).filter(text(querystr)).first()
        
        
    def upsertNonScalarFiles(self,nonscalfile):
        

        querystr="nonscalarfile_signal_id={0} and nonscalarfile_timestamp={1}".format(nonscalfile.nonscalarfile_signal_id,nonscalfile.nonscalarfile_timestamp)
        logging.debug(querystr)
        dbresult =  db_session.query(NonScalarFile).filter(text(querystr)).first()
        
        logging.debug(str(dbresult))
        
        if not dbresult is None:
            print("found it",dbresult.nonscalarfile_signal_id)
            
            dbresult.nonscalarfile_speed = nonscalfile.nonscalarfile_speed
            dbresult.nonscalarfile_RPM_Avg = nonscalfile.nonscalarfile_RPM_Avg
            dbresult.nonscalarfile_RPM_Max = nonscalfile.nonscalarfile_RPM_Max
            dbresult.nonscalarfile_RPM_Min =nonscalfile.nonscalarfile_RPM_Min
            db_session.flush()
            
        else:
            print("make it new")
            db_session.add(nonscalfile)
            db_session.flush()
            
        db_session.commit()

    def upsertScalarFiles(self,scalfile):
        

        querystr="scalarfile_signal_id={0} \
            and scalarfile_year={1} \
            and scalarfile_month={2} \
            and scalarfile_day={3}".format(scalfile.scalarfile_signal_id,scalfile.scalarfile_year,scalfile.scalarfile_month,scalfile.scalarfile_day)
        logging.debug(querystr)
        dbresult =  db_session.query(ScalarFile).filter(text(querystr)).first()
        
        logging.debug(str(dbresult))
        
        if not dbresult is None:
            print("found it",dbresult.scalarfile_signal_id)
            
            dbresult.scalarfile_size = scalfile.scalarfile_size
            dbresult.scalarfile_no_meas = scalfile.scalarfile_no_meas
            
            db_session.flush()
            
        else:
            print("make it new")
            db_session.add(scalfile)
            db_session.flush()
            
        db_session.commit()
        
    def getScalarFile(self,signal_id,year,month,day):
        querystr="scalarfile_signal_id={0} \
                    and scalarfile_year={1} \
                    and scalarfile_month={2}\
                    and scalarfile_day={3}".format(signal_id,year,month,day)
        logging.debug(querystr)
        dbresult =  db_session.query(ScalarFile).filter(text(querystr)).first()
        return dbresult
    
    def getScalarFilesByProject(self,project_id,year,month,day):
        querystr="scalarfile_project_id={0} \
                    and scalarfile_year={1} \
                    and scalarfile_month={2}\
                    and scalarfile_day={3}".format(project_id,year,month,day)
        logging.debug(querystr)
        dbresult =  db_session.query(ScalarFile).filter(text(querystr)).all()
        return dbresult
        
    def getNameMapping(self,mapping_short):
        try:
            querystr="mapping_short='{0}'".format(mapping_short)
            mapped=db_session.query(Mapping).filter(text(querystr)).one()
        except:
            logging.debug("not mapped: "+str(mapping_short))
            mapped=mapping_short
        return mapped 