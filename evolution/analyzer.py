import json
import os

from evolution.task import Task


DATA_FILE = "evolution/data/tasks.json"


class Analyzer:

    def __init__(self):

        os.makedirs("evolution/data", exist_ok=True)

        if not os.path.exists(DATA_FILE):

            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    def find_next_task(self):

        with open(DATA_FILE, "r") as f:
            tasks = json.load(f)

        if len(tasks) == 0:
            return None

        tasks.sort(
            key=lambda t: t["priority"],
            reverse=True
        )

        return Task.from_dict(tasks[0])

    def add_task(self, task: Task):

        with open(DATA_FILE, "r") as f:
            tasks = json.load(f)

        tasks.append(task.to_dict())

        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=4)

    def complete(self, task):

        with open(DATA_FILE, "r") as f:
            tasks = json.load(f)

        for t in tasks:

            if t["id"] == task.id:
                t["status"] = "completed"

        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=4)