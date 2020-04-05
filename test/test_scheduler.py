import unittest
import datetime
import time
from src.tasks import scheduler
from src.database import service


class TestScheduler(unittest.TestCase):
    def test_tasks(self):
        self.assertTrue(scheduler.running)
        oldcnt = service._trim_count
        job = scheduler.get_jobs()[0]
        job.modify(next_run_time=datetime.datetime.now())
        time.sleep(1)
        newcnt = service._trim_count
        self.assertEqual(oldcnt + 1, newcnt)
