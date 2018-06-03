from model import Interviewer
from service import db_service


def create_interviewer(email, first_name, last_name, availability):
    """
    CREATE Method to be mapped to POST
    Receives information for a new interviewer and creates a database entry with that information.
    :param email: The email address of the interviewer
    :param first_name: The first name of the interviewer
    :param last_name: The last name of the interviewer
    :param availability: The availability of the interviewer for the next time period encoded as bitstring. Needs to ne provided as String without leading 0b.
    :return: The newly created interviewer object as json String.
    """
    session = db_service.get_session()
    if not get_interviewer_by_email(email):
        next_id = db_service.get_next_id(Interviewer)
        if not availability:
            interviewer = Interviewer(next_id, email, first_name, last_name, None)
            session.add(interviewer)
        else:
            interviewer = Interviewer(next_id, email, first_name, last_name, availability)
            session.add(interviewer)
        session.commit()
        response = interviewer.__repr__()

    else:
        response = None
    session.close()
    return response


def get_interviewer_by_id(id):
    """
    READ Method to be mapped to GET
    Receives an interviewer id and returns the corresponding object from the database
    :param id: The database id of the interviewer to be retrieved
    :return: The interviewee object corresponding to the id or None.
    """
    session = db_service.get_session()
    interviewer = session.query(Interviewer).filter(Interviewer.id == id).first()
    if interviewer:
        response = interviewer
    else:
        response = None
    session.close()
    return response


def get_interviewer_by_email(email):
    """
    For usage in availability mapping, so that a meeting does not have to be set up by providing user ids.
    :param email: The email address of the interviewer to be retrieved from the database
    :return: The interviewee object corresponding to the email address or None.
    """
    session = db_service.get_session()
    interviewer = session.query(Interviewer).filter(Interviewer.email == email).first()
    if interviewer:
        response = interviewer
    else:
        response = None
    session.close()
    return response


def get_availability_by_email(email):
    """
    Receives the email address of an interviewer and returns the interviewers' availability if available.
    :param email: The email address of the interviewer
    :return: The availability of the interviewer as bitstring
    """
    session = db_service.get_session()
    interviewer = session.query(Interviewer).filter(Interviewer.email == email).first()
    return interviewer.availability


def update_interviewer(id, email, first_name, last_name, availability):
    """
    UPDATE Method to be mapped to PUT
    :param id: The database id of the interviewer to be updated
    :param email: The new email address of the interviewer.
    :param first_name: The new first name of the interviewer.
    :param last_name: The new last name of the interviewer.
    :param availability: The new availability encoded as bitstring. Provided as String without leading 0b
    :return: The updated interviewer object as json String.
    """
    session = db_service.get_session()
    if email and get_interviewer_by_email(email):
        response = None
    elif not get_interviewer_by_id(id):
        response = None
    else:

        interviewer = session.query(Interviewer).filter(Interviewer.id == id).first()
        if email:
            interviewer.email = email
        if first_name:
            interviewer.first_name = first_name
        if last_name:
            interviewer.last_name = last_name
        if availability:
            interviewer.availability = availability
        session.commit()
        response = interviewer.__repr__()

    session.close()
    return response


def delete_interviewer(id):
    """
    DELETE Method to be mapped to DELETE
    :param id: The database id of the interviewer to be deleted.
    :return: Either a success message or None if the interviewer was not available.
    """
    session = db_service.get_session()
    interviewer = session.query(Interviewer).filter(Interviewer.id == id).first()
    if interviewer:
        session.delete(interviewer)
        session.commit()
        response = "Interviewer with id %s was deleted" % id
    else:
        response = None
    session.close()
    return response


def get_all():
    """
    READ Method to receive a list of all interviewees
    :return: The list of all interviewers in the database as json String.
    """
    session = db_service.get_session()
    result_set = session.query(Interviewer).all()
    interviewer_list = []
    for interviewer in result_set:
        interviewer_list.append(interviewer.__repr__())
    session.close()
    return interviewer_list
