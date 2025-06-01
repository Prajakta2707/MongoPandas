from flask import Flask, jsonify, request

app = Flask(__name__)


db = {
    1: {"name": "John Doe"},
    2: {"name": "Jane Smith"},
    3: {"name": "Prajakta Latane"},
    4: {"name": "Tulasi Dem"}
}

@app.route('/api/entries', methods=['POST'])
def create_entries():
    data = request.get_json()
    new_id = max(db.key()) + 1 if db else 1
    db[new_id] = {"name" : data.get("name")}
    return jsonify({"id" : new_id , "name" : db[new_id]["name"]}),201

@app.route('/api/entries', methods=['POST'])
def delete_entries():
    if id in db:
        del db[id]
        return jsonify({"message":"Entry is deleted"}),200
    else:
        return jsonify({"message":"Entry not found"}),404
if __name__ = '__main__':
    app.run(debug=True)
