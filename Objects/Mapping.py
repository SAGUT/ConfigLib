from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,UniqueConstraint
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class Mapping(Base):
    __tablename__ = 'tab_mapping'

    # Every SQLAlchemy table should have a primary key named 'id'
    mapping_id = Column(Integer, primary_key=True)
    mapping_position = Column(Integer,default=0)
    mapping_short = Column(String(10))
    mapping_long = Column(String(255))
    mapping_description = Column(Text)
    __table_args__ = (UniqueConstraint('mapping_position', 'mapping_short'),)
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Mapping(mapping_id='%s', mapping_short='%s', mapping_description'%s')>" % (
                               self.mapping_id, self.mapping_short, self.mapping_description)