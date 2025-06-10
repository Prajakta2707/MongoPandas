from flask import Flask , request , jsonify
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")  # Connect to MONGODB running on localhost
db = client["MyDatabase"]  #Access or create database called MYDatabase
collection = db["Students_Data"] #Access or create Collection called Students

app = Flask(__name__)

def serialise_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# Get all data sorted on age(asc)
@app.route("/All" , methods = ["GET"])
def get_all():
    data = [serialise_doc(doc) for doc in collection.find().sort("age" , 1)]
    return jsonify(data) #JSON does not guarantee key order.Python dictionaries (and MongoDB) store keys in order, but JSON viewers like Postman may display them differently. This doesn't affect your data.

#Filtering 
@app.route("/Filter" ,methods = ["GET"])
def get_filter():
    data = list(collection.find({}, {"name": 1, "age": 1, "city": 1, "_id": 0}))
    return jsonify(data) #By default, Python dictionaries (and MongoDB) store keys in insertion order, but Postman or jsonify() may reorder them during serialization.

#To give 3 entries , sorting in ascsnding in terms of name and will skip first 2 results and give rest 3 entries as per limit.
@app.route("/students", methods=["GET"])
def get_students():
    data = [serialise_doc(doc) for doc in collection.find().skip(2).limit(3).sort("name", 1)]
    return jsonify(data)

# Gets student by ID
@app.route("/students/<id>", methods=["GET"])
def get_student(id):
    doc = collection.find_one({"_id": ObjectId(id)})
    if doc:
        student = serialise_doc(doc)
        return jsonify(student)
    else:
        return jsonify({"error":"Student not Found"} , 404)

# Gets 1 entry by age
@app.route('/by_age/<int:age>', methods=['GET'])
def get_data(age):
    doc = collection.find({"age" : age})
    if doc :
        student = serialise_doc(doc)
        return jsonify(student)
    else:
        return jsonify({"error": "Student age not Found"})

# Get all students of a specific age
@app.route("/all_of_parti_age/<int:age>" , methods=["GET"])
def all_of_parti_age(age):
    data = collection.find({"age":age})
    result = []
    for d in data:
        d["_id"] = str(d["_id"])
        result.append(d)
    return jsonify(result)

#Get all students from a specific city Pune
@app.route('/PuneCity', methods=['GET'])
def Pune_City():
    data = [serialise_doc(doc) for doc in collection.find({"city" : "Pune"})]
    return jsonify(data)

# Get all students from a specific city (e.g., Mumbai)
@app.route("/all_of_parti_city/<city>" , methods=["GET"])
def all_Specific_city(city):
    data = collection.find({"city":city})
    result = []
    for d in data:
        d["_id"] = str(d["_id"])
        result.append(d)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)


