from evolution.mission import Mission
from evolution.analyzer import Analyzer
from evolution.planner import Planner
from evolution.programmer import Programmer
from evolution.debugger import Debugger
from evolution.sandbox import Sandbox
from evolution.evaluator import Evaluator
from evolution.installer import Installer


class EvolutionManager:

    def __init__(self):
        self.mission = Mission()

        self.analyzer = Analyzer()
        self.planner = Planner()
        self.programmer = Programmer()
        self.debugger = Debugger()
        self.sandbox = Sandbox()
        self.evaluator = Evaluator()
        self.installer = Installer()

    def evolve(self):

        print("\n========== ARGOS EVOLUTION ==========")

        task = self.analyzer.find_next_task()

        if task is None:
            print("Nothing to improve.")
            return

        print(f"Target: {task}")

        plan = self.planner.create_plan(task)

        candidate = self.programmer.generate(plan)

        attempt = 1

        while True:

            print(f"\nTesting attempt {attempt}")

            result = self.sandbox.test(candidate)

            if result.success:
                break

            print("Repairing...")

            candidate = self.debugger.fix(
                candidate,
                result
            )

            attempt += 1

            if attempt > 10:
                print("Maximum repair attempts reached.")
                return

        score = self.evaluator.evaluate(candidate)

        if score >= 85:

            print("Candidate accepted.")

            self.installer.install(candidate)

        else:

            print(f"Rejected (score {score})")