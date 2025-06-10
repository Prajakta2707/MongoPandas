from flask import Flask , request , jsonify
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")  # Connect to MONGODB running on localhost
db = client["MyDatabase"]  #Access or create database called MYDatabase
collection = db["Students_Data"] #Access or create Collection called Students

#insert many documents
collection.insert_many([
    {"name" : "Isha", "age" : 22, "city" : "Pune", "Hobby" : "Painting", "Blood Group" : "A+"},
    {"name" : "Shrenish", "age" : 23, "city" : "Mumbai", "Hobby" : "Dancing", "Blood Group" : "B+" },
    {"name" : "Satwik", "age" : 20, "city" : "Mumbai", "Hobby" : "Singing", "Blood Group" : "O+" },
    {"name" : "Sidhik", "age" : 21 , "city" : "Banglore" , "Hobby" : "Vlogging", "Blood Group" : "A-" },
    {"name" : "Prajakta", "age" : 24, "city" : "Pune", "Hobby" : "Swimming", "Blood Group" : "AB+"},
    {"name" : "Piyu", "age" : 22, "city" : "Mumbai", "Hobby" : "Dancing" , "Blood Group" : "O+" }
])

#chcekcking id data is inserted
for s in collection.find():
    print (s)