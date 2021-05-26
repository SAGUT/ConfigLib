from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ...Database import Base

# Our User object, mapped to the 'users' table
class Hierarchy(Base):
    __tablename__ = 'tab_hierarchy'

    # Every SQLAlchemy table should have a primary key named 'id'
    hierarchy_id = Column(Integer, primary_key=True)
    hierarchy_dbparent = Column(Integer)
    hierarchy_name = Column(String(255))
    hierarchy_project_id = Column(Integer, ForeignKey('tab_project.project_id'))
    hierarchy_azureid= Column(String(255))
    hierarchy_description = Column(String(255))
    hierarchy_number = Column(String(32))
    hierarchy_label = Column(Text)
    hierarchy_parentId= Column(String(255))
    hierarchy_designation= Column(String(255))
    hierarchy_metadata= Column(Text)
    hierarchy_environment= Column(String(255))
    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(hierarchy_name='%s', hierarchy_project_id='%s', hierarchy_label'%s')>" % (
                               self.hierarchy_name, self.hierarchy_project_id, self.hierarchy_label)