from __future__ import absolute_import
from sqlalchemy import Column, Integer, String, ForeignKey,Text,Float
from sqlalchemy.orm import relationship
#from Application.database import Base, db_session, engine
from ..Database import Base
# Our User object, mapped to the 'users' table
class Sensor(Base):
    __tablename__ = 'tab_sensor'

    # Every SQLAlchemy table should have a primary key named 'id'
    sensor_id = Column(Integer, primary_key=True)
    sensor_name = Column(String(255))
    sensor_type = Column(String(255))
    sensor_channel_id=Column(Integer,ForeignKey('tab_channel.channel_id'))
    sensor_description = Column(Text)
    sensor_supplier = Column(String(255))
    sensor_supplier_name = Column(String(255))
    channel = relationship("Channel", back_populates="sensor")
    
    __mapper_args__ = {
        'polymorphic_identity':'genericsensor',
        'polymorphic_on':sensor_type
    }

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Project(sensor_name='%s', sensor_type='%s', sensor_description'%s')>" % (
                               self.sensor_name, self.sensor_type, self.sensor_description)

class AccelerationSensor(Base):
    __tablename__ = 'tab_accsensor'

    # Every SQLAlchemy table should have a primary key named 'id'
    accsensor_id = Column(Integer, primary_key=True)
    accsensor_ccs = Column(String(255))
    accsensor_bias_min = Column(Float)
    accsensor_bias_max = Column(Float)
    accsensor_meas_max = Column(Float)
    accsensor_frequency_min = Column(Float)
    accsensor_frequency_max = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity':'accelerationsensor'
    }

    # Lets us print out a object conveniently.
    def __repr__(self):
       return "<Project(accsensor_id='%s', accsensor_frequency_min='%s', accsensor_frequency_max'%s')>" % (
                               self.accsensor_id, self.accsensor_frequency_min, self.accsensor_frequency_max)