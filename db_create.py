from app import db
from sqlalchemy import func, distinct, text
from model import RegisteredUser

# create the database and the db table
db.create_all()

# Query the number of users
num_of_users = db.session.query(func.count(distinct(RegisteredUser.id))).all()[0][0]

# Equates to the query above
# sql_num_of_users = text('select count(distinct id) from registered_user')
# num_of_users = db.session.execute(sql_num_of_users).fetchall()[0]


# users = db.session.query(RegisteredUser).all()
# for user in users:
#     print (user.email)

#print(num_of_users)
#print(type(num_of_users))

# insert data
#db.session.add(RegisteredUser(num_of_users + 1, 'user'+str(num_of_users+1), '11654321', str(num_of_users+1) + 'cba@yahoo.com'))

# commit the changes
db.session.commit()
