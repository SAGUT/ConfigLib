from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class Signal(Base):
    __tablename__ = 'tab_signal'

    # Every SQLAlchemy table should have a primary key named 'id'
    signal_id = Column(Integer, primary_key=True)
    signal_name = Column(String(255))
    signal_type = Column(String(255))
    signal_channel_id = Column(Integer, ForeignKey('tab_channel.channel_id'))
    signal_description = Column(Text)
    signal_azureid= Column(Text)
    channel = relationship("Channel", back_populates="signals")

    __mapper_args__ = {
        'polymorphic_identity':'generic',
        'polymorphic_on':signal_type
    }

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(signal_name='%s', signal_type='%s', signal_description'%s')>" % (self.signal_name, self.signal_type, self.signal_description)

class CalculatedSignal(Signal):
    __tablename__ = 'tab_calculated_signal'

    # Every SQLAlchemy table should have a primary key named 'id'
    calcsignal_id = Column(Integer, primary_key=True)
    calcsignal_signal_id = Column(Integer, ForeignKey('tab_signal.signal_id'))
    calcsignal_type = Column(String(255))
    
    

    __mapper_args__ = {
        'polymorphic_identity':'calculated_signal'
    }

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(signal_name='%s', signal_type='%s', signal_description'%s')>" % (self.signal_name, self.signal_type, self.signal_description)