from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
app.config['ORMONGO_REGION'] = "IAD"
app.config['ORMONGO_RS_URL'] = 'mongodb://iad2-c12-1.mongo.objectrocket.com:53515,iad2-c12-2.mongo.objectrocket.com:53515,iad2-c12-0.mongo.objectrocket.com:53515/?replicaSet=747aaeac3c6c4f359b4ffc81cfd04230&ssl=true'
app.config['ORMONGO_URL'] = 'mongodb://iad2-c12-1.mongo.objectrocket.com:53515?ssl=true'

@app.route("/")
def hi():
    title = 'hi'
    return title

uri = "mongodb://ynstf:ynstf2023@iad2-c12-1.mongo.objectrocket.com:53515,iad2-c12-2.mongo.objectrocket.com:53515,iad2-c12-0.mongo.objectrocket.com:53515/db_msgs?replicaSet=747aaeac3c6c4f359b4ffc81cfd04230&retrywrites=false"
mongo = PyMongo(app,uri=uri)

db = mongo.db
data = db.messages.find({"user_id":"3"},{"_id":False,"msgs":True})
print(data)

doc = {"user_id":"3","msgs":{"msg":"lgo","response":"zert"}}
db.messages.insert_one(doc)

data = db.messages.find({"user_id":"3"},{"_id":False,"msgs":True})
print(data)