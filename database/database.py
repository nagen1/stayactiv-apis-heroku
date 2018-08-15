# from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# import sys
#
# Base = declarative_base()
#
# class Activities(Base):
#     __tablename__ = 'activities'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30), nullable=False)
#
#
# engine = create_engine('sqlite://stayactiv-v1.db')
# Base.metadata.creaet_all(engine)


from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    iconLink = db.Column(db.String(256))
    createTime = db.Column(DateTime, default=datetime.utcnow)
    createdby = db.Column(db.String(100))
    updateTime = db.Column(DateTime, default=datetime.utcnow)
    updatedby = db.Column(db.String(100))

    # @property
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name
    #     }

class ActivitySchema(ma.ModelSchema):
    class Meta:
        model = Activity

class Exercises(db.Model):
    __tablename__ = 'Exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    muscle = db.Column(db.String, nullable=False)
    routine = db.Column(db.String, nullable=False)
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
    workoutprograms = db.relationship('Activity', backref='workoutprograms', lazy=True)

class WorkoutProgramsSchema(ma.ModelSchema):
    class Meta:
        model = WorkoutPrograms

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
    programroutine = db.relationship("WorkoutPrograms", backref='programRoutines', lazy=True)

class DailyRoutines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Difficulty = db.Column(db.Integer, db.ForeignKey(Exercises.difficulty), nullable=False)
    Duration = db.Column(db.String(4)) # ": "1m",
    ExerciseId = db.Column(db.Integer, db.ForeignKey(Exercises.id), nullable=False) # ": "2",
    ExerciseName = db.Column(db.String, db.ForeignKey(Exercises.name), nullable=False) # ": "Barbell Bench Press",
    Muscle = db.Column(db.Integer, db.ForeignKey(Exercises.muscle), nullable=False) # ": "Chest",
    PreviewLink = db.Column(db.Integer, db.ForeignKey(Exercises.previewLink), nullable=False) # ": "https://www.jefit.com/images/exercises/50_50/8.jpg",
    Reps = db.Column(db.Integer) # ": "8",
    RestTime = db.Column(db.Integer)# ": "60",
    Routine = db.Column(db.Integer, db.ForeignKey(Exercises.routine), nullable=False) # ": "Beginner",
    Sequence = db.Column(db.Integer)# ": "1",
    Sets = db.Column(db.Integer) # ": "3",
    Type = db.Column(db.Integer, db.ForeignKey(Exercises.type), nullable=False)