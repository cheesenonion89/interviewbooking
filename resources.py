from flask import request
from flask_restful import Resource
from controller import interviewer_controller as interviewer_ctrl, interviewee_controller as interviewee_ctrl
from service import availability_service

"""
The Resources module defines 
"""
class Availability(Resource):
    def post(self):
        """
        POST endpoint, receives a json object containing a list of interviewer email addresses, an interviewee email
        adress. From the email adresses the availabilities are obtained from the db_service and the
        availability_service is used to compute a set of common time slots
        :return: json
        """
        # Get the json data from the request body
        data = request.get_json()
        na_interviewers = []    # list to collect email addresses that belong to no interviewer
        na_availabilities = []  # list of interviewers that have no availability information
        interviewer_availabilities = [] # list to collection availabilities from invertviewers

        # Validate that the json object contains the fields interviewee_email and interviewer_emails
        if 'interviewee_email' not in data:
            return "Interviewee Email is missing", 400
        elif 'interviewer_emails' not in data:
            return "At least one interviewer mail must be provided", 400

        # Validate that there is an interviewer in the database with the provided email adress
        interviewee_email = data["interviewee_email"]
        interviewee = interviewee_ctrl.get_interviewee_by_email(interviewee_email)

        # If the interviewer is not in the database or has no availability information, return an error message
        if not interviewee:
            return "The interviewee with the email %s does not exist" % data["interviewee_email"], 400

        elif not interviewee.availability:
            return "There is no availability information for the intervieweee %s" % interviewee_email, 400

        # Validate interviewer data
        interviewer_emails = data["interviewer_emails"]

        # If list of interviewer emails is empty return an error
        if not interviewer_emails:
            return "At least one interviewer email must be provided", 400
        # Collect all non existent interviewers or interviewers without availability information
        else:
            for interviewer_email in interviewer_emails:
                if not interviewer_ctrl.get_interviewer_by_email(interviewer_email):
                    na_interviewers.append(interviewer_email)
                elif not interviewer_ctrl.get_interviewer_by_email(interviewer_email).availability:
                    na_availabilities.append(interviewer_email)
                else:
                    interviewer_availabilities.append(interviewer_ctrl.get_availability_by_email(interviewer_email))

        # If there are missing interviewers or missing availability information for interviewers emails,
        # return the list of emails for which data is missing with an error
        response_msg = ""
        if na_interviewers:
            response_msg = "The following interviewers do not exist: %s. " % na_interviewers
        if na_availabilities:
            response_msg += "There are no availability information for the following interviewers: %s" % na_availabilities
        if na_interviewers or na_availabilities:
            return response_msg, 400

        # If interviewee and interviewee information is valid, compute the common availabilities
        else:
            availability = availability_service.get_available_time_slots(interviewer_availabilities,
                                                                         interviewee.availability)
            if not availability:
                return "There is no common time slot for the provided list of interviewers with the interviewee.", 200
            else:
                return availability, 200


class NewInterviewer(Resource):
    def post(self):
        """
        POST interface to create a new interviewer. Receives a json object containing the email, first_name and
        last_name of the new interviewer. The availability information in optional. It can be updated via the PUT
        interface in the Interviewer resource.
        :return:
        """
        # Get the json data from the request body and check for the required fields
        data = request.get_json()
        if 'email' not in data:
            response = "Missing argument 'email'", 400
        elif 'first_name' not in data:
            response = "Missing argument 'first_name'", 400
        elif 'last_name' not in data:
            response = "Missing argument 'last_name'", 400
        # If the required fields are available, create a new interviewer and add it to the database.
        else:
            if 'availability' not in data:
                availability = None
            else:
                availability = data["availability"]
            interviewer = interviewer_ctrl.create_interviewer(data["email"], data["first_name"], data["last_name"],
                                                              availability)
            if not interviewer:
                response = "Interviewer with email %s already exists" % data["email"], 406
            else:
                response = interviewer, 200
        return response


