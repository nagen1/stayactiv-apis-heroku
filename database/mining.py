import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
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

# https://www.jefit.com/routines/workout-routine-database.php?id=31531

# https://www.jefit.com/routines/?name=1&tag=1&keyword=0&gender=0&sort=3&search=&page=1

def getalllinks(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    bsObjTable = bsObj.find("table", {"id":"hor-minimalist_3"})
    linklist = []
    for span in bsObjTable.find_all('span'):
        for a in span.find_all('a', href=True):
            linklist.append(a['href'])

    for one in linklist:
        if 'workout-routine' not in one:
            linklist.remove(one)

    mylist = list(set(linklist))

    return mylist

def getprograms(url):
    url = 'https://www.jefit.com/routines/' + url
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    workoutprog = bsObj.find('div', {'class': 'col-8'})
    bsObjTables = bsObj.find_all("table", {"id": "hor-minimalist_3"})

    workoutprogObj = workoutprog.findAll('strong')

    # for strong in workoutprogObj:
    #     print(strong.nextSibling)
    # strong - workout name = [0
    # frequency = [3
    # Type = [5
    # Difficulty = [6
    newlist = []
    workoutprogam = database.WorkoutPrograms()
    workoutprogam.activity_id = '3'
    print(workoutprogObj[0].nextSibling)
    workoutprogam.name = workoutprogObj[0].nextSibling

    try:
        frequency = workoutprogObj[3].nextSibling
        frequent = re.findall(r'\d+', frequency)
        workoutprogam.frequency = frequent[0]
    except:
        pass
    print(workoutprogObj[3].nextSibling)

    print(workoutprogObj[5].nextSibling)
    progtype = workoutprogObj[5].nextSibling
    workoutprogam.type = progtype

    print(workoutprogObj[6].nextSibling)
    difficulty = workoutprogObj[6].nextSibling
    workoutprogam.difficulty = difficulty
    newlist.append(workoutprogam)

    dbsession.add(workoutprogam)
    dbsession.commit()

    daynum = 0
    progseq = 0
    for table in bsObjTables:
        day = ''
        dailyseq = 0

        progRot = database.ProgramRoutines()
        for row in table.findAll("tr"):
            cells = row.findAll("td")

            if len(cells) == 2:
                if day != cells[0].find(text=True):
                    day = cells[0].find(text=True)
                    progseq += 1
                    progRot.Sequence = progseq

                    if day == "Monday":
                        daynum = 1
                    elif day == 'Tuesday':
                        daynum = 2
                    elif day == 'Wednesday':
                        daynum = 3
                    elif day == 'Thursday':
                        daynum = 4
                    elif day == 'Friday':
                        daynum = 5
                    elif day == 'Saturday':
                        daynum = 6
                    elif day == 'Sunday':
                        daynum = 7
                    elif day == 'Any' or day == 'ANY':
                        daynum += 1
                    else:
                        try:
                            daynum = re.findall(r'\d+', day)
                            daynum = daynum[0]
                            print(daynum)
                        except:
                            pass

                    progRot.Day = daynum
                    muscle = cells[1].find(text=True)
                    progRot.Musle = muscle

            progRot.Day = daynum
            progRot.workoutprogram_id = workoutprogam.id
            dbsession.add(progRot)
            dbsession.commit()


            if len(cells) >= 6:
                if cells[0].find(text=True) not in ('Muscle', 'Exercise Name', 'Timer', 'Reps','Sets', 'Track','\n'):
                    Muscle = cells[0].find(text=True)
                    dailyRot = database.DailyRoutines()
                    print(Muscle)
                    dailyRot.Muscle = Muscle

                    dailyseq += 1
                    dailyRot.Sequence = dailyseq

                if cells[3].find(text=True) not in ('Muscle', 'Exercise Name', 'Timer', 'Reps','Sets', 'Track','\n'):
                    Timeers = cells[3].find(text=True)

                    if 'min' not in Timeers:
                        Timeers = re.findall(r'\d+', Timeers)
                        Timeers = int(Timeers[0])
                        print(Timeers)
                    else:
                        Timeers = re.findall(r'\d+', Timeers)
                        Timeers = int(Timeers[0]) * 60
                        print(Timeers)
                    dailyRot.Duration = Timeers

                if cells[4].find(text=True) not in ('Muscle', 'Exercise Name', 'Timer', 'Reps','Sets', 'Track', '\n'):
                    Reps = cells[4].find(text=True)
                    print(Reps)
                    dailyRot.Reps = Reps

                if cells[5].find(text=True) not in ('Muscle', 'Exercise Name', 'Timer', 'Reps','Sets', 'Track', '\n'):
                    Sets = cells[5].find(text=True)
                    try:
                        newSet1 = re.findall(r'\d+', Sets)
                        if len(newSet1) != 0:
                            newSet1 = newSet1[0]
                            print(newSet1)
                            dailyRot.Sets = int(newSet1)

                    except:
                        pass

                if cells[2].find('a'):
                    dailyRot.ExerciseName = cells[2].find('a').text

                if cells[1].find('img'):
                    imagelink = cells[1].find('img')  #image
                    imagelink = imagelink['src']
                    imagelink = imagelink[2:]
                    previewLink = 'https://www.jefit.com' + imagelink
                    dailyRot.PreviewLink = previewLink

                    dailyRot.Difficulty = difficulty
                    dailyRot.ExerciseId = 1
                    dailyRot.Type = progtype
                    dailyRot.Routine = difficulty
                    dailyRot.RestTime = 60
                    dailyRot.programroutine_id = progRot.id
                    dbsession.add(dailyRot)
                    dbsession.commit()


            print("something")

    # for table in bsObjTables:
    #     rows = table.findAll(lambda tag: tag.name=='tr')
    #     # data = [[td.findNext(text=True) for td in tr.findAll("td")] for tr in rows]
    #     for tr in rows:
    #         for td in tr.findAll('td'):
    #             new = td.findNext(text=True)
    #             new2 = re.findall(r'\d+', new)
    #             print(new2)

x = 1
newList = []
while x <= 5:
    url = "https://www.jefit.com/routines/?name=1&tag=1&keyword=0&gender=0&sort=3&search=&page=" + str(x)
    newList.append(getalllinks(url))
    x += 1
updateList = newList[0]+newList[1]+newList[3]+newList[4]+newList[2]
print(updateList)
for new in updateList:
    getprograms(new)


# https://www.jefit.com/routines/workout-routine-database.php?id=31531