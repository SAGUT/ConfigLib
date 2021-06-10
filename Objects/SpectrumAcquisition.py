from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class SpectrumAcquisition(Base):
    __tablename__ = 'tab_spectrum_acquisition'

    # Every SQLAlchemy table should have a primary key named 'id'
    specacq_id = Column(Integer, primary_key=True)
    specacq_channel_id = Column(Integer, ForeignKey('tab_channel.channel_id'))
    specacq_signal_id = Column(Integer, ForeignKey('tab_calculated_signal.signal_id'))
    specacq_no_lines = Column(Integer)
    specacq_resolution = Column(Float)
    specacq_period = Column(Integer)
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<SpectrumAcquisition(specacq_id='%s', specacq_channel_id='%s', specacq_no_lines'%s')>" % (
                               self.specacq_id, self.specacq_channel_id, self.specacq_no_lines)