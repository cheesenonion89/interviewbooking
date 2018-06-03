from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from config import Config
from resources import NewInterviewer, Interviewer, Interviewers, NewInterviewee, Interviewee, Interviewees, Availability
from service import db_service

"""
Entry point. Setup for the server and the API endpoints.
"""

# Create app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db_service.init_db()

# Fill the database with mockup data for testing
db_service.mockup()

# Setup REST endpoints‚
CORS(app)
api = Api(app)

# Endpoints to manage interviewers and interviewees
api.add_resource(NewInterviewer, '/interviewer/add')
api.add_resource(Interviewer, '/interviewer/<id>')
api.add_resource(Interviewers, '/interviewers')
api.add_resource(NewInterviewee, '/interviewee/add')
api.add_resource(Interviewee, '/interviewee/<id>')
api.add_resource(Interviewees, '/interviewees')

# Endpoints to get availability
api.add_resource(Availability, '/availability')

# Run app
app.run()
