from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from typing import Dict, Any


Base = declarative_base()

class UserDBModel(Base):
	__tablename__ = 'users'

	id = Column(String, primary_key=True)
	email = Column(String)
	full_name = Column(String)
	password = Column(String)
	roles = Column(String)
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	verified = Column(Boolean, default=False)
	banned = Column(Boolean, default=False)

	def to_dict(self) -> Dict[str, Any]:
		return {
			'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'verified': self.verified,
            'banned': self.banned,
            'roles': self.roles
		}

	def __repr__(self) -> str:
		return f"<User(id='{self.id}', email='{self.email}')>"
