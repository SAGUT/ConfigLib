from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class TWFAcquisition(Base):
    __tablename__ = 'tab_twf_acquisition'

    # Every SQLAlchemy table should have a primary key named 'id'
    twfacq_id = Column(Integer, primary_key=True)
    twfacq_channel_id = Column(Integer, ForeignKey('tab_channel.channel_id'))
    twfacq_signal_id = Column(Integer, ForeignKey('tab_calculated_signal.signal_id'))
    twfacq_samplef = Column(Float)
    twfacq_length = Column(Float)
    twfacq_period = Column(Integer)
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<TWFAcquisition(twfacq_id='%s', twfacq_channel_id='%s', twfacq_samplef'%s')>" % (
                               self.twfacq_id, self.twfacq_channel_id, self.twfacq_samplef)