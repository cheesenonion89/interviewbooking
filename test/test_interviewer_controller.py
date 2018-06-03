import unittest
from service import db_service
from unittest import TestCase

import controller.interviewer_controller as ctrl


class TestInterviewerController(TestCase):
    def setUp(self):
        db_service.init_db()
        db_service.mockup()

    def test_get_interviewer_by_id(self):
        interviewer = ctrl.get_interviewer_by_id(1)
        self.assertIsNotNone(interviewer)
        self.assertEqual(interviewer.id, 1)

        interviewer = ctrl.get_interviewer_by_id(10)
        self.assertIsNone(interviewer)

    def test_get_interviewer_by_email(self):
        interviewer = ctrl.get_interviewer_by_email('n.available@interviewer.de')
        self.assertEqual(interviewer.email, 'n.available@interviewer.de')

    def test_get_availability_by_email(self):
        availability = ctrl.get_availability_by_email('n.available@interviewer.de')
        self.assertEqual(availability,
                         '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    def test_create_interviewer(self):
        ctrl.create_interviewer('email4', 'fn4', 'ln4', None)
        self.assertEqual(ctrl.get_interviewer_by_email('email4').id, 6)

        ctrl.create_interviewer('email5', 'fn5', 'ln5', '1001001')
        self.assertEqual(ctrl.get_interviewer_by_email('email5').availability, '1001001')

    def test_update_interviewer(self):
        new_email = 'liame1'
        new_fn = '1nf'
        new_ln = '1nl'
        new_availability = b'11111111'

        ctrl.update_interviewer(1, new_email, None, None, None)
        self.assertEqual(ctrl.get_interviewer_by_id(1).email, new_email)
        self.assertEqual(ctrl.get_interviewer_by_id(1).first_name, 'never')

        ctrl.update_interviewer(1, None, new_fn, None, None)
        self.assertEqual(ctrl.get_interviewer_by_id(1).first_name, new_fn)
        self.assertEqual(ctrl.get_interviewer_by_id(1).last_name, 'available')

        ctrl.update_interviewer(1, None, None, new_ln, new_availability)
        self.assertEqual(ctrl.get_interviewer_by_id(1).last_name, new_ln)
        self.assertEqual(ctrl.get_interviewer_by_id(1).availability, new_availability)

    def test_delete_interviewer(self):
        ctrl.delete_interviewer(1)
        self.assertIsNone(ctrl.get_interviewer_by_id(1))

    def tearDown(self):
        db_service.teardown_db()


if __name__ == '__main__':
    unittest.main()
