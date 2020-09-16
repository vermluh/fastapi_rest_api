from typing import Dict, List, Optional
from typing import Iterable
from pydantic import BaseModel



class UserBase(BaseModel):
	id: int
	username: str
	email: str
	# department_id : int
	links : Dict = {}

	class Config:
		orm_mode = True
		fields = {'links': '_links'}


class User(BaseModel):
	data : UserBase


class UserIn(BaseModel):
	username: str
	email: str
	department_id : Optional[int] = None

	class Config:
		orm_mode = True


class UserListOut(BaseModel):
	total: Optional[int] = None
	limit: Optional[int] = None
	offset: Optional[int] = None	
	data: List = []


class DepartmentBase(BaseModel):
	id: int
	name: str
	links : Dict = {}

	class Config:
		orm_mode = True
		fields = {'links': '_links'}


class DepartmentIn(BaseModel):
	name: str
	class Config:
		orm_mode = True


class Department(BaseModel):
	data : DepartmentBase


class DepartmentListOut(BaseModel):
	total: Optional[int] = None
	limit: Optional[int] = None
	offset: Optional[int] = None	
	data: List = []