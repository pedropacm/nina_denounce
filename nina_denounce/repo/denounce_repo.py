import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///:memory:')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

class DenounceRepo:

	def __init__(self):
		Base.metadata.create_all(engine)
		

	def save(self, denounce):
		session.add(denounce)
		session.commit()
		return session.query(Denounce).filter(
			Denounce.lat == denounce.lat,
			Denounce.lon == denounce.lon,
			Denounce.bus_number == denounce.bus_number).first()

	def find_by_id(self, denounce_id):
		return session.query(Denounce).filter(Denounce.id == denounce_id).first()

	def list_all(self):
		return session.query(Denounce).all()

class Denounce(Base):
	__tablename__ = 'denounce'
	id = Column(Integer, primary_key=True)
	lat = Column(String(20), nullable=False)
	lon = Column(String(20), nullable=False)
	bus_number = Column(Integer, nullable=False)
	user_id = Column(Integer, nullable=True)
	description = Column(String(250), nullable=True)