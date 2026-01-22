from manager import QueueClient


def main():
    print("Minion connecting to manager...")
    client = QueueClient()
    print("Minion ready, waiting for tasks...")

    while True:
        task = client.task_queue.get()
        print(f"Minion received task {task.identifier}, working...")
        task.work()
        print(f"Minion finished task {task.identifier}")
        client.result_queue.put(task)


if __name__ == "__main__":
    main()