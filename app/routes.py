from app import app, db
from . import models, schemas
from typing import List
from fastapi import Request, HTTPException, Response, status


# List
@app.get("/users", response_model=schemas.UserListOut)
def read_users(request:Request, offset=0, limit=100):
	total = db.query(models.User).count()
	users = db.query(models.User).offset(offset).limit(limit).all()	
	for user in users:
		_links = {}
		_links.update({"self" : request.url_for("read_user", user_id=user.id)})
		_links.update({"collection" : request.url_for("read_users")})
		_links.update({"department" : request.url_for("read_department", department_id=user.department_id)})
		user.__setattr__("_links", _links)
	return {'data':users, 'total':total, 'offset':offset, 'limit':limit}


# Create
@app.post("/users", response_model=schemas.User)
def create_user(request:Request, response: Response, user_data: schemas.UserIn):
	user = models.User(username=user_data.username, email=user_data.email)
	db.add(user)
	db.commit()
	_links = {}
	_links.update({"self" : request.url_for("read_user", user_id=user.id)})
	_links.update({"collection" : request.url_for("read_users")})
	_links.update({"department" : request.url_for("read_department", department_id=user.department_id)})
	user.__setattr__("_links", _links)
	response.status_code = status.HTTP_201_CREATED
	return {'data':user}


# Read
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(request:Request, user_id):
	user = db.query(models.User).get(user_id)
	if not user:
		raise HTTPException(status_code=404, detail=f"Could not find User with ID {user_id}")			
	_links = {}
	_links.update({"self" : request.url_for("read_user", user_id=user.id)})
	_links.update({"collection" : request.url_for("read_users")})
	_links.update({"department" : request.url_for("read_department", department_id=user.department_id)})
	user.__setattr__("_links", _links)
	return {'data':user}


# Update
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(request:Request, user_id, user_data: schemas.UserIn):
	user = db.query(models.User).get(user_id)
	if not user:
		raise HTTPException(status_code=404, detail=f"Could not find User with ID {user_id}")
	user.username = user_data.username
	user.email = user_data.email
	user.department_id = user_data.department_id
	db.commit()
	return {'data':user}


# Delete
@app.delete("/users/{user_id}")
def delete_user(user_id):
	user = db.query(models.User).get(user_id)
	if user:
		db.delete(user)
		db.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=404, detail=f"Could not find User with ID {user_id}")


# List
@app.get("/departments", response_model=schemas.DepartmentListOut)
def read_departments(request:Request, offset=0, limit=100):
	total = db.query(models.Department).count()
	departments = db.query(models.Department).offset(offset).limit(limit).all()	
	for department in departments:
		_links = {}
		_links.update({"self" : request.url_for("read_department", department_id=department.id)})
		_links.update({"collection" : request.url_for("read_departments")})
		_links.update({"users" : request.url_for("read_department_users", department_id=department.id)})
		department.__setattr__("_links", _links)
	return {'data':departments, 'total':total, 'offset':offset, 'limit':limit}


# Create
@app.post("/departments", response_model=schemas.Department)
def create_department(request:Request, response: Response, department_data: schemas.DepartmentIn):
	department = models.Department(name=department_data.name)
	db.add(department)
	db.commit()
	_links = {}
	_links.update({"self" : request.url_for("read_department", department_id=department.id)})
	_links.update({"collection" : request.url_for("read_departments")})
	_links.update({"users" : request.url_for("read_department_users", department_id=department.id)})
	department.__setattr__("_links", _links)
	response.status_code = status.HTTP_201_CREATED
	return {'data':department}


# Read
@app.get("/departments/{department_id}", response_model=schemas.Department)
def read_department(request:Request, department_id):
	department = db.query(models.Department).get(department_id)
	if not department:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")
	_links = {}
	_links.update({"self" : request.url_for("read_department", department_id=department.id)})
	_links.update({"collection" : request.url_for("read_departments")})
	_links.update({"users" : request.url_for("read_department_users", department_id=department_id)})
	department.__setattr__("_links", _links)
	return {'data':department}


# Update
@app.put("/departments/{department_id}", response_model=schemas.Department)
def update_user(request:Request, department_id, department_data: schemas.DepartmentIn):
	department = db.query(models.Department).get(department_id)
	if not department:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")
	department.name = department_data.name
	db.commit()
	return {'data':department}


# Delete
@app.delete("/departments/{department_id}")
def delete_department(department_id):
	department = db.query(models.Department).get(department_id)
	if department:
		db.delete(department)
		db.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")


# List Department Users
@app.get("/departments/{department_id}/users", response_model=schemas.UserListOut)
def read_department_users(request:Request, department_id:int, offset=0, limit=100):
	department = db.query(models.Department).get(department_id)
	if not department:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")	
	total = department.users.count()
	users = department.users.offset(offset).limit(limit).all()
	for user in users:
		_links = {}
		_links.update({"self" : request.url_for("read_user", user_id=user.id)})
		_links.update({"collection" : request.url_for("read_users")})
		_links.update({"department" : request.url_for("read_department_users", department_id=user.department_id)})
		user.__setattr__("_links", _links)
	return {'data':users, 'total':total, 'offset':offset, 'limit':limit}
