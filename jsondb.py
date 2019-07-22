import json

def login(username, password):
    with open('./dataset/database.json') as mydb:
        database = json.load(mydb)
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
    with open('./dataset/database.json') as mydb:
        database = json.load(mydb)
    username = username
    password = password
    for i in range(len(database)):
        if username == database[i]['username']:
            return False
        elif i == len(database) - 1:
            new_user = {'username': username, 'password':password}
            database.append(new_user)
            data_json = json.dumps(database)
            my_json = open('./dataset/database.json','w')
            my_json.write(data_json)
            return username
        else:
            continue