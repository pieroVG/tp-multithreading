from manager import QueueManager
from task import Task
import time


def main():
    manager = QueueManager(
        address=("", 50000),
        authkey=b"secret",
    )
    manager.start()

    task_queue = manager.get_task_queue()
    result_queue = manager.get_result_queue()

    print("Boss started, manager running")

    for i in range(5):
        task_queue.put(Task(identifier=i))

    # Boucle de collecte (exemple)
    for _ in range(5):
        t = result_queue.get()
        print(f"Task {t.identifier} finished in {t.time:.4f}s")

    print("Boss waiting (Ctrl+C to stop)")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
