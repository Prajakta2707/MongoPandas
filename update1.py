from flask import Flask , request , jsonify
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")  # Connect to MONGODB running on localhost
db = client["MyDatabase"]  # Access or create database called MYDatabase
collection = db["Students_Data"] # Access or create Collection called Students

app = Flask(__name__)

def serialise_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# update the age as 22 where city is Mumbai nd age is 20
@app.route("/update-age" , methods=["PUT"])
def update_age():
    query = {"city" : "Mumbai" , "age":20}
    new_val = {"$set" : {"age" : 22}}

    result = collection.update_many(query , new_val)

    return jsonify({
        "matched" : result.matched_count,
        "modified" : result.modified_count,
        "message" : f"Updated {result.modified_count} student(s) in Mumbai from age 20 to 22"
    })


if __name__ == "__main__":
    app.run(debug=True)