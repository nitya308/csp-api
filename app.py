# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from CS1 import CS1SectionsCSP

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True


@app.route("/", methods=["POST"])
def get_times():
    print("here")
    data = request.get_json()
    app.logger.info(f"Received")
    students = data['students']
    num_leaders = data['num_leaders']
    times = data['times']

    print(students)
    print(num_leaders)
    print(times)
    solver = CS1SectionsCSP(students, num_leaders, times)
    result = solver.solve()
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
