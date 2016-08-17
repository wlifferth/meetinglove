import sqlalchemy
from datetime import datetime
from generateKey import generateKey

"""
meeting:
    meetingKey
    meetingName
    adminKey
    creationTimeStamp

person:
    personKey
    meetingKey
    personName

meetingTime:
    meetingTimeKey
    meetingKey
    startTime
    stopTime

avail:
    availKey
    meetingKey
    personKey
"""

dbInfo = {
    "hostname": "meetinglove.cloudsproutdesign.com",
    "dbname": "meetinglove",
    "username": "wlifferth",
    "password": "qqe8PrP381"
}


class DBConnection():
    def __init__(self):
        hostname = "meetinglove.cloudsproutdesign.com"
        dbname = "meetinglove"
        username = "wlifferth"
        password = "qqe8PrP381"
        self.db = sqlalchemy.create_engine('mysql://{}:{}@{}/{}'.format(username, password, hostname, dbname))

    def addMeeting(self, meetingName):
        meetingKey = generateKey(20)
        adminKey = generateKey(20)
        creationTimeStamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("INSERT INTO meeting VALUES(%s, %s, %s, %s)", (meetingKey, meetingName, adminKey, creationTimeStamp))
        return Meeting(meetingKey, meetingName, adminKey)

    def getMeeting(self, meetingKey):
        meetingRow = self.db.execute("SELECT * FROM meeting WHERE meetingKey='{}'".format(meetingKey)).fetchone()
        return Meeting(meetingRow[0], meetingRow[1], creationTimeStamp=meetingRow[3])

    def addMeetingTime(self, meetingKey, adminKey, startTime):
        meetingTimeKey = generateKey(20)
        if self.db.execute("SELECT adminKey FROM meeting WHERE meetingKey=%s", (meetingKey)).fetchone()[0] == adminKey and not self.db.execute("SELECT * FROM meetingTime WHERE startTime=%s", (startTime)).fetchall():
            self.db.execute("INSERT INTO meetingTime VALUES(%s, %s, %s)", (meetingTimeKey, meetingKey, startTime))
            return MeetingTime(meetingTimeKey, meetingKey, startTime)
        else:
            return None

    def getMeetingTimes(self, meetingKey):
        meetingTimes = self.db.execute("SELECT * FROM meeting RIGHT JOIN meetingTime ON meeting.meetingKey=meetingTime.meetingKey WHERE meeting.meetingKey=%s GROUP BY meetingTime.startTime", (meetingKey)).fetchall()
        for meetingTime in meetingTimes:
            meetingTime = MeetingTime(meetingTime[4], meetingTime[5], meetingTime[6])
        return meetingTimes

    def deleteMeetingTime(self, meetingKey, adminKey, meetingTimeKey):
        if self.db.execute("SELECT adminKey FROM meeting WHERE meetingKey=%s", (meetingKey)).fetchone()[0] == adminKey:
            print("DELETE FROM meetingTime WHERE meetingTimeKey='{}'".format(meetingTimeKey))
            self.db.execute("DELETE FROM meetingTime WHERE meetingTimeKey=%s", (meetingTimeKey))

    def addPerson(self, meetingKey, personName):
        personKey = generateKey(20)
        while self.db.execute("SELECT COUNT(1) FROM person WHERE personKey=%s", (personKey)) == 1:
            personKey = generateKey(20)
        self.db.execute("INSERT INTO person VALUES (%s, %s, %s)", (personKey, meetingKey, personName))

    def getPersons(self, meetingKey):
        # Get all the rows of person that have the correct meetingKey
        persons = self.db.execute("SELECT * FROM person WHERE meetingKey=%s", (meetingKey)).fetchall()
        # Returns a list of Person objects
        return [Person(person[0], person[1], person[2]) for person in persons]

    def getAvails(self, meetingKey, personKey):
        self.db.execute("SELECT * FROM person WHERE meetingKey=%s RIGHT JOIN avail ON person.personKey=avail.personKey RIGHT JOIN  meetingTime ON avail.meetingTimeKey=meetingTime.meetingTimeKey", (meetingKey))


class Meeting():
    def __init__(self, meetingKey, name, adminKey=None, creationTimeStamp=None):
        self.meetingKey = meetingKey
        self.name = name
        self.adminKey = adminKey
        self.creationTimeStamp = creationTimeStamp

class MeetingTime():
    def __init__(self, meetingTimeKey, meetingKey, startTime):
        self.meetingTimeKey = meetingTimeKey
        self.meetingKey = meetingKey
        self.startTime = startTime

class Person():
    def __init__(self, personKey, meetingKey, personName):
        self.personKey = personKey
        self.meetingKey = meetingKey
        self.personName = personName
