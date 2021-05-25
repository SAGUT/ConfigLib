from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float,Boolean
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
       return "<Channel(channel_name='%s', channel_number='%s', channel_type'%s')>" % (
                               self.channel_name, self.channel_number, self.channel_type)


class DDAU3Channel(Channel):
    __tablename__ = 'tab_ddau3_channel'

    # Every SQLAlchemy table should have a primary key named 'id'
    #ddauchannel_id = Column(Integer, primary_key=True)
    ddauchannel_channel_id = Column(Integer,ForeignKey('tab_channel.channel_id'), primary_key=True)
    ddauchannel_bkvid = Column(String(255))  
    ddauchannel_ch_idx= Column(Integer)
    ddauchannel_bkvname = Column(String(255))
    ddauchannel_limit_negative = Column(Float)
    ddauchannel_offset = Column(Float)
    ddauchannel_transducertype = Column(String(255))
    ddauchannel_CCS= Column(Boolean)
    ddauchannel_sensitivity = Column(Float)
    ddauchannel_enable= Column(Boolean)
    ddauchannel_limit_positive = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity':'ddau3channel',
    }
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<DDAU3Channel(ddauchannel_channel_id='%s', ddauchannel_bkvname='%s')>" % ( self.ddauchannel_channel_id, self.ddauchannel_bkvname)