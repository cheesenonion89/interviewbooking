# Flask REST API for Interview booking

This repository contains a simple flask sever that exposes a REST API to manage
lists of interviewers and interviewees, together with their availabilities to
arrange interviews between a set of interviewers and an interviewer at a time
slot where all parties are available. The availability for a certain time frame
is encoded as a bit string, where each bit represents the availability at a time
slot. If, for example, a meeting for a time range of 5 days is planned and the
availabilities for each day is separated by 30 minute frames between 6 am and 6pm,
a bit string of length 5 x 24 = 120 bits represents the availabilities, where 1
represents the availability of a person and 0 the unavailability. The leftmost bit
is interpreted as the first time slot (6 am, Monday in the example), the second
would be 6:30 pm and so on.

The database is filled with 5 interviewers and interviewees with availabilities
as stated above for testing purposes. The datasets added by default can be
observed in the mockup() function in /service/db_service.py.

# Running the server

To run the server, install the latest python 3 version together with pip.

Install the required packages by running
```
pip3 install -r requirements.txt
```

To run the server, run
```
python3 app.py
```

The server should now be running on localhost:5000 and the REST Api is available.

# Accessing the REST API

In the following the REST endpoints are listed and the corresponding HTTP requests
are listed. Data for testing the REST funtionality can be found in test/RESTtests.txt

## /interviewer/new & interviewee/new
### POST
* Creation of a new interviewer/interviwee
* Expects a json object containing the first name, last name and email address of a new interviewer/interviewee. The avalability is optional.

## /interviewer/<id> & interviewee/<id>
### GET
* Get the interviewer/interviewee with the database id <id>. Interviewers/Interviewee with ids 1-5 are created by default for testing.
* Expects the interviewer id as part of the URL

### PUT
* Updates the interviewer with id <id>.
* Expects a json object with any of the keys first_name, last_name, email and/or availability. All provided fields will be updated if the interviewer exists

### DELETE
* Deletes the interviewer with id <id>

## /interviewers & /interviewer_email
### GET
* Returns a list of all interviewers/interviewees in the database.

## /availability
### POST
* Expects a json object with the keys interviewee_email and interviewer_emails containing the email of an interviewee in the database and a list of email addresses of interviewers in the database and returns the bitstring encoding the common available time slots.
