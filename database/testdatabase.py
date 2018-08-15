from sqlalchemy import create_engine, and_, distinct
from sqlalchemy.orm import sessionmaker
from database import Activity
import os
import json
from flask import jsonify
from collections import OrderedDict

from sqlalchemy.ext.declarative import DeclarativeMeta

path = os.path.dirname(__file__)
print("os.path.dirname" + path)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
print("db path" + db_path)

db_uri = 'sqlite:///{}'.format(db_path)

engine = create_engine(db_uri)
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# activityone = database.Activity(name="Meditation")
# dbsession.add(activityone)
# dbsession.commit()

activitieslist = dbsession.query(Activity).order_by(Activity.name).all()

for activity in activitieslist:
    print(activity.name)

