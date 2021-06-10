from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ...Database import Base

# Our User object, mapped to the 'users' table
class ReportSummary(Base):
    __tablename__ = 'tab_report_summary'

    # Every SQLAlchemy table should have a primary key named 'id'
    repsummary_id = Column(Integer, primary_key=True)
    repsummary_report_id= Column(Integer, ForeignKey('tab_report.report_id'))
    repsummary_name = Column(String(255))
    repsummary_seq = Column(String(255))
    repsummary_text = Column(Text)
   
    def __repr__(self):
       return "<Project(repsummary_id='%s', repsummary_report_id='%s', repsummary_name'%s')>" % (
                               self.repsummary_id, self.repsummary_report_id, self.repsummary_name)