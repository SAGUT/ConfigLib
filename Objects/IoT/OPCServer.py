from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from ..System import System
#from Application.ConfigLib.LibFrame import applicationDict      # .database import Base
from ...Database import Base

# Our User object, mapped to the 'users' table
class OPC(System):
    __tablename__ = 'tab_opc'

    # Every SQLAlchemy table should have a primary key named 'id'
    opc_id = Column(Integer, primary_key=True)
    opc_system_id = Column(Integer,ForeignKey('tab_system.system_id'))
    opc_ip = Column(String(255))
    opc_port = Column(Integer)
    
    
    __mapper_args__ = {
        'polymorphic_identity':'opc',
    }
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<DDAU3(ddau_id='%s', ddau_name='%s')>" % ( self.ddau_id, self.ddau_ip)