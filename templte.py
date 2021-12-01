# To insert a single document into the database,
# insert_one() function is used
@app.route('/insert-one/<name>/<id>/', methods=['GET'])
def insertOne(name, id):
    queryObject = {
        'Name': name,
        'ID': id
    }
    query = SampleTable.insert_one(queryObject)
    return "Query inserted...!!!"
  
# To find the first document that matches a defined query,
# find_one function is used and the query to match is passed
# as an argument.
@app.route('/find-one/<argument>/<value>/', methods=['GET'])
def findOne(argument, value):
    queryObject = {argument: value}
    query = SampleTable.find_one(queryObject)
    query.pop('_id')
    return jsonify(query)
  
# To find all the entries/documents in a table/collection,
# find() function is used. If you want to find all the documents
# that matches a certain query, you can pass a queryObject as an
# argument.
@app.route('/find/', methods=['GET'])
def findAll():
    query = SampleTable.find()
    # # Convert the output of query into list 
    # latest_doc = list(db.Resume.find().sort("_id", pymongo.DESCENDING).limit(1))

    # # use generation_time attribute to get datetime from _id
    # print(latest_doc[0]['_id'].generation_time)
    output = {}
    i = 0
    for x in query:
        if i < 2000: 
            i += 1
            continue
        output[i] = x
        output[i].pop('_id')
        output[i]['timestamp'] = output[i]['timestamp'].strftime("%Y-%m-%dT%H:%M:%S.%f") +"Z"
        i += 1
        if i>2099: break
    return jsonify(output)
  
  
# To update a document in a collection, update_one()
# function is used. The queryObject to find the document is passed as
# the first argument, the corresponding updateObject is passed as the
# second argument under the '$set' index.
@app.route('/update/<key>/<value>/<element>/<updateValue>/', methods=['GET'])
def update(key, value, element, updateValue):
    queryObject = {key: value}
    updateObject = {element: updateValue}
    query = SampleTable.update_one(queryObject, {'$set': updateObject})
    if query.acknowledged:
        return "Update Successful"
    else:
        return "Update Unsuccessful"