import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://yoyogesh27:LH44isthegoat@cluster0.umivw3g.mongodb.net/?retryWrites=true&w=majority')

db = cluster["yogeshdb"]
coaches = db["coaches"]
players = db["players"]
temp = []
result_username = players.find()
result_email = players.find({'email': 'b@gmail.com'})
for i in result_email:
    temp.append(i)
print(temp)
if temp == []:
    print(1)
else:
    print(0)