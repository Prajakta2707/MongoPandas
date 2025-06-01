from flask import Flask, jsonify, request

app = Flask(__name__)

# Fixed "Database"
db = {
    1: {"name": "John Doe"},
    2: {"name": "Jane Smith"},
    3: {"name": "Prajakta Latane"},
    4: {"name": "Tulasi Dem"}
}

# Home route
@app.route('/api')
def home():
    return "Welcome to the Name API!"

@app.route('/api/entries', methods=['GET'])
def get_entries():
    return jsonify(db), 200  

# Create an existing entry
@app.route('/api/entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = {"name": data.get("name")}
    return jsonify({"id": new_id, "name": db[new_id]["name"]}), 201

# Update an existing entry
@app.route('/api/entries/<int:id>', methods=['PUT'])
def update_entry(id):
    if id in db:
        data = request.get_json()
        db[id]["name"] = data["name"]
        return jsonify(db[id]), 200
    else:
        return jsonify({"message": "Entry not found"}), 404

# Delete an entry
@app.route('/api/entries/<int:id>', methods=['DELETE'])
def delete_entry(id):
    if id in db:
        del db[id]
        return jsonify({"message": "Entry deleted"}), 200
    else:
        return jsonify({"message": "Entry not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)