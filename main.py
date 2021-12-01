import os
from flask import Flask, jsonify
from flask_cors import CORS
from uuid import uuid4
import pymongo
import requests

connection_url = os.environ['mongodbkey']
client = pymongo.MongoClient(connection_url)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

Database = client["publicService"]
userTable = Database["user"]

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/cek/')
def cek():
  query = userTable.find()
  output = {}
  for i, data in enumerate(query):
    data.pop("_id")
    output[i] = data
  return jsonify(output)

@app.route('/register/<name>/', methods=['GET'])
def insertOne(name):
    queryObject = {
        'Name': name,
        'UUID': uuid4().hex,
        'limit': 5
    }
    userTable.insert_one(queryObject)
    return "Query inserted...!!!"

@app.route('/api/<key>/catimg')
def catimg(key):  
  serviceID = 'catimg'
  queryObject = {'UUID': key}
  query = userTable.find_one(queryObject)
  if query:
    counter = query.get(serviceID)
    if counter:
      counter += 1
      if counter < query.get("limit"):
        updateObject = {serviceID: counter}
        query = userTable.update_one(queryObject, {'$set': updateObject})
        if query.acknowledged:
          url = "https://thatcopy.pw/catapi/rest/"
          r = requests.get(url)
          return jsonify(r.json())
        else:
          return jsonify({"error": "Error Adding counter"})
      else:
        return jsonify({"error": f"API request exceed the limit ({query.get('limit')})"})
    else:
      updateObject = {serviceID: 1}
      query = userTable.update_one(queryObject, {'$set': updateObject})
      if query.acknowledged:
        url = "https://thatcopy.pw/catapi/rest/"
        r = requests.get(url)
        return jsonify(r.json())
      else:
        return jsonify({"error": "Error Adding new service counter"})
  else:
    return jsonify({"error": "apikey invalid"})


if __name__ == '__main__':
  app.run( # Starts the site
    host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
    port=5000,  # Randomly select the port the machine hosts on.
    debug=True
  )