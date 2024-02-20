import unittest
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from dormyboba_core.entity.queue import Queue
from dormyboba_core.entity.institute import Institute 
from dormyboba_core.entity.dormyboba_user import DormybobaUser, DormybobaRole
from dormyboba_core import model
from dormyboba_core.entity.academic_type import AcademicType
import dormyboba_api.v1api_pb2 as apiv1

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.sample_queue = Queue(
            queue_id=1,
            title="Sample Queue",
            description="Sample Description",
            open=datetime(2024, 1, 1, 12, 0, 0),
            close=datetime(2024, 1, 2, 12, 0, 0),
            active_user=DormybobaUser(
                user_id=1,
                role=DormybobaRole(role_id=1, role_name="Sample Role"),
                institute=Institute(institute_id=1, institute_name="Sample Institute"),
                academic_type=AcademicType(type_id=1, type_name="Sample Academic Type"),
                year=2024,
                group="Sample Group",
                is_registered=True
            ),
            is_event_generated=True,
        )

    def test_from_api(self):
        api_queue = apiv1.Queue(
            queue_id=1,
            title="Sample Queue",
            description="Sample Description",
            open=Timestamp(),
            close=Timestamp(),
        )
        queue = Queue.from_api(api_queue)
        self.assertEqual(queue.queue_id, 1)
        self.assertEqual(queue.title, "Sample Queue")
        self.assertEqual(queue.description, "Sample Description")
        self.assertIsNotNone(queue.open)
        self.assertIsNotNone(queue.close)
        self.assertIsNone(queue.active_user)
        self.assertIsNone(queue.is_event_generated)

    def test_to_api(self):
        api_queue = self.sample_queue.to_api()
        self.assertEqual(api_queue.queue_id, 1)
        self.assertEqual(api_queue.title, "Sample Queue")
        self.assertEqual(api_queue.description, "Sample Description")
        self.assertIsNotNone(api_queue.open)
        self.assertIsNotNone(api_queue.close)

    def test_from_model(self):
        model_queue = model.Queue(
            queue_id=1,
            title="Sample Queue",
            description="Sample Description",
            open=datetime(2024, 1, 1, 12, 0, 0),
            close=datetime(2024, 1, 2, 12, 0, 0),
            active_user_id=1,
            is_event_generated=True,
        )
        queue = Queue.from_model(model_queue)
        self.assertEqual(queue.queue_id, 1)
        self.assertEqual(queue.title, "Sample Queue")
        self.assertEqual(queue.description, "Sample Description")
        self.assertIsNotNone(queue.open)
        self.assertIsNotNone(queue.close)
        self.assertTrue(queue.is_event_generated)

    def test_to_model(self):
        model_queue = self.sample_queue.to_model()
        self.assertEqual(model_queue.queue_id, 1)
        self.assertEqual(model_queue.title, "Sample Queue")
        self.assertEqual(model_queue.description, "Sample Description")
        self.assertIsNotNone(model_queue.open)
        self.assertIsNotNone(model_queue.close)
        self.assertEqual(model_queue.active_user_id, 1)
        self.assertTrue(model_queue.is_event_generated)

if __name__ == '__main__':
    unittest.main()
