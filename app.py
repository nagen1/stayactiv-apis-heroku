import os
import sys
sys.path.append('/app/app.py')
from flask import Flask, jsonify
from taskJson import workoutJson
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database import database
#from app.database import Acitvity
from sqlalchemy import create_engine, and_, distinct
from sqlalchemy.orm import sessionmaker

app = database.app
db_path = os.path.join(os.path.dirname(__file__), 'database/app.db')
print(db_path)
db_uri = 'sqlite:///{}'.format(db_path)
print(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(db_uri)
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


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

@app.route('/activities')
def activities():
    try:
        activlist = database.Activity.query.all()
        activity_schema = database.ActivitySchema(many=True)
        output = activity_schema.dump(activlist).data

    except:
        output = 'NoResultFound'

    return jsonify({'Activities': output})

if __name__ == "__main__":
    app.run(debug=True)