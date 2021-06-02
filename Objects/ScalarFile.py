from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class ScalarFile(Base):
    __tablename__ = 'tab_scalarfiles'

    # Every SQLAlchemy table should have a primary key named 'id'
    scalarfile_id = Column(Integer, primary_key=True)
    scalarfile_name = Column(String(255))
    scalarfile_type = Column(String(255))
    scalarfile_project_id=Column(Integer,ForeignKey('tab_project.project_id'))
    scalarfile_system_id=Column(Integer,ForeignKey('tab_system.system_id'))
    scalarfile_signal_id=Column(Integer,ForeignKey('tab_calculated_signal.signal_id'), index=True)
    scalarfile_link = Column(Text)
    scalarfile_size = Column(Integer)
    scalarfile_no_meas = Column(Integer)
    scalarfile_year = Column(Integer, index=True)
    scalarfile_month = Column(Integer, index=True)
    scalarfile_day = Column(Integer, index=True)
    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<ScalarFile(scalarfile_name='%s', scalarfile_type='%s', scalarfile_signal_id'%s')>" % (
                               self.scalarfile_name, self.scalarfile_type, self.scalarfile_signal_id)
