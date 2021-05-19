from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,UniqueConstraint,Float,Boolean
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class SourceSignal(Base):
    __tablename__ = 'tab_source_signal'
    sourcesignal_id= Column(Integer, primary_key=True)
    sourcesignal_azureid= Column(String(255))
    sourcesignal_name= Column(String(255))
    sourcesignal_description= Column(String(255))
    sourcesignal_type= Column(String(255))
    sourcesignal_realTime= Column(Boolean)
    sourcesignal_measurementType= Column(String(255))
    sourcesignal_sourceUnit= Column(String(255))
    sourcesignal_sourceIdentifier= Column(String(255))
    sourcesignal_systemHigh= Column(Float)
    sourcesignal_systemLow= Column(Float)
    sourcesignal_parentId= Column(String(255))
    sourcesignal_designation= Column(Text)
    sourcesignal_metadata= Column(Text)
    sourcesignal_channel= Column(String(255))
    sourcesignal_systemid= Column(Integer, ForeignKey('tab_system.system_id'))
    # Lets us print out an object conveniently.
    def __repr__(self):
       return "<SourceSignal(sourceignal_azureid='%s', sourceignal_name='%s', sourceignal_description'%s')>" % (
                               self.sourceignal_azureid, self.sourceignal_name, self.sourceignal_description)