import unittest
from unittest import TestCase

from service import availability_service as srvc


class TestAvailabilityService(TestCase):
    def test_get_available_time_slots(self):
        interviewer_availabilities = ['000000000000000000000011111', '000000000000000000001111000',
                                      '000000000000000000000001000']
        interviewee_availability = '000000000000000000000111100'
        availability = srvc.get_available_time_slots(interviewer_availabilities, interviewee_availability)
        self.assertEqual(availability, '000000000000000000000001000')


if __name__ == '__main__':
    unittest.main()
