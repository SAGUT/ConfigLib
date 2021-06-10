from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float,Boolean
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from  ...Database import Base
# Our User object, mapped to the 'users' table
class ChannelPlots(Base):
    __tablename__ = 'tab_channel_plots'

    # Every SQLAlchemy table should have a primary key named 'id'
    channel_plot_id = Column(Integer, primary_key=True)
    channel_plot_project_id = Column(Integer, ForeignKey('tab_project.project_id'))
    channel_plot_report_id = Column(Integer, ForeignKey('tab_report.report_id'))
    channel_plot_channel_id = Column(Integer, ForeignKey('tab_channel_status.channel_status_channel_id'))
    channel_plot_plotfile= Column(String(255))
    channel_plot_caption= Column(String(255))
    channel_plot_sequence= Column(Integer)

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<ChannelPlots(channel_plot_channel_id='%s', channel_plot_report_id='%s', channel_plot_plotfile'%s')>" % (
                               self.channel_plot_channel_id, self.channel_plot_report_id, self.channel_plot_plotfile)
