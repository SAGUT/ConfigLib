from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float,BigInteger
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class NonScalarFile(Base):
    __tablename__ = 'tab_non_scalarfiles'

    # Every SQLAlchemy table should have a primary key named 'id'
    nonscalarfile_id = Column(Integer, primary_key=True)
    nonscalarfile_name = Column(String(255))
    nonscalarfile_type = Column(String(255))
    nonscalarfile_project_id=Column(Integer,ForeignKey('tab_project.project_id'))
    nonscalarfile_system_id=Column(Integer,ForeignKey('tab_system.system_id'))
    nonscalarfile_signal_id=Column(Integer,ForeignKey('tab_calculated_signal.signal_id'), index=True)
    nonscalarfile_channel = Column(String(255))
    nonscalarfile_channelname = Column(String(255))
    nonscalarfile_link = Column(Text)
    nonscalarfile_size = Column(Integer)
    nonscalarfile_speed = Column(Float)
    nonscalarfile_speedunit = Column(String(255))
    nonscalarfile_RPM_Avg = Column(Float)
    nonscalarfile_RPM_Max = Column(Float)
    nonscalarfile_RPM_Min = Column(Float)
    nonscalarfile_year = Column(Integer, index=True)
    nonscalarfile_month = Column(Integer, index=True)
    nonscalarfile_day = Column(Integer, index=True)
    nonscalarfile_hour = Column(Integer, index=True)
    nonscalarfile_minute = Column(Integer, index=True)
    nonscalarfile_timestamp = Column(BigInteger, index=True)
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<NonScalarFile(nonscalarfile_name='%s', nonscalarfile_type='%s', nonscalarfile_signal_id'%s')>" % (
                               self.nonscalarfile_name, self.nonscalarfile_type, self.nonscalarfile_signal_id)
