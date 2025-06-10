# SORT , LIMIT , SKIP , Group by , Count

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

# Get all data sorted on age(asc)
@app.route("/All" , methods = ["GET"])
def get_all():
    data = [serialise_doc(doc) for doc in collection.find().sort("age" , 1)]
    return jsonify(data) # JSON does not guarantee key order. Python dictionaries (and MongoDB) store keys in order, but JSON viewers like Postman may display them differently. This doesn't affect your data.

# Get Distict City
@app.route("/distinct", methods=["GET"])
def distinct_names():
    City = collection.distinct("city")
    return jsonify(City)

# find document with age and sort by name desc
@app.route("/age_by_name/<int:age>" , methods=["GET"])
def get_by_age_sort_name(age):
    data = collection.find({"age" : age}).sort("name" , -1)
    result = [serialise_doc(doc) for doc in data]
    return jsonify(result)

# Get count of distinct city using group by nd sorting based on count
@app.route("/group_by_city" , methods=["GET"])
def group_by_city():
    pipeline = [
        {
            "$group" : {                   #Groups doc by city field 
                "_id" : "$city",           #group key is the city name
                "count" : {"$sum":1}       #count how many docs per city. For each grp,count is the sum of doc in tht city($sum adds 1 per doc)
            }
        },
        {
            "$sort" : {"count" : 1}          #sort the results by count
        }
    ]
    #since _id here is a string (city name) , no objid conversion needed
    
    result = list(collection.aggregate(pipeline))
    for doc in result:
        doc["city"] = doc.pop("_id")
    return jsonify(result)

# Get count of distinct city using group by , sort nd limit
@app.route("/group_by_city_with_limit/<int:limit>" , methods=["GET"])
def group_by_city_with_limit(limit):
    pipeline = [
        {
            "$group" : {                   #Groups doc by city field 
                "_id" : "$city",           #group key is the city name
                "count" : {"$sum":1}       #count how many docs per city. For each grp,count is the sum of doc in tht city($sum adds 1 per doc)
            }
        },
        {
            "$sort" : {"_id" : 1}          #sort the results by city name asc
        },
        {
            "$limit" : limit              
        }
    ]
    #since _id here is a string (city name) , no objid conversion needed
    
    result = list(collection.aggregate(pipeline))
    for doc in result:
        doc["city"] = doc.pop("_id")
    return jsonify(result)

# Group by city, age nd get its count
@app.route("/group_by_city_age" , methods=["GET"])
def group_by_city_age():
    pipeline = [
        {
            "$group" : {
                "_id" : {
                    "city" : "$city",
                    "age" : "$age"
                },           
                "count" : {"$sum":1}       
            }
        },
        {
            "$sort" : {
                "_id.city" : 1,
                "_id.age" : 1
            }
        }     
     
    ]
    
    
    result = list(collection.aggregate(pipeline))
    formatted = []
    for doc in result:
        formatted.append({
            "city" :doc["_id"]["city"],
            "age" : doc["_id"]["age"],
            "count" : doc["count"]
        })
         
    return jsonify(formatted)

#count where city is Mumbai or Pune
@app.route("/count_mum_pune" , methods=["GET"])
def count_mum_pune():
    query = {"city" : {"$in":["Mumbai" , "Pune"]}}
    count = collection.count_documents(query)
    return jsonify({"count":count})

#Individual count of Pune and Mumbai doc
@app.route("/count_mum_pune_indi" , methods=["GET"])
def count_mum_pune_indi():
    mum_count = collection.count_documents({"city": "Mumbai"})
    pune_count = collection.count_documents({"city": "Pune"})
    total = mum_count + pune_count 

    return jsonify({
        "Mumbai" : mum_count,
        "Pune" : pune_count,
        "Total" : total
    })

if __name__ == "__main__":
    app.run(debug=True)