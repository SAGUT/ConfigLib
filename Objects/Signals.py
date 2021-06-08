from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class CalculatedSignal(Base):
    __tablename__ = 'tab_calculated_signal'

    # Every SQLAlchemy table should have a primary key named 'id'
    signal_id = Column(Integer, primary_key=True)
    signal_system_id = Column(Integer, ForeignKey('tab_system.system_id'))
    signal_sourcename = Column(String(255))
    signal_source_id = Column(Integer)
    signal_name = Column(String(255))
    signal_signalType = Column(String(255))
    signal_channel_id = Column(Integer, ForeignKey('tab_channel.channel_id'),nullable=True)
    signal_description = Column(Text)
    signal_azureid= Column(String(255))
    signal_moduleId= Column(String(255))
    signal_parentAssetId= Column(String(255))
    signal_calculationType= Column(String(255))
    signal_measurementUnit= Column(String(255))
    signal_measurementType= Column(String(255))
    signal_calculation= Column(Text)
    signal_inputSignals= Column(String(255))
    signal_label= Column(String(255))
    signal_designation= Column(String(255))
    signal_dataGroup= Column(String(255))
    signal_metadata= Column(Text)
    signal_environment= Column(String(255))
    signal_speedsignal= Column(Integer, ForeignKey('tab_calculated_signal.signal_id'),nullable=True)
    assignements = relationship("NonScalarConfig", back_populates="signal")

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<CalculatedSignal(signal_name='%s', signal_signalType='%s', signal_description'%s')>" % (self.signal_name, self.signal_signalType, self.signal_description)
