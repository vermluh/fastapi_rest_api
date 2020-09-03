from app import app, db
from . import models, schemas
from typing import List
from fastapi import Request, HTTPException, Response, status


@app.get("/users", response_model=schemas.UserListOut)
@app.get("/users/", response_model=schemas.UserListOut)
def read_users(request:Request, offset=0, limit=100):
	total = db.query(models.User).count()
	users = db.query(models.User).offset(offset).limit(limit).all()	
	for user in users:
		_links = {}
		_links.update({"self" : request.url_for("read_users", user_id=user.id)})
		_links.update({"collection" : request.url_for("read_users")})
		_links.update({"department" : request.url_for("read_departments", department_id=user.department_id)})
		user.__setattr__("_links", _links)
	return {'data':users, 'total':total, 'offset':offset, 'limit':limit}


@app.get("/users/{user_id}", response_model=schemas.User)
def read_users(request:Request, user_id):
	user = db.query(models.User).get(user_id)
	if not user:
		raise HTTPException(status_code=404, detail=f"Could not find User with ID {user_id}")			
	_links = {}
	_links.update({"self" : request.url_for("read_users", user_id=user.id)})
	_links.update({"collection" : request.url_for("read_users")})
	_links.update({"department" : request.url_for("read_departments", department_id=user.department_id)})
	user.__setattr__("_links", _links)
	return {'data':user}


@app.delete("/users/{user_id}")
def delete_user(user_id):
	user = db.query(models.User).get(user_id)
	if user:
		db.delete(user)
		db.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=404, detail=f"Could not find User with ID {user_id}")


@app.get("/departments", response_model=schemas.DepartmentListOut)
@app.get("/departments/", response_model=schemas.DepartmentListOut)
def read_departments(request:Request, offset=0, limit=100):
	total = db.query(models.Department).count()
	departments = db.query(models.Department).offset(offset).limit(limit).all()	
	for department in departments:
		_links = {}
		_links.update({"self" : request.url_for("read_departments", department_id=department.id)})
		_links.update({"collection" : request.url_for("read_departments")})
		_links.update({"users" : request.url_for("read_department_users", department_id=department.id)})
		department.__setattr__("_links", _links)
	return {'data':departments, 'total':total, 'offset':offset, 'limit':limit}


@app.get("/departments/{department_id}", response_model=schemas.Department)
def read_departments(request:Request, department_id):
	department = db.query(models.Department).get(department_id)
	if not department:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")
	_links = {}
	_links.update({"self" : request.url_for("read_departments", department_id=department.id)})
	_links.update({"collection" : request.url_for("read_departments")})
	_links.update({"users" : request.url_for("read_department_users", department_id=department_id)})
	department.__setattr__("_links", _links)
	return {'data':department}


@app.get("/departments/{department_id}/users", response_model=schemas.UserListOut)
def read_department_users(request:Request, department_id:int, offset=0, limit=100):
	department = db.query(models.Department).get(department_id)
	if not department:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")	
	total = department.users.count()
	users = department.users.offset(offset).limit(limit).all()
	for user in users:
		_links = {}
		_links.update({"self" : request.url_for("read_users", user_id=user.id)})
		_links.update({"collection" : request.url_for("read_users")})
		_links.update({"department" : request.url_for("read_department_users", department_id=user.department_id)})
		user.__setattr__("_links", _links)
	return {'data':users, 'total':total, 'offset':offset, 'limit':limit}


@app.delete("/departments/{department_id}")
def delete_department(department_id):
	department = db.query(models.Department).get(department_id)
	if department:
		db.delete(department)
		db.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=404, detail=f"Could not find Department with ID {department_id}")