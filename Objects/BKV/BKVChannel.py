from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Boolean,Float
from sqlalchemy.orm import relationship
from ...Database import Base

# Our User object, mapped to the 'users' table
class BKVChannel(Base):
    __tablename__ = 'tab_bkv_channel'

    # Every SQLAlchemy table should have a primary key named 'id'
    bkvchannel_id = Column(Integer, primary_key=True)
    bkvchannel_templateid = Column(Integer,ForeignKey('tab_bkv_template.bkvtemplate_id'))
    bkvchannel_ch_idx = Column(Integer)
    bkvchannel_idstr = Column(String(255))
    bkvchannel_name = Column(String(255))
    bkvchannel_limit_negative = Column(Float)
    bkvchannel_offset = Column(Float)
    bkvchannel_transducertype = Column(String(255))
    bkvchannel_CCS = Column(Boolean)
    bkvchannel_sensitivity = Column(Float)
    bkvchannel_enable = Column(Boolean)
    bkvchannel_limit_positive = Column(Float)

    template = relationship("BKVTemplate", back_populates="channels")
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<BKVChannel(bkvchannel_idstr='%s', bkvchannel_name='%s')>" % (self.bkvchannel_idstr, self.bkvchannel_name)