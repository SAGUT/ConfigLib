from __future__ import absolute_import
import logging
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from .LibFrame import applicationDict

Base = declarative_base()
dbconfig=applicationDict['config']['dbsetup']

if dbconfig['type']=="mariadb":
    logging.debug("using mariadb")
    link="mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4".format(dbconfig['user'],
                                                                      dbconfig['pwd'],
                                                                      dbconfig['server'],
                                                                      dbconfig['port'],
                                                                      dbconfig['database'])

logging.debug(link)
engine = create_engine(link, echo=False)
db_session = scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False
        )
    )
