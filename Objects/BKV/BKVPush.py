from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Boolean
from sqlalchemy.orm import relationship
from ...Database import Base


class BKVPush(Base):
    __tablename__ = 'tab_bkv_push'

    # Every SQLAlchemy table should have a primary key named 'id'
    bkvpush_id = Column(Integer, primary_key=True)
    bkvpush_templateid = Column(Integer,ForeignKey('tab_bkv_template.bkvtemplate_id'))
    bkvpush_bkvid = Column(String(255))
    bkvpush_trigger = Column(String(255))
    bkvpush_trigger_data_timer = Column(Integer)
    bkvpush_target = Column(String(255))
    bkvpush_target_data_trigger = Column(String(255))
    bkvpush_config_secure= Column(Boolean)
    bkvpush_config_refid = Column(String(255))
    bkvpush_config_page = Column(String(255))
    bkvpush_config_remote_server = Column(String(255))
    bkvpush_config_port = Column(Integer)
    bkvpush_config_retries = Column(Integer)
    bkvpush_config_delay = Column(Integer)
    bkvpush_config_timeout = Column(Integer)
    template = relationship("BKVTemplate", back_populates="pushes")
    

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<BKVPush(bkvpush_id='%s', bkvpush_id='%s')>" % (self.bkvpush_id, self.bkvpush_id)