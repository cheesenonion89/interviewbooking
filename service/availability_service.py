from bitstring import BitArray

"""
Service to expose the functionality that computes the availability between a set of interviewers and interviewees
"""


def get_available_time_slots(interviewer_availabilities, interviewee_availability):
    """
    Receives a list of availabilities from interviewers and an interviewee availability as bitstring, where each bit is
    mapped to a time slot. 0 indicates that the time slot is not free, 1 that it is free.
    E.g. the leftmost bit it Monday 6.00 am, the second Monday 6:30 am and so on. The bit strings
    are then combined with a bitwise and operation so that the resulting bit string represents the time slots at which
    all participants are free.
    :param interviewer_availabilities: list of bitstring encoding availability at time slots for the interviewers
    :param interviewee_availability: bitstring encoding time slots for the interviewee
    :return:
    """
    availability = BitArray(bin=interviewee_availability)
    for interviewer_availability in interviewer_availabilities:
        availability = availability & BitArray(bin=interviewer_availability)
    if availability.int != 0:
        return str(availability.bin)
    else:
        return None
