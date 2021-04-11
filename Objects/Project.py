from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
#from Application.database import Base, db_session, engine
from ..Database import Base
from .BKV.DDAU3 import DDAU3
# Our User object, mapped to the 'users' table
class Project(Base):
    __tablename__ = 'tab_project'

    # Every SQLAlchemy table should have a primary key named 'id'
    project_id = Column(Integer, primary_key=True)

    project_name = Column(String(255))
    project_site = Column(String(255))
    project_country = Column(String(255))
    project_environment = Column(String(32))
    project_description = Column(Text)
    projekt_type= Column(String(255))
    projekt_application= Column(String(255))
    projekt_site_id= Column(String(255))
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(project_name='%s', project_site='%s', project_country'%s')>" % (
                               self.project_name, self.project_site, self.project_country)