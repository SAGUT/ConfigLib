from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class Channel(Base):
    __tablename__ = 'tab_channel'

    # Every SQLAlchemy table should have a primary key named 'id'
    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String(255))
    channel_number= Column(String(255))
    channel_type = Column(String(255))
    channel_system_id = Column(Integer, ForeignKey('tab_system.system_id'))
    #channel_related_channel = Column(Integer, ForeignKey('tab_channel.channel_id'), nullable=True)
    channel_description = Column(Text)
    system = relationship("System", back_populates="channels")
    #signals = relationship("Signal", back_populates="channel")
    sensor= relationship("Sensor", back_populates="channel")
    
    __mapper_args__ = {
        'polymorphic_identity':'channel',
        'polymorphic_on':channel_type
    }

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(system_name='%s', system_type='%s', system_description'%s')>" % (
                               self.system_name, self.system_type, self.system_description)