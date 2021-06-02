from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.sql.sqltypes import Boolean, Float

#from Application.ConfigLib.LibFrame import applicationDict      # .database import Base
from ...Database import Base

# Our User object, mapped to the 'users' table
class SPMCondmasterServer(Base):
    __tablename__ = 'tab_spm_condmaster'

    # Every SQLAlchemy table should have a primary key named 'id'
    spmcondmaster_id = Column(Integer, primary_key=True)
    spmcondmaster_name = Column(String(255))
    spmcondmaster_address = Column(String(255))
    spmcondmaster_port = Column(Integer)
    spmcondmaster_user= Column(String(255))
    spmcondmaster_pwd= Column(String(255))
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<SPMCondmasterServer(spmcondmaster_name='%s', spmcondmaster_address='%s')>" % (self.spmcondmaster_name, self.spmcondmaster_address)

       

class SPMCondmasterDB(Base):
    __tablename__ = 'tab_spm_condmaster_db'

    # Every SQLAlchemy table should have a primary key named 'id'
    spmcondmasterdb_id = Column(Integer, primary_key=True)
    spmcondmasterdb_server = Column(Integer,ForeignKey('tab_spm_condmaster.spmcondmaster_id'))
    spmcondmasterdb_name = Column(String(255))
    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<SPMCondmasterDB(spmcondmasterdb_server='%s', spmcondmasterdb_name='%s')>" % (self.spmcondmaster_name, self.spmcondmaster_address)

class SPMCondmasterMP(Base):
    __tablename__ = 'tab_spm_condmaster_mp'

    # Every SQLAlchemy table should have a primary key named 'id'
    spmcondmastermp_id = Column(Integer, primary_key=True)
    spmcondmastermp_server = Column(Integer,ForeignKey('tab_spm_condmaster_db.spmcondmasterdb_id'))
    spmcondmastermp_number = Column(String(255))
    spmcondmastermp_intno = Column(Integer)
    spmcondmastermp_name = Column(String(255))
    spmcondmastermp_assignment = Column(Text(convert_unicode=True))
    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<SPMCondmasterMP(spmcondmastermp_server='%s', spmcondmastermp_name='%s')>" % (self.spmcondmastermp_server, self.spmcondmastermp_name)

class SPMCondmasterFFTAS(Base):
    __tablename__ = 'tab_spm_condmaster_fftas'

    # Every SQLAlchemy table should have a primary key named 'id'
    spmcondmasterfftas_id = Column(Integer, primary_key=True)
    spmcondmasterfftas_mpid = Column(Integer,ForeignKey('tab_spm_condmaster_mp.spmcondmastermp_id'))
    spmcondmasterfftas_dbid = Column(Integer,ForeignKey('tab_spm_condmaster_db.spmcondmasterdb_id'))
    spmcondmasterfftas_techid = Column(String(255))
    spmcondmasterfftas_assignments=Column(Text(convert_unicode=True))
    
    
    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<SPMCondmasterFFTAS(spmcondmasterfftas_id='%s', spmcondmasterfftas_mpid='%s')>" % (self.spmcondmasterfftas_id, self.spmcondmasterfftas_mpid)
