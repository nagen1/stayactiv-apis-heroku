import requests
import shutil
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
from pathlib import Path
from heroku.database import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
#config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(db_uri)
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# get all the exercise links -
# 'https://www.jefit.com/exercises/bodypart.php?id=11&exercises=All&All=0&Bands=0&Bench=0&Dumbbell=0&EZBar=0&Kettlebell=0&MachineStrength=0&M
# achineCardio=0&Barbell=0&BodyOnly=0&ExerciseBall=0&FoamRoll=0&PullBar=0&WeightPlate=0&Other=0&Strength=0&Stretching=0&Powerlifting=0&OlympicWeightLifting=0&Beginner=0&Intermediate=0&Expert=0&page='+str(i)

data_folder = Path("/Users/nagen/Documents/Python-Workspace/stayactiv-apis/heroku/static/images/exercises")

def getalllinks(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    bsObjTable = bsObj.find("table", {"id":"hor-minimalist_3"})
    linklist = []

    f = open('exerciselinks.txt', 'a')

    for span in bsObjTable.find_all('h4'):
        for a in span.find_all('a', href=True):
            linklist.append(a['href'])
            newlink = 'https://www.jefit.com/exercises/' + a['href']
            f.write(newlink+'\n')

    f.close()

    return None

def getexerciseimages(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    bsObjImgLinks = bsObj.findAll("div", {"class": "col-12 m-2"})

    i = 1
    for link in bsObjImgLinks:

        for atags in link.find_all('a', href=True):
            subLink = atags['href']
            newsublink = subLink[9:]
            newlink = 'https://www.jefit.com/' + newsublink
            print(newlink, i)

            response = requests.get(newlink, stream=True)
            filename = 'something-' + str(i) + '.jpg'
            with open(data_folder / filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            i += 1

    return None

def getexercisedetails(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")

    bsObjexercisedetails = bsObj.findAll("div", {"class": "mt-2 p-2"})
    exercises = database.Exercises()

    urlsplit = url[32:]
    temp = urlsplit.split('/')
    exercises.name = temp[1].replace('-', ' ')

    for new in bsObjexercisedetails:
        for detail in new.find_all('strong'):
            print(detail.text, detail.next_sibling)
            compsss = str(detail.text)

            compStr = compsss.strip()

            if 'Main' in compStr:
                exercises.muscle = detail.next_sibling
            if 'Detailed' in compStr:
                exercises.detailedMuscle = detail.next_sibling
            if 'Other' in compStr:
                exercises.otherMuscle = detail.next_sibling
            if 'Type' in compStr:
                exercises.type = detail.next_sibling
            if 'Machanics' in compStr:
                exercises.mechanics = detail.next_sibling
            if 'Equipment' in compStr:
                exercises.equipment = detail.next_sibling
            if 'Difficulty' in compStr:
                exercises.difficulty = detail.next_sibling

    print(exercises)
    exercises.routine = 'some'
    exercises.previewLink = 'runTime previewLink'
    dbsession.add(exercises)
    dbsession.commit()

    bsObjImgLinks = bsObj.findAll("div", {"class": "col-12 m-2"})

    i = 1
    for link in bsObjImgLinks:

        for atags in link.find_all('a', href=True):
            subLink = atags['href']
            newsublink = subLink[9:]
            newlink = 'https://www.jefit.com/' + newsublink
            print(newlink, i)

            response = requests.get(newlink, stream=True)
            filename = str(exercises.id) + '-' + str(i) + '.jpg'
            with open(data_folder / filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            i += 1

url = 'https://www.jefit.com/exercises/53/Band-Back-Fly'
#getexercisedetails(url)


with open('exerciselinks.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

for url in content:
    getexercisedetails(url)
    print("scrap complete --- ", url)