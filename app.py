import os
import sys
sys.path.append('/app/app.py')
from flask import Flask, jsonify, render_template
from datetime import datetime
from taskJson import workoutJson
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database import database # Always uncomment this before deploying in heroku
#from heroku.database import database # Always comment this before deploying in heroku
from sqlalchemy import create_engine, and_, distinct
from sqlalchemy.orm import sessionmaker


app = database.app

db_path = os.path.join(os.path.dirname(__file__), 'database/app.db')
db_uri = 'sqlite:///{}'.format(db_path)

#app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


engine = create_engine(db_uri)
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# @app.route('/')
# def hello_world():
#   return '<body><h2>Welcome to StayActiv</h2>' \
#          '<ul><li><a href="/activities">Activities</a>' \
#          '</li><li><a href="/exercises">Exercises</a>' \
#          '</li><li><a href="/workouts">Workout Programs - API_v0.1</a>' \
#          '</li><li><a href="/programroutine">Program Routine</a></li>' \
#          '</li><li><a href="/workoutprograms">Workout Programs - API_v1</a></li>' \
#          '</ul></body>'

@app.route('/')
def home():
    return render_template(
         'index.html',
        # title='Home Page',
        # year=datetime.now().year
    )

@app.route('/api/v1/workouts', methods=['GET'])
def workouts():
    try:
        list = workoutJson
    except:
        NoResultFound

    return jsonify({'activities': list})

@app.route('/api/v1/activities')
def activities():
    try:
        activlist = database.Activity.query.all()
        activity_schema = database.ActivitySchema(many=True)
        output = activity_schema.dump(activlist).data

    except:
        output = 'NoResultFound'

    return jsonify({'Activities': output})

@app.route('/api/v1/workoutprograms')
def workoutprog():
    try:
        workoutprogs = database.WorkoutPrograms.query.all()
        workout_schema = database.WorkoutProgramsSchema(many=True)
        output = workout_schema.dump(workoutprogs).data

    except:
        output = "No Results Found"

    return jsonify({"Workout Programs":output})

@app.route('/api/v1/programroutine')
def progroutine():
    try:
        progroutines = database.ProgramRoutines.query.all()
        program_schema = database.ProgramRoutinesSchema(many=True)
        output = program_schema.dump(progroutines).data
    except:
        output = "No Results Found"

    return jsonify({"Program Routine": output})

@app.route('/api/v1/exercises')
def exercises():
    return "No Data Found"

if __name__ == "__main__":
    app.run(debug=True)