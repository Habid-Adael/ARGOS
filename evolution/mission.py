import json
import os


MISSION_FILE = "evolution/mission.json"


DEFAULT_MISSION = {
    "mission": "Become more useful to the user while remaining safe, stable, and efficient.",

    "rules": [
        "Never modify the core directly.",
        "Always use the sandbox before installing code.",
        "Never delete working functionality.",
        "Prefer plugins over core modifications.",
        "Keep backups before every installation.",
        "Improve code quality whenever possible.",
        "Learn from every success and failure."
    ],

    "goals": [
        "Increase capabilities.",
        "Reduce response time.",
        "Reduce errors.",
        "Increase automation.",
        "Improve code quality."
    ]
}


class Mission:

    def __init__(self):

        if not os.path.exists(MISSION_FILE):
            self.save(DEFAULT_MISSION)

        self.data = self.load()

    def load(self):

        with open(MISSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):

        with open(MISSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_mission(self):
        return self.data["mission"]

    def get_rules(self):
        return self.data["rules"]

    def get_goals(self):
        return self.data["goals"]