from manager import QueueClient


def main():
    client = QueueClient()

    while True:
        task = client.task_queue.get()
        task.work()
        client.result_queue.put(task)


if __name__ == "__main__":
    main()
