from model import Interviewee
from service import db_service


def create_interviewee(email, first_name, last_name, availability):
    """
    CREATE Method to be mapped to POST
    Receives information for a new interviewee and creates a database entry with that information.
    :param email: The email address of the interviewee
    :param first_name: The first name of the interviewee
    :param last_name: The last name of the interviewee
    :param availability: The availability of the interviewee for the next time period encoded as bitstring. Needs to ne provided as String without leading 0b.
    :return: The newly created interviewee object as json String.
    """
    session = db_service.get_session()
    if not get_interviewee_by_email(email):
        next_id = db_service.get_next_id(Interviewee)
        if not availability:
            interviewee = Interviewee(next_id, email, first_name, last_name, None)
            session.add(interviewee)
        else:
            interviewee = Interviewee(next_id, email, first_name, last_name, availability)
            session.add(interviewee)
        session.commit()
        response = interviewee.__repr__()

    else:
        response = None
    session.close()
    return response


def get_interviewee_by_id(id):
    """
    READ Method to be mapped to GET
    Receives an interviewee id and returns the corresponding object from the database
    :param id: The database id of the interviewee to be retrieved
    :return: The interviewee object corresponding to the id or None.
    """
    session = db_service.get_session()
    interviewee = session.query(Interviewee).filter(Interviewee.id == id).first()
    if interviewee:
        response = interviewee
    else:
        response = None
    session.close()
    return response


def get_interviewee_by_email(email):
    """
    For usage in availability mapping, so that a meeting does not have to be set up by providing user ids.
    :param email: The email address of the interviewee to be retrieved from the database
    :return: The interviewee object corresponding to the email address or None.
    """
    session = db_service.get_session()
    interviewee = session.query(Interviewee).filter(Interviewee.email == email).first()
    if interviewee:
        response = interviewee
    else:
        response = None
    session.close()
    return response


def get_availability_by_email(email):
    """
    Receives the email address of an interviewee and returns the interviewees' availability if available.
    :param email: The email address of the interviewee
    :return: The availability of the interviewee as bitstring
    """
    session = db_service.get_session()
    interviewee = session.query(Interviewee).filter(Interviewee.email == email).first()
    return interviewee.availability


def update_interviewee(id, email, first_name, last_name, availability):
    """
    UPDATE Method to be mapped to PUT
    :param id: The database id of the interviewee to be updated
    :param email: The new email address of the interviewee.
    :param first_name: The new first name of the interviewee.
    :param last_name: The new last name of the interviewee.
    :param availability: The new availability encoded as bitstring. Provided as String without leading 0b
    :return: The updated interviewee object as json String.
    """
    session = db_service.get_session()

    if email and get_interviewee_by_email(email):
        response = None
    elif not get_interviewee_by_id(id):
        response = None
    else:

        interviewee = session.query(Interviewee).filter(Interviewee.id == id).first()
        if email:
            interviewee.email = email
        if first_name:
            interviewee.first_name = first_name
        if last_name:
            interviewee.last_name = last_name
        if availability:
            interviewee.availability = availability
        session.commit()
        response = interviewee.__repr__()

    session.close()
    return response


def delete_interviewee(id):
    """
    DELETE Method to be mapped to DELETE
    :param id: The database id of the interviewee to be deleted.
    :return: Either a success message or None if the interviewee was not available.
    """
    session = db_service.get_session()
    interviewee = session.query(Interviewee).filter(Interviewee.id == id).first()
    if interviewee:
        session.delete(interviewee)
        session.commit()
        response = "interviewee with id %s was deleted" % id
    else:
        response = None
    session.close()
    return response


def get_all():
    """
    READ Method to receive a list of all interviewees
    :return: The list of all interviewees in the database as json String.
    """
    session = db_service.get_session()
    result_set = session.query(Interviewee).all()
    interviewee_list = []
    for interviewee in result_set:
        interviewee_list.append(interviewee.__repr__())
    session.close()
    return interviewee_list
