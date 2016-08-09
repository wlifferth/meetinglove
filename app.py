#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import redirect
from flask import jsonify
from flask import request
from random import SystemRandom
import string
from datetime import datetime

from generateKey import generateKey
from models import DBConnection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/newMeeting/<string:meetingName>", methods=["POST"])
def new(meetingName):
    dbConnection = DBConnection()
    meeting = dbConnection.addMeeting(meetingName=meetingName)
    return redirect("/meeting/{}/admin/{}".format(meeting.meetingKey, meeting.adminKey))


@app.route("/meeting/<string:meetinKey>")
def meeting(meetingKey):
    pass


@app.route("/meeting/<string:meetingKey>/admin/<string:adminKey>")
def meetingAdmin(meetingKey, adminKey):
    # Open database connection
    dbConnection = DBConnection()
    # Get the basic meeting information from the database
    meeting = dbConnection.getMeeting(meetingKey)
    return render_template("adminDashboard.html", meetingName=meeting.name, meetingKey=meetingKey, adminKey=adminKey)

@app.route("/addMeetingTime")
def addMeetingTime():
    # Collect the arguments from the request
    meetingKey = request.args.get('meetingKey')
    adminKey = request.args.get('adminKey')
    newMeetingTime = request.args.get('meetingTime')
    # Open database connection
    dbConnection = DBConnection()
    # Create the new meeting time in the database
    newMeetingTime = dbConnection.addMeetingTime(meetingKey, adminKey, newMeetingTime)
    # Get all the meetingTimes so we can return them to the ajax caller
    meetingTimes = dbConnection.getMeetingTimes(meetingKey)
    # Turn meetingTime (an array of MeetingTime objects) into an array of timestamps
    meetingTimes = [(x.startTime, x.meetingTimeKey) for x in meetingTimes]
    # Return the array as jsonified object
    return jsonify(meetingTimes=meetingTimes)


@app.route("/getMeetingTimes")
def getMeetingTimes():
    # Collect the arguments from the request
    meetingKey = request.args.get('meetingKey')
    # Open database conneciton
    dbConnection = DBConnection()
    # Get all the meetingTimes so we can return them to the ajax caller
    meetingTimes = dbConnection.getMeetingTimes(meetingKey)
    # Turn meetingTime (an array of MeetingTime objects) into an array of timestamps
    meetingTimes = [(x.startTime, x.meetingTimeKey) for x in meetingTimes]
    # Return the array as a jsonified object
    return jsonify(meetingTimes=meetingTimes)

@app.route("/deleteMeetingTime")
def deleteMeetingTime():
    # Collect the arguments from the request
    meetingKey = request.args.get('meetingKey')
    adminKey = request.args.get('adminKey')
    meetingTimeKey = request.args.get('meetingTimeKey')
    # Open database connection
    dbConnection = DBConnection()
    # Delete the meeting time with the meeting key
    dbConnection.deleteMeetingTime(meetingKey, adminKey, meetingTimeKey)
    # Get all the meetingTimes so we can return them to the ajax caller
    meetingTimes = dbConnection.getMeetingTimes(meetingKey)
    # Turn meetingTime (an array of MeetingTime objects) into an array of timestamps
    meetingTimes = [(x.startTime, x.meetingTimeKey) for x in meetingTimes]
    # Return the array as a jsonified object
    return jsonify(meetingTimes=meetingTimes)


if __name__ == "__main__":
    app.run()
