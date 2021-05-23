from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
from ...Database import Base

# Our User object, mapped to the 'users' table
class BKVTemplate(Base):
    __tablename__ = 'tab_bkv_template'

    # Every SQLAlchemy table should have a primary key named 'id'
    bkvtemplate_id = Column(Integer, primary_key=True)
    bkvtemplate_name = Column(String(255))
    bkvtemplate_templateid = Column(String(255))
    bkvtemplate_purpose = Column(Text)
    bkvtemplate_application = Column(String(255))
    bkvtemplate_description = Column(Text)
    bkvtemplate_filelink = Column(String(255))
    registers = relationship("BKVRegister", back_populates="template")
    pushes = relationship("BKVPush", back_populates="template")

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<BKVTemplate(bkvtemplate_id='%s', bkvtemplate_name='%s')>" % (self.bkvtemplate_id, self.bkvtemplate_name)