from queue_manager import QueueManager
from task import Task


def main():
    manager = QueueManager(address=("", 50000), authkey=b"abc")
    manager.start()

    task_q = manager.get_task_queue()
    result_q = manager.get_result_queue()

    # Création de 5 tâches
    for i in range(5):
        task_q.put(Task(identifier=i, size=100))

    # Récupération des résultats
    for _ in range(5):
        result = result_q.get()
        print(f"Result: Task {result.identifier} done in {result.time:.4f}s")

    manager.shutdown()


if __name__ == "__main__":
    main()