class Interviewer(Resource):
    def get(self, id):
        """
        GET interface to retrieve the interviewer information for a specific interviewer by the database id, which is
        automatically assigned at creation.
        :param id: unique database id of the interviewer to be retrieved
        :return:
        """
        # Get the interviewer data from the database
        interviewer = interviewer_ctrl.get_interviewer_by_id(id)
        # If there is an interviewer with the requested id, return the data as json object, else return an error
        if interviewer:
            response = interviewer.__repr__(), 200
        else:
            response = "The interviewer with id %s does not exist" % id, 406
        return response

    def put(self, id):
        """
        PUT interface to update an interviewer by it's unique database id. All data for which is contained in the json
        object is updated.
        :param id:
        :return:
        """
        # Get the json object from the request body
        data = request.get_json()
        # Check all fields for availability and get the new data if the field is available
        if 'email' not in data:
            email = None
        else:
            email = data["email"]
        if 'first_name' not in data:
            first_name = None
        else:
            first_name = data["first_name"]
        if 'last_name' not in data:
            last_name = None
        else:
            last_name = data["last_name"]
        if 'availability' not in data:
            availability = None
        else:
            availability = data["availability"]

        # Update all requested fields of the requested interviewer, if there is an interviewer with the id, else return
        # an error
        interviewer = interviewer_ctrl.update_interviewer(id, email, first_name, last_name, availability)
        if not interviewer:
            response = "Interviewer with id %s does not exist or email %s is already taken by another interviewer" % (
                id, email), 400
        else:
            response = interviewer, 200
        return response

    def delete(self, id):
        """
        Interface to delete the interviewer with the requested id.
        :param id:
        :return:
        """
        # If the interviewer is in the database, confirm deletion, else return an error
        success_msg = interviewer_ctrl.delete_interviewer(id)
        if success_msg:
            response = success_msg, 200
        else:
            response = "Interviewer with id %s does not exist" % id, 406
        return response


class Interviewers(Resource):
    def get(self):
        """
        GET interface to get a list of all interviewers in the database
        :return:
        """
        return interviewer_ctrl.get_all()


class NewInterviewee(Resource):
    def post(self):
        """
        POST interface to create a new interviewee. Receives a json object containing the email, first_name and
        last_name of the new interviewee. The availability information in optional. It can be updated via the PUT
        interface in the Interviewee resource.
        :return:
        """
        data = request.get_json()
        if 'email' not in data:
            response = "Missing argument 'email'", 400
        elif 'first_name' not in data:
            response = "Missing argument 'first_name'", 400
        elif 'last_name' not in data:
            response = "Missing argument 'last_name'", 400
        else:
            if 'availability' not in data:
                availability = None
            else:
                availability = data["availability"]
            interviewee = interviewee_ctrl.create_interviewee(data["email"], data["first_name"], data["last_name"],
                                                              availability)
            if not interviewee:
                response = "interviewee with email %s already exists" % data["email"], 406
            else:
                response = interviewee, 200
        return response


class Interviewee(Resource):
    def get(self, id):
        """
        GET interface to retrieve the interviewee information for a specific interviewee by the database id, which is
        automatically assigned at creation.
        :param id: unique database id of the interviewee to be retrieved
        :return:
        """
        interviewee = interviewee_ctrl.get_interviewee_by_id(id)
        if interviewee:
            response = interviewee.__repr__(), 200
        else:
            response = "The interviewee with id %s does not exist" % id, 406
        return response

    def put(self, id):
        """
        PUT interface to update an interviewee by it's unique database id. All data for which is contained in the json
        object is updated.
        :param id:
        :return:
        """
        data = request.get_json()
        if 'email' not in data:
            email = None
        else:
            email = data["email"]
        if 'first_name' not in data:
            first_name = None
        else:
            first_name = data["first_name"]
        if 'last_name' not in data:
            last_name = None
        else:
            last_name = data["last_name"]
        if 'availability' not in data:
            availability = None
        else:
            availability = data["availability"]
        interviewee = interviewee_ctrl.update_interviewee(id, email, first_name, last_name, availability)
        if not interviewee:
            response = "Interviewee with id %s does not exist or email %s is already taken by another interviewee" % (
                id, email), 400
        else:
            response = interviewee, 200
        return response

    def delete(self, id):
        """
        Interface to delete the interviewee with the requested id.
        :param id:
        :return:
        """
        success_msg = interviewee_ctrl.delete_interviewee(id)
        if success_msg:
            response = success_msg, 200
        else:
            response = "interviewee with id %s does not exist" % id, 406
        return response


class Interviewees(Resource):
    def get(self):
        """
        GET interface to get a list of all interviewees in the database
        :return:
        """
        return interviewee_ctrl.get_all()
