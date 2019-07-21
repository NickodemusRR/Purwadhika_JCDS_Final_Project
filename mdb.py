from pymongo import MongoClient

server = MongoClient('mongodb://localhost:27017/')

db = server['nrrdb']        
collection = db['my_database'] 

database = []
for i in collection.find():
    my_dict = {
        'username': i['username'],
        'password' : i['password']
    }
    database.append(my_dict)

def login(username, password):
    username = username
    password = password
    for i in range(len(database)):
        if username == database[i]['username'] and password == database[i]['password']:
            return username
        elif i == len(database) - 1:
            return False
        else:
            continue

def signup(username, password):
    username = username
    password = password
    for i in range(len(database)):
        if username == database[i]['username']:
            return False
        elif i == len(database) - 1:
            new_user = {'username': username, 'password':password}
            collection.insert_one(new_user)
            return username
        else:
            continue