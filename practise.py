from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["MyDatabase"]
collection = db["PractiseDB"]
'''
collection.insert_many([
    {"SR.NO.":1 , "name": "John Doe" , "age" : 24},
    {"SR.NO.":2 , "name": "Jane Smith", "age" : 25},
    {"SR.NO.":3 , "name": "Prajakta Latane", "age" : 26},
    {"SR.NO.":4 , "name": "Tulasi Dem", "age" : 28}
])
'''
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc 

@app.route('/data', methods=['GET'])
def get_data():
    data = [serialize_doc(doc) for doc in collection.find({"age" : 24})]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


