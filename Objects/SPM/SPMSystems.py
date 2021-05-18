from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from ..CMSSystem import System
#from Application.ConfigLib.LibFrame import applicationDict      # .database import Base
from ...Database import Base

# Our User object, mapped to the 'users' table
class SPMLarge(System):
    __tablename__ = 'tab_spml'

    # Every SQLAlchemy table should have a primary key named 'id'
    spml_id = Column(Integer, primary_key=True)
    spml_system_id = Column(Integer,ForeignKey('tab_system.system_id'))
    spml_ip = Column(String(255))
    
    __mapper_args__ = {
        'polymorphic_identity':'spmlarge',
    }
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(ddau_id='%s', ddau_name='%s')>" % (
                               self.spml_system_id, self.system_name)