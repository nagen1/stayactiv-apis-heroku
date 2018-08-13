from flask import Flask, jsonify
from taskJson import workoutJson

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello, its working!'

@app.route('/workouts', methods=['GET'])
def workouts():
    try:
        list = workoutJson
    except:
        NoResultFound

    return jsonify({'activities': list})


if __name__ == "__main__":
	app.run()
