import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN")
MODEL = os.getenv("MODEL_NAME")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

ENV_URL = "http://localhost:8000"


def extract_json(text):
    import re
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"tool_name": "finish", "tool_input": "error"}


def run():
    scores = []

    for _ in range(3):
        res = requests.post(f"{ENV_URL}/reset").json()
        obs = res["observation"]

        for step in range(8):
            prompt = f"""
You are an advanced reasoning agent.

Task: {obs['task']}
History: {obs['history']}
Reflection: {obs.get('reflection')}

You can use tools:
query_db, calculate, search, reflect, finish

Think carefully. Use reflect if uncertain.

Return JSON only.
"""

            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )

            action = extract_json(response.choices[0].message.content)

            res = requests.post(f"{ENV_URL}/step", json=action).json()
            obs = res["observation"]

            if res["done"]:
                scores.append(res["info"]["score"])
                break

    print("Scores:", scores)
    print("Average:", sum(scores) / len(scores))


if __name__ == "__main__":
    run()