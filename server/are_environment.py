import random
import json
import statistics

from ..models import AreAction, AreObservation
from ..graders import grade_easy, grade_medium, grade_hard


class AreEnvironment:
    def __init__(self):
        self.tasks = [
            {"id": "easy", "task": "Find average salary of engineers in India"},
            {"id": "medium", "task": "Find which role has highest average salary"},
            {"id": "hard", "task": "Compare India vs global engineer salary and recommend action"},
        ]

        self.reset()

    def reset(self):
        random.seed(42)
        self.current_task = random.choice(self.tasks)

        self.history = []
        self.last_output = None
        self.reflection = None
        self.steps = 0
        self.done = False

        return {
            "observation": AreObservation(
                task=self.current_task["task"],
                history=[],
                last_tool_output=None,
                reflection=None,
                done=False,
            ),
            "reward": 0.0,
            "done": False,
            "info": {},
        }

    def step(self, action: AreAction):
        self.steps += 1

        tool = action.tool_name
        input_data = action.tool_input

        correct_tool = True
        output = None

        try:
            if tool == "query_db":
                output = [
                    {"role": "engineer", "salary": 1200000, "country": "India"},
                    {"role": "engineer", "salary": 1500000, "country": "India"},
                    {"role": "manager", "salary": 2000000, "country": "India"},
                    {"role": "engineer", "salary": 3000000, "country": "US"},
                ]

            elif tool == "calculate":
                data = json.loads(input_data)
                salaries = [x["salary"] for x in data]
                output = statistics.mean(salaries)

            elif tool == "search":
                output = 3000000

            elif tool == "reflect":
                self.reflection = f"Reviewing steps: {self.history[-2:]}"
                output = self.reflection

            elif tool == "finish":
                self.done = True
                output = input_data

            else:
                correct_tool = False
                output = "Invalid tool"

        except Exception as e:
            output = str(e)
            correct_tool = False

        self.history.append(f"{tool}: {output}")
        self.last_output = str(output)

        reward = 0.0

        if correct_tool:
            reward += 0.2
        else:
            reward -= 0.3

        if tool == "reflect":
            reward += 0.3

        if len(self.history) >= 2 and self.history[-1] == self.history[-2]:
            reward -= 0.3

        reward -= 0.02 * self.steps

        score = 0.0
        if self.done:
            if self.current_task["id"] == "easy":
                score = grade_easy(self.last_output, self.history)
            elif self.current_task["id"] == "medium":
                score = grade_medium(self.last_output, self.history)
            else:
                score = grade_hard(self.last_output, self.history)

            reward += score

        if self.steps >= 8:
            self.done = True

        return {
            "observation": AreObservation(
                task=self.current_task["task"],
                history=self.history,
                last_tool_output=self.last_output,
                reflection=self.reflection,
                done=self.done,
            ),
            "reward": reward,
            "done": self.done,
            "info": {"score": score},
        }

    def state(self):
        return {
            "task": self.current_task,
            "history": self.history,
            "reflection": self.reflection,
        }