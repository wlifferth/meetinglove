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
        if self.db.execute("SELECT adminKey FROM meeting WHERE meetingKey=%s", (meetingKey)).fetchone()[0] == adminKey:
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
        else:
            print("ERROR")


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
