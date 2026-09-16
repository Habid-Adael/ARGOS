class Planner:

    def create_plan(self, task):

        return {

            "task": task,

            "steps": [

                "Understand the objective",

                "Inspect existing plugins",

                "Generate implementation",

                "Generate tests",

                "Execute sandbox",

                "Repair failures if necessary",

                "Evaluate",

                "Install"

            ]

        }
    