from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ...Database import Base

# Our User object, mapped to the 'users' table
class FieldAgent(Base):
    __tablename__ = 'tab_fieldagent'

    # Every SQLAlchemy table should have a primary key named 'id'
    fa_id = Column(Integer, primary_key=True)
    fa_project_id= Column(Integer, ForeignKey('tab_project.project_id'))
    fa_azureid = Column(String(255))
    fa_name = Column(String(255))
    fa_model = Column(String(255))
    fa_description = Column(String(32))
    fa_serialNo = Column(Text)
    fa_oS= Column(String(255))
    fa_config= Column(String(255))
    fa_web= Column(String(255))
    fa_base= Column(String(255))

    modules = relationship("FieldAgentModule", back_populates="fa")
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<FieldAgent(fa_project_id='%s', fa_name='%s', fa_model'%s')>" % (
                               self.fa_project_id, self.fa_name, self.fa_model)

class FieldAgentModule(Base):
    __tablename__ = 'tab_fieldagent_module'

    # Every SQLAlchemy table should have a primary key named 'id'
    fa_module_id = Column(Integer, primary_key=True)
    fa_module_fa_id = Column(Integer,ForeignKey('tab_fieldagent.fa_id'))
    fa_module_system_id = Column(Integer,ForeignKey('tab_system.system_id'),nullable=True)
    fa_module_azureid = Column(String(255))
    fa_module_type = Column(String(255))
    fa_module_name = Column(String(255))
    fieldagent = relationship("FieldAgent", back_populates="modules")
    versions = relationship("FieldAgentModuleVersion", back_populates="module")
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<FieldAgentModule(fa_module_fa_id='%s', fa_module_name='%s')>" % ( self.fa_module_fa_id, self.fa_module_name)

class FieldAgentModuleVersion(Base):
    __tablename__ = 'tab_fieldagent_module_versions'

    # Every SQLAlchemy table should have a primary key named 'id'
    fa_module_version_id = Column(Integer, primary_key=True)
    fa_module_version_module_id = Column(Integer,ForeignKey('tab_fieldagent_module.fa_module_id'))
    fa_module_version_tag = Column(String(255))
    fa_module_version_timestamp = Column(String(255))
    fa_module = relationship("FieldAgentModule", back_populates="versions")
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<FieldAgentModuleVersion(fa_module_version_timestamp='%s', fa_module_version_tag='%s')>" % ( self.fa_module_version_timestamp, self.fa_module_version_tag)