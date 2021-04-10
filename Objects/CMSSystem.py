from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class CMSSytem(Base):
    __tablename__ = 'tab_system'

    # Every SQLAlchemy table should have a primary key named 'id'
    system_id = Column(Integer, primary_key=True)
    system_name = Column(String(255))
    system_type = Column(String(255))
    system_project_id = Column(Integer, ForeignKey('tab_project.project_id'))
    system_description = Column(Text)
    
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(system_name='%s', system_type='%s', system_description'%s')>" % (
                               self.system_name, self.system_type, self.system_description)