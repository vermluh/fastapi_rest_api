import csv
from app import app, create_app, db
from app import models


hr = models.Department(name='HR')
sales = models.Department(name='Sales')
legal = models.Department(name='Legal')
engineering = models.Department(name='Engineering')
db.add(hr)
db.add(sales)
db.add(legal)
db.add(engineering)

admin = models.User(username="admin", email="admin@example.com")
guest = models.User(username="guest", email="guest@example.com")
jan = models.User(username="jan", email="jan@example.com")
hein = models.User(username="hein", email="hein@example.com")
klaas = models.User(username="klaas", email="klaas@example.com")
pit = models.User(username="pit", email="pit@example.com")

db.add(admin)
db.add(guest)
db.add(jan)
db.add(hein)
db.add(klaas)
db.add(pit)

hr.users.append(admin)
sales.users.append(jan)
legal.users.append(hein)
engineering.users.append(klaas)
engineering.users.append(pit)

db.commit()


with open('mock_data.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		
		mock_user = models.User(username=row["username"], email=row["email"], department_id=row["department_id"])
		db.add(mock_user)
		line_count += 1

db.commit()