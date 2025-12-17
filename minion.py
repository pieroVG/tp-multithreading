from queue_manager import QueueManager


def main():
    manager = QueueManager(address=("127.0.0.1", 50000), authkey=b"abc")
    manager.connect()

    task_q = manager.get_task_queue()
    result_q = manager.get_result_queue()

    while True:
        task = task_q.get()
        if task is None:  # signal de fin
            break
        task.work()
        result_q.put(task)


if __name__ == "__main__":
    main()
