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
    
    __mapper_args__ = {
        'polymorphic_identity':'ddau3',
    }
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(ddau_id='%s', ddau_name='%s')>" % ( self.ddau_id, self.ddau_name)