from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from ..System import System
#from Application.ConfigLib.LibFrame import applicationDict      # .database import Base
from ...Database import Base

# Our User object, mapped to the 'users' table
class DDAU3(System):
    __tablename__ = 'tab_ddau3'

    # Every SQLAlchemy table should have a primary key named 'id'
    ddau_id = Column(Integer, primary_key=True)
    ddau_system_id = Column(Integer,ForeignKey('tab_system.system_id'))
    ddau_ip = Column(String(255))
    ddau_template = Column(Integer,ForeignKey('tab_bkv_template.bkvtemplate_id'),nullable=True)
    ddau_port = Column(Integer)
    ddau_ip = Column(String(255))
    ddau_hardware_revision = Column(String(255))
    ddau_device_id = Column(String(255))
    ddau_prod_date = Column(String(255))
    ddau_factory_version = Column(String(255))
    ddau_ser_no = Column(String(255)) 
    ddau_MAC = Column(String(255))
    ddau_version = Column(String(255))
    
    __mapper_args__ = {
        'polymorphic_identity':'ddau3',
    }
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<DDAU3(ddau_id='%s', ddau_name='%s')>" % ( self.ddau_id, self.ddau_ip)