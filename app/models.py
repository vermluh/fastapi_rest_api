from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app import Base


class Department(Base):	
	"""SQLAlchemy model/description for our departments"""
	__tablename__ = 'department'
	id = Column(Integer, primary_key=True)
	name = Column(String(), unique=True, nullable=False)
	users = relationship('User', backref='dep', lazy='dynamic')
	
	def __repr__(self):
		return '<Department %r>' % self.name	


class User(Base):
	"""SQLAlchemy model/description for our users"""
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(), unique=True, nullable=False)
	email = Column(String(), unique=True, nullable=False)
	department_id = Column(Integer, ForeignKey(Department.id))

	def __repr__(self):
		return '<User %r>' % self.username
	