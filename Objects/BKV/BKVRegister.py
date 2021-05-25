from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float
from sqlalchemy.orm import relationship
from ...Database import Base

# Our User object, mapped to the 'users' table
class BKVRegister(Base):
    __tablename__ = 'tab_bkv_register'

    # Every SQLAlchemy table should have a primary key named 'id'
    bkvregister_id = Column(Integer, primary_key=True)
    bkvregister_templateid = Column(Integer,ForeignKey('tab_bkv_template.bkvtemplate_id'))
    bkvregister_register = Column(Integer)
    bkvregister_input = Column(String(255))
    bkvregister_name = Column(String(255))
    bkvregister_physical_quantity= Column(String(255))
    bkvregister_unit = Column(String(255))
    bkvregister_okrangehigh = Column(Float)
    bkvregister_okrangelow = Column(Float)
    bkvregister_history = Column(Text)
    template = relationship("BKVTemplate", back_populates="registers")
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<BKVTemplate(bkvtemplate_id='%s', bkvtemplate_name='%s')>" % (self.bkvtemplate_id, self.bkvtemplate_name)