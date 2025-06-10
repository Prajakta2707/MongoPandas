
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

'''
collection.insert_many([
    {"SR.NO.":1 , "name": "John Doe" , "age" : 24},
    {"SR.NO.":2 , "name": "Jane Smith", "age" : 25},
    {"SR.NO.":3 , "name": "Prajakta Latane", "age" : 26},
    {"SR.NO.":4 , "name": "Tulasi Dem", "age" : 28}
])
'''

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MyDatabase"]
collection = db["PractiseDB"]

# Helper: convert Mongo ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# GET all documents
@app.route("/data", methods=["GET"])
def get_all():
    data = [serialize_doc(doc) for doc in collection.find()]
    return jsonify(data)

# GET by ID
@app.route("/data/<id>", methods=["GET"])
def get_by_id(id):
    doc = collection.find_one({"_id": ObjectId(id)})
    if doc:
        return jsonify(serialize_doc(doc))
    return jsonify({"error": "Not found"}), 404

# POST: Insert new document
@app.route("/data", methods=["POST"])
def create():
    data = request.json
    inserted = collection.insert_one(data)
    return jsonify({"inserted_id": str(inserted.inserted_id)})

# PUT: Update by ID
@app.route("/data/<id>", methods=["PUT"])
def update(id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"updated": True})
    return jsonify({"error": "Not found"}), 404

# DELETE by ID
@app.route("/data/<id>", methods=["DELETE"])
def delete(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"deleted": True})
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)