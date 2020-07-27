from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1',27017)
db = client['users_db']

users = db.users
books = db.books


# users.insert_one({"author": "Peter",
#                "age" : 78,
#                "text": "is cool! Wildberry",
#                "tags": ['cool','hot','ice'],
#                "date": '14.06.1983'})
#CRUD

# users.insert_many(
#     [{"author": "John",
#                "age" : 29,
#                "text": "Too bad! Strawberry",
#                "tags": ['ice'],
#                "date": '04.08.1971'},
#
#                     {"author": "Anna",
#                "age" : 36,
#                "title": "Hot Cool!!!",
#                "text": "easy too!",
#                "date": '26.01.1995'},
#
#                    {"author": "Jane",
#                "age" : 43,
#                "title": "Nice book",
#                "text": "Pretty text not long",
#                "date": '08.08.1975',
#                "tags":['fantastic','criminal']}
#      ]
# )


# for user in users.find({'$or':[{'author':'Peter'},{'age':21}]}):
#     print(user)

# for user in users.find({'author':'Peter'} , {'author':1,'age':1,'date':1, '_id':0}):
#     print(user)

# for user in users.find({} , {'author':1,'age':1,'date':1, '_id':0}).sort('age',-1).limit(3):
#     print(user)

# for user in users.find({'author':'Peter','age':{'$gte':43}}):
#     print(user)

doc = {'age': 18,
 'author': 'Anna',
 'date': '26.01.1998',
 'text': 'easy too!',
 'title': 'Hot Cool!!!'}


users.find()
books.find()

# users.replace_one({'author':'Peter','age':22},doc)
# users.replace_many()
users.update_many({},{'$set':{'new_field':47}})
# users.update_one()

# users.delete_one({'author':'Anna'})
# users.delete_many({})
# users.drop()



for user in users.find({}):
     print(user)

print(db.show_collections())