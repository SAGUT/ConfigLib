from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float,Boolean
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from  ...Database import Base
# Our User object, mapped to the 'users' table
class ChannelStatus(Base):
    __tablename__ = 'tab_channel_status'

    # Every SQLAlchemy table should have a primary key named 'id'
    channel_status_id = Column(Integer, primary_key=True)
    channel_status_project_id = Column(Integer, ForeignKey('tab_project.project_id'))
    channel_status_report_id = Column(Integer, ForeignKey('tab_report.report_id'))
    channel_status_channel_id = Column(Integer, ForeignKey('tab_channel.channel_id'))
    channel_status_status= Column(String(255))
    channel_status_description = Column(Text)


    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<ChannelStatus(report_name='%s', report_project_id='%s', report_type'%s')>" % (
                               self.report_name, self.report_project_id, self.report_type)
