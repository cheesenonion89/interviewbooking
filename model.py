from sqlalchemy import Column, String, LargeBinary, Integer, Binary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
Definition of the domain model. The model is mapped to a database model by the ORM framework sqlalchemy. 
Provides domain classes for the interviewer and interviewee data.
"""

class Interviewer(Base):
    __tablename__ = 'interviewer'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    availability = Column(String)

    def __init__(self, id, email, first_name, last_name, availability):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.availability = availability

    def __repr__(self):
        return '{"id":%d, "email":"%s", "first_name":"%s", "last_name":"%s", "availability":"%s"}' % (
            self.id, self.email, self.first_name, self.last_name, self.availability)


class Interviewee(Base):
    __tablename__ = 'interviewee'
    id = Column(Integer, primary_key=True)
    email = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    availability = Column(String)

    def __init__(self, id, email, first_name, last_name, availability):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.availability = availability

    def __repr__(self):
        return '{"id":%d, "email":"%s", "first_name":"%s", "last_name":"%s", "availability":"%s"}' % (
            self.id, self.email, self.first_name, self.last_name, self.availability)
