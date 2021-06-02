from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Boolean,Float
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class NonScalarConfig(Base):
    __tablename__ = 'tab_nonscalar_config'

    # Every SQLAlchemy table should have a primary key named 'id'
    scalarconfig_id = Column(Integer, primary_key=True)
    scalarconfig_signal_id = Column(Integer, ForeignKey('tab_calculated_signal.signal_id'))
    scalarconfig_system_id = Column(Integer, ForeignKey('tab_system.system_id'))
    scalarconfig_dbid = Column(Integer)
    scalarconfig_azureid = Column(String(255))
    scalarconfig_condmasterId = Column(String(255))
    scalarconfig_condmasterDb = Column(Integer, ForeignKey('tab_spm_condmaster_db.spmcondmasterdb_id'))
    scalarconfig_condmasterServer = Column(Integer, ForeignKey('tab_spm_condmaster.spmcondmaster_id'))
    scalarconfig_condmasterAssignment = Column(Integer, ForeignKey('tab_spm_condmaster_fftas.spmcondmasterfftas_id'))
    scalarconfig_enableScale = Column(Boolean)
    scalarconfig_scaleFactor = Column(Float)
    scalarconfig_type = Column(String(255))
    scalarconfig_signalType = Column(Integer)
    scalarconfig_signalDecimate = Column(Boolean)
    scalarconfig_signalEnvelope = Column(Boolean)
    scalarconfig_signalHpfilter = Column(Boolean)
    scalarconfig_signalRemovedc = Column(Boolean)
    scalarconfig_signalIntegrate = Column(Integer)
    scalarconfig_signalSampleratefactor = Column(Integer)
    scalarconfig_rpmType = Column(Integer)
    signal = relationship("CalculatedSignal", back_populates="assignements")
    
    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<NonScalarConfig(scalarconfig_signal_id='%s', scalarconfig_condmasterDb='%s', scalarconfig_condmasterId'%s')>" % (
                               self.scalarconfig_signal_id, self.scalarconfig_condmasterDb, self.scalarconfig_condmasterId)