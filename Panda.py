from flask import Flask, jsonify , request
import pandas as pd

app = Flask(__name__)

# Load CSV file using pandas   
df = pd.read_csv('student.csv')

@app.route('/HOME')
def home():
    return "Welcome to the Student API!"

@app.route('/students', methods=['GET'])
def get_students():
    # Convert DataFrame to dictionary
    data = df.to_dict(orient='records') # creates a filter to find the row where id matches. For example, if student_id = 2, this finds the row with id 2
    return jsonify(data)

#Get students by id
@app.route('/students/<int:student_id>')
def get_student_by_id(student_id):
    student = df[df["id"] == student_id]
    if not student.empty:
        return jsonify(student.to_dict(orient='records')[0])
    else:
        return jsonify({"error":"Student not found"}), 404

#Add new student
@app.route('/students', methods=['POST'])
def add_route():
    global df
    new_data = request.json
    new_df = pd.DataFrame([new_data]) #convert dict to dataframe
    df = pd.concat([df , new_df], ignore_index = True)
    return jsonify({"message" : "Student added successfuly"})

#Get data by column
@app.route('/students/col' , methods = ['GET'])
def get_name_city():
    sel_data = df[["name" , "city"]]
    return jsonify(sel_data.to_dict(orient='records'))

#Get student by name
@app.route('/students/<name>' , methods=['GET'])
def get_student(name):
    student = df[df['name']==name]
    if not student.empty:
        return jsonify(student.to_dict(orient='records')[0])
    else:
        return jsonify({"error":"Student not found"}) , 404

if __name__ == '__main__':
    app.run(debug=True)
