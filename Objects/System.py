from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class System(Base):
    __tablename__ = 'tab_system'

    # Every SQLAlchemy table should have a primary key named 'id'
    system_id = Column(Integer, primary_key=True)
    system_name = Column(String(255))
    system_type = Column(String(255))
    system_project_id = Column(Integer, ForeignKey('tab_project.project_id'))
    system_description = Column(Text)
    system_azureid = Column(String(255))
    system_environment = Column(String(255))
    system_supplier = Column(String(255))
    system_batchagg_id= Column(String(255))
    system_rtagg_id= Column(String(255))
    system_nonscalarbatchagg_id= Column(String(255))
    project = relationship("Project", back_populates="systems")
    channels = relationship("Channel", back_populates="system")
    
    __mapper_args__ = {
        'polymorphic_identity':'system',
        'polymorphic_on':system_type
    }

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(system_name='%s', system_type='%s', system_description'%s')>" % (
                               self.system_name, self.system_type, self.system_description)