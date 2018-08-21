from sqlalchemy import create_engine, and_, distinct
from sqlalchemy.orm import sessionmaker
from heroku.database import database
import os
import json
from flask import jsonify
from collections import OrderedDict

from sqlalchemy.ext.declarative import DeclarativeMeta

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
#config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(db_uri)
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
#
# activityone = database.Activity(name="Workout")
# dbsession.add(activityone)
# dbsession.commit()
#
# workoutprogram = database.WorkoutPrograms(name = "12 Fat Burn Program",
#     bodyPart = "FullBody",
#     difficulty = "Beginner",
#     duration = "40",
#     frequency = "4",
#     previewLink = "https://www.jefit.com/images/exercises/50_50/8.jpg",
#     routine = "None",
#     shortDescription = "Sample Beginner Program",
#     type = "Bulking",
#     weeks = "4",
#     activity_id = '3')
# dbsession.add(workoutprogram)
# dbsession.commit()

def generateJson():
    activitieslist = dbsession.query(database.Activity).order_by(database.Activity.name).all()

    activ = []
    worout =[]
    for activity in activitieslist:
        act_dict = {}
        act_dict['name'] = activity.name
        act_dict['id'] = activity.id

        if activity.name == 'Workout':
            i = 0
            workoutprogs = database.WorkoutPrograms.query.all()
            for workoutprog in workoutprogs:
                workout_dict = {}
                workout_dict["id"] = workoutprog.id
                workout_dict["bodyPart"] = workoutprog.bodyPart
                workout_dict["difficulty"] = workoutprog.difficulty
                worout.append(workout_dict)

                progroutines = database.ProgramRoutines.query.filter(database.ProgramRoutines.workoutprogram_id == workoutprog.id)
                prog = []
                j = 0
                for progroutine in progroutines:
                    prog_dict = {}
                    prog_dict['id']=progroutine.id
                    prog_dict['Musle'] = progroutine.Musle
                    prog_dict['Week'] = progroutine.Week
                    prog.append(prog_dict)

                    daily = []
                    dailyroutines = database.DailyRoutines.query.filter(database.DailyRoutines.programroutine_id == progroutine.id)
                    for dailyroutine in dailyroutines:
                        daily_dict = {}
                        daily_dict['Difficulty'] = dailyroutine.id
                        daily_dict['ExerciseName'] = dailyroutine.ExerciseName
                        daily.append(daily_dict)

                    act_dict["Workout"] = worout
                    act_dict["Workout"][i]["ProgramRoutine"] = prog
                    act_dict["Workout"][i]["ProgramRoutine"][j]["Daily"] = daily
                    j += 1
                i += 1
        activ.append(act_dict)

    activity = {}
    activity["activity"] = activ
    jsonobj = json.dumps(activity)
    print(jsonobj)



def generatenewJson():
    activities = database.Activity.query.all()
    activities_dict = [activ.as_dict() for activ in activities]
    i = 0
    for activity in activities_dict:
        if activity['name'] == 'Workout':
            workoutprogs = database.WorkoutPrograms.query.all()
            workoutprogs_dict = [workout.as_dict() for workout in workoutprogs]
            activities_dict[i]['Workout'] = workoutprogs_dict
        i += 1

    activity = {}
    activity["activity"] = activities_dict
    jsonobj = json.dumps(activity)
    #print(jsonobj)

    return jsonify({'actibities': activity})

newjob = generatenewJson()

activitylist = newjob['activity']

print(newjob)

#generateJson()
#
# programroutine = database.ProgramRoutines(Day = "1",
#                                           Duration='40',
#                                           Musle='Sholders',
#                                           PreviewLink='https://www.jefit.com/images/exercises/50_50/32.jpg',
#                                           RoutineId = '1',
#                                           Sequence = '3',
#                                           Week = '1',
#                                           workoutprogram_id='1')
#
# dailyrout = database.DailyRoutines(
#     Difficulty='Difficulty',
# Duration = "1m",
# ExerciseId = "2",
# ExerciseName = "Dumble Press",
# Muscle = "Chest",
# PreviewLink = "https://www.jefit.com/images/exercises/50_50/8.jpg",
# Reps = "8",
# RestTime = "60",
# Routine = "Beginner",
# Sequence = "1",
# Sets = "3",
# Type = "Beginner",
# programroutine_id = '1')
#
# dbsession.add(dailyrout)
# dbsession.commit()
#
# #
# dailyroutine = database.Activity.query.all()
# results = [daily.as_dict() for daily in dailyroutine ]
# print(results)
# # for daily in dailyroutine:
# #     print(daily.ExerciseName)