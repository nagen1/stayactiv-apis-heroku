import os
import sys
sys.path.append('/app/app.py')
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from datetime import datetime
from taskJson import workoutJson
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database import database # Always uncomment this before deploying in heroku
#from heroku.database import database # Always comment this before deploying in heroku
from sqlalchemy import create_engine, and_, distinct
from sqlalchemy.orm import sessionmaker


app = database.app
app.secret_key = 'super_secret_key_230742'

# db_path = os.path.join(os.path.dirname(__file__), 'database/app.db')
# db_uri = 'sqlite:///{}'.format(db_path)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# engine = create_engine(db_uri)
# DBSession = sessionmaker(bind=engine)

dbsession = database.db #DBSession()


@app.route('/')
def home():
    return render_template(
         'index.html',
        # title='Home Page',
        # year=datetime.now().year
    )


# ------------------------- Only APIs ---------------------------------

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
        newlist = database.Activity.query.all()
        activities_schema = database.OnlyActivitiesSchema(many=True)
        output = activities_schema.dump(newlist).data

    except:
        output = "No Results Found"

    return jsonify({"Activities": output})


# This will deliver the list of activities, workouts and routine in one single Json
# Effective when used, app goes offline or initial app installation time. Page 1 will be saved along with it
@app.route('/api/v1/miniJson/<int:page>', methods=['GET'])
def minijson(page):
    try:
        # activlist = database.Activity.query.all()
        # activity_schema = database.ActivitySchema(many=True)
        # output = activity_schema.dump(activlist).data
        newlist = []
        allactlist = database.Activity.query.all()
        for activity in allactlist:
            newlist.append(database.Activity.as_dict(activity))
        workoutprogs = database.WorkoutPrograms.query.paginate(page, 10, False)
        records = workoutprogs.items
        workout_schema = database.WorkoutProgramsSchema(many=True)
        output = workout_schema.dump(records).data
        newlist[2]['WorkoutPrograms'] = output

    except:
        output = 'NoResultFound'

    return jsonify({'Activities': newlist})

@app.route('/api/v1/workoutprograms/<int:page>', methods=['GET'])
def workoutprog(page):
    try:
        workoutprogs = database.WorkoutPrograms.query.paginate(page, 10, False)
        records = workoutprogs.items
        workout_schema = database.WorkoutProgramsSchema(many=True)
        output = workout_schema.dump(records).data

    except:
        output = "No Results Found"

    return jsonify({"Workout Programs": output})

@app.route('/api/v1/programroutine', methods=['GET'])
def progroutine():
    try:
        progroutines = database.ProgramRoutines.query.all()
        program_schema = database.ProgramRoutinesSchema(many=True)
        output = program_schema.dump(progroutines).data
    except:
        output = "No Results Found"

    return jsonify({"Program Routine": output})

@app.route('/api/v1/exercises/<int:page>', methods=['GET'])
def exercises(page):
    try:
        exercisesList = database.Exercises.query.paginate(page, 10, False)
        records = exercisesList.items
        exercise_schema = database.ExercisesSchema(many=True)
        output = exercise_schema.dump(records).data

    except:
        output = "No Results Found"

    return jsonify({"Exercises": output})

# ------------------------- Only APIs Code End ---------------------------------


# ------------------------- Web site with UI ---------------------------------

@app.route('/workoutprograms')
def workoutprogam():
    try:
        # list = dbsession.session.query(database.WorkoutPrograms).order_by(database.WorkoutPrograms.createdDate).limit(5).all()
        list = dbsession.session.query(database.WorkoutPrograms).order_by(database.WorkoutPrograms.createdDate).all()
    except NoResultFound:
        None

    return render_template('/workouts/woindex.html', wolist=list)


