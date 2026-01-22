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

    print("Boss started, manager running on port 50000")

    # Envoyer des tâches
    for i in range(5):
        task = Task(identifier=i)
        task_queue.put(task)
        print(f"Task {i} sent to queue")

    # Collecter les résultats
    results_collected = 0
    while results_collected < 5:
        t = result_queue.get()
        print(f"✓ Task {t.identifier} finished in {t.time:.4f}s")
        results_collected += 1

    print("All tasks completed! Boss waiting (Ctrl+C to stop)")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()