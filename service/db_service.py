from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from config import Config
from model import Base, Interviewer, Interviewee

"""
Wraps basic database actions into functions and exposes them to the controllers for database interaction.
"""

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


def init_db():
    """
    initialize the database with the domain model
    :return:
    """
    import model

    model.Base.metadata.drop_all(engine)
    model.Base.metadata.create_all(engine)


def teardown_db():
    """
    Teardown the database by dropping the whole domain model (all tables)
    :return:
    """
    import model
    model.Base.metadata.drop_all()


def mockup():
    """
    Fill the database with mockup data for testing.
    :return:
    """
    session = get_session()
    session.add(Interviewer(1, 'n.available@interviewer.de', 'never', 'available',
                            '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
    session.add(Interviewer(2, 'fh.available@interviewer.de', 'first half', 'available',
                            '111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000'))
    session.add(Interviewer(3, 'sh.available@interviewer.de', 'second half', 'available',
                            '000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111111'))
    session.add(Interviewer(4, 'a.available@interviewer.de', 'always', 'available',
                            '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'))
    session.add(Interviewer(5, 'fb.available@interviewer.de', 'first best', 'available',
                            '100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
    session.add(Interviewee(1, 'n.available@interviewee.de', 'never', 'available',
                            '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
    session.add(Interviewee(2, 'fh.available@interviewee.de', 'first half', 'available',
                            '111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000'))
    session.add(Interviewee(3, 'sh.available@interviewee.de', 'second half', 'available',
                            '000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111111'))
    session.add(Interviewee(4, 'a.available@interviewee.de', 'always', 'available',
                            '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'))
    session.add(Interviewee(5, 'fb.available@interviewer.de', 'first best', 'available',
                            '100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))

    session.commit()
    session.close()


def get_session():
    """
    Create and provide a database session. The session needs to be closed afterwards.
    :return:
    """
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def get_next_id(Table):
    """
    Utility to handle the potentially missing autoincrement functionality for the database id.
    :param Table:
    :return:
    """
    session = get_session()
    max_id = session.query(func.max(Table.id)).one()[0]
    return max_id + 1