@app.route('/workoutprograms/new', methods=['GET', 'POST'])
def createwop():
    if request.method == 'POST':
        createWorkoutProgram = database.WorkoutPrograms()
        createWorkoutProgram.name = request.form['title']
        createWorkoutProgram.bodyPart = request.form['bodyPart']
        createWorkoutProgram.difficulty = request.form['difficulty']
        createWorkoutProgram.duration = request.form['duration']
        createWorkoutProgram.frequency = request.form['frequency']
        createWorkoutProgram.previewLink = request.form['previewLink']
        createWorkoutProgram.routine = request.form['routine']
        createWorkoutProgram.shortDescription = request.form['shortDescription']
        createWorkoutProgram.type = request.form['type']
        createWorkoutProgram.weeks = request.form['weeks']
        createWorkoutProgram.activity_id = 3

        dbsession.session.add(createWorkoutProgram)
        dbsession.session.commit()

        flash("Workout Program created Successfully!", "Workout")
        return redirect(url_for('workoutprogam'))

    if request.method == 'GET':
        return render_template('/workouts/createwo.html')

@app.route('/workoutprograms/details/<int:id>', methods=['GET', 'POST'])
def wodetails(id):

    try:
        wodetail = database.WorkoutPrograms.query.filter(database.WorkoutPrograms.id == id).one()
    except:
        wodetail = 'No Reulst Found'

    try:
        routine = database.ProgramRoutines.query.filter(database.ProgramRoutines.workoutprogram_id == id).all()
    except:
        None

    if request.method == 'POST':
        createroutine = database.ProgramRoutines()
        createroutine.workoutprogram_id = id
        createroutine.Duration = request.form['Duration']
        createroutine.Day = request.form['Day']
        createroutine.Musle = request.form['Musle']
        createroutine.PreviewLink = request.form['PreviewLink']
        createroutine.Sequence = request.form['Sequence']
        createroutine.Week = request.form['Week']

        dbsession.session.add(createroutine)
        dbsession.session.commit()

        return redirect(url_for('wodetails', id=id, wodetail=wodetail, routine=routine))

    else:

        return render_template('/workouts/wodetails.html', wodetail=wodetail, routine=routine)


@app.route('/workoutprograms/routine/details/<int:id>', methods=['GET', 'POST'])
def routineDetails(id):

    try:
        routine = database.ProgramRoutines.query.filter(database.ProgramRoutines.id == id).one()
    except:
        None

    try:
        wodetails = database.WorkoutPrograms.query.filter(database.WorkoutPrograms.id == routine.workoutprogram_id).one()
    except:
        None
    try:
        daily = database.DailyRoutines.query.filter(database.DailyRoutines.programroutine_id == id).all()
        # exercisesList = dbsession.session.query(database.Exercises.muscle).distinct()
        exercisesList = dbsession.session.query(database.Exercises).order_by(database.Exercises.muscle).all()
    except:
        None

    if request.method == 'POST':
        ExerciseId = request.form['ExerciseId']
        exercise = database.Exercises.query.filter(database.Exercises.id == ExerciseId).one()
        daily = database.DailyRoutines()
        daily.Difficulty = exercise.difficulty
        daily.Duration = request.form['Duration']
        daily.ExerciseId = ExerciseId
        daily.ExerciseName = exercise.name
        daily.Muscle = exercise.muscle
        daily.PreviewLink = exercise.previewLink
        daily.Reps = request.form['Reps']
        daily.RestTime = request.form['RestTime']
        daily.Routine = exercise.routine
        daily.Sequence = request.form['Sequence']
        daily.Sets = request.form['Sets']
        daily.Type = exercise.type
        daily.programroutine_id = id

        dbsession.session.add(daily)
        dbsession.session.commit()

        return redirect(url_for('routineDetails', routineDetails=routine, wodetails=wodetails, muscle=exercisesList, daily=daily))
    else:
        return render_template('/routine/routinedetails.html', routineDetails=routine, wodetails=wodetails, muscle=exercisesList, daily=daily)


if __name__ == "__main__":
    app.run(debug=True)