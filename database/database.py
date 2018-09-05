from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema

template_dir = os.path.join(os.path.dirname(__file__))
new = template_dir[:-9]
templates = new + '/templates'
statics = new + '/static'

#app = Flask(__name__)
app = Flask(__name__, template_folder=templates, static_folder=statics)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
        }
        return obj_d

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    iconLink = db.Column(db.String(256))
    previewLink = db.Column(db.String(256))
    createTime = db.Column(DateTime, default=datetime.utcnow)
    createdby = db.Column(db.String(100))
    updateTime = db.Column(DateTime, default=datetime.utcnow)
    updatedby = db.Column(db.String(100))

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'iconLink': self.iconLink,
            'previewLink': self.previewLink
        }
        return obj_d

class Exercises(db.Model):
    __tablename__ = 'Exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    muscle = db.Column(db.String, nullable=False)
    detailedMuscle = db.Column(db.String)
    routine = db.Column(db.String, nullable=False)
    otherMuscle = db.Column(db.String)
    mechanics = db.Column(db.String)
    equipment = db.Column(db.String)
    previewLink = db.Column(db.String, nullable=False)
    createdDate = db.Column(DateTime, default=datetime.utcnow)
    updatedDate = db.Column(DateTime, onupdate=datetime.utcnow)

class WorkoutPrograms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) # 4 weeks Beginner Program"
    bodyPart = db.Column(db.String(50)) # ": "FullBody",
    difficulty = db.Column(db.String(50)) # ": "Beginner",
    duration = db.Column(db.Integer) # ": "40",
    frequency = db.Column(db.Integer) # ": "4",
    previewLink = db.Column(db.String(250)) # ": "https://www.jefit.com/images/exercises/50_50/8.jpg",
    routine = db.Column(db.String(50)) # ": "None",
    shortDescription = db.Column(db.String(50)) # ": "Sample Beginner Program",
    type = db.Column(db.String(50)) # ": "Bulking",
    weeks = db.Column(db.Integer) # ": "4"
    activity_id = db.Column(db.Integer, db.ForeignKey(Activity.id), nullable=False)
    activity = db.relationship('Activity', backref='workoutprograms')


    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'bodyPart': self.bodyPart,
            'difficulty': self.difficulty,
            'duration': self.duration,
            'frequency': self.frequency,
            'previewLink': self.previewLink,
            'routine': self.routine,
            'shortDescription': self.shortDescription,
            'type': self.type,
            'weeks': self.weeks,
        }
        return obj_d


class ProgramRoutines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Day = db.Column(db.Integer) # ": "1",
    Duration = db.Column(db.Integer)  # ": "40",
    Musle = db.Column(db.String(50)) # ": "Chest and tricepts",
    PreviewLink = db.Column(db.String(250)) # ": "https://www.jefit.com/images/exercises/50_50/32.jpg",
    RoutineId = db.Column(db.Integer)  # ": "123",
    Sequence = db.Column(db.Integer)  # ": "1",
    Week = db.Column(db.Integer)  # ": "1"
    workoutprogram_id = db.Column(db.Integer, db.ForeignKey(WorkoutPrograms.id), nullable=False)
    workoutprograms = db.relationship("WorkoutPrograms", backref='programroutines')


class DailyRoutines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Difficulty = db.Column(db.Integer, db.ForeignKey(Exercises.difficulty), nullable=False)
    Duration = db.Column(db.String(4)) # ": "1m",
    ExerciseId = db.Column(db.Integer, db.ForeignKey(Exercises.id), nullable=False) # ": "2",
    ExerciseName = db.Column(db.String, nullable=False) # ": "Barbell Bench Press",
    Muscle = db.Column(db.Integer, nullable=False) # ": "Chest",
    PreviewLink = db.Column(db.Integer, nullable=False) # ": "https://www.jefit.com/images/exercises/50_50/8.jpg",
    Reps = db.Column(db.Integer) # ": "8",
    RestTime = db.Column(db.Integer)# ": "60",
    Routine = db.Column(db.Integer, nullable=False) # ": "Beginner",
    Sequence = db.Column(db.Integer) # ": "1",
    Sets = db.Column(db.Integer) # ": "3",
    Type = db.Column(db.Integer, nullable=False)
    programroutine_id = db.Column(db.Integer, db.ForeignKey(ProgramRoutines.id), nullable=False)
    programroutine = db.relationship("ProgramRoutines", backref='dailyRoutines', lazy=True)


class ExercisesSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", 'type', "difficulty", "muscle", 'detailedMuscle', 'otherMuscle', 'mechanics', 'equipment')

class DailyRoutinesSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'Difficulty', 'Duration', 'ExerciseId', 'ExerciseName', 'Muscle', 'PreviewLink',
                  'Reps', 'RestTime', 'Routine', 'Sets', 'Type', 'programroutine_id', 'Sequence')

class ProgramRoutinesSchema(ma.ModelSchema):
    dailyRoutines = fields.Nested(DailyRoutinesSchema, many=True)
    class Meta:
        fields = ('id', 'Day', 'Duration', 'Musle', 'PreviewLink',
                  'RoutineId', 'Sequence', 'workoutprogram_id', 'Week', 'dailyRoutines')

class WorkoutProgramsSchema(ma.ModelSchema):
    programroutines = fields.Nested(ProgramRoutinesSchema, many=True)
    class Meta:
        fields = ('id', 'name', 'bodyPart', 'difficulty', 'duration', 'frequency', 'previewLink',
                  'routine', 'shortDescription', 'type', 'weeks', 'activity_id', 'programroutines')

class ActivitySchema(ma.ModelSchema):
    workoutprograms = fields.Nested(WorkoutProgramsSchema, many=True)
    class Meta:
        fields = ("id", "name", 'iconLink', "previewLink", "workoutprograms")
    # class Meta:
    #     model = Activity

class OnlyActivitiesSchema(ma.ModelSchema):
    class Meta:
        fields = ("id", "name", 'iconLink', "previewLink")

