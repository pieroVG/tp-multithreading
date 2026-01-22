from multiprocessing.managers import BaseManager
from queue import Queue


_task_queue = Queue()
_result_queue = Queue()


class QueueManager(BaseManager):
    pass


QueueManager.register("get_task_queue", callable=lambda: _task_queue)
QueueManager.register("get_result_queue", callable=lambda: _result_queue)


class QueueClient:
    def __init__(self, host="127.0.0.1", port=50000, authkey=b"secret"):
        self.manager = QueueManager(
            address=(host, port),
            authkey=authkey,
        )
        self.manager.connect()

        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()