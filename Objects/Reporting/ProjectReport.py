from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float,BigInteger
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from  ...Database import Base
# Our User object, mapped to the 'users' table
class Report(Base):
    __tablename__ = 'tab_report'

    # Every SQLAlchemy table should have a primary key named 'id'
    report_id = Column(Integer, primary_key=True)
    report_name = Column(String(255))
    report_project_id = Column(Integer, ForeignKey('tab_project.project_id'))
    report_type = Column(String(255))
    report_timestamp = Column(BigInteger)
    report_starttime = Column(BigInteger)  
    report_endtime= Column(BigInteger)
    report_timetext= Column(String(255))
    report_author= Column(String(255))
    report_description = Column(Text)


    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Report(report_name='%s', report_project_id='%s', report_type'%s')>" % (
                               self.report_name, self.report_project_id, self.report_type)
