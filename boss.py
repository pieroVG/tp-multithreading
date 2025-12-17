from manager import QueueManager
from task import Task


def main():
    manager = QueueManager(
        address=("", 50000),
        authkey=b"secret",
    )
    manager.start()

    task_queue = manager.get_task_queue()
    result_queue = manager.get_result_queue()

    for i in range(5):
        task_queue.put(Task(identifier=i))

    for _ in range(5):
        t = result_queue.get()
        print(f"Task {t.identifier} finished in {t.time:.4f}s")

    manager.shutdown()


if __name__ == "__main__":
    main()
