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
        try:
            return json.loads(match.group())
        except:
            pass
    return {"tool_name": "finish", "tool_input": "error"}


def run():
    scores = []

    for episode in range(3):
        # 🔹 RESET ENV
        res = requests.post(f"{ENV_URL}/reset").json()
        obs = res["observation"]

        task = obs.get("task", "unknown")

        # ✅ REQUIRED LOG FORMAT
        print(f"START task={task}")

        for step in range(1, 9):
            prompt = f"""
You are an advanced reasoning agent.

Task: {obs['task']}
History: {obs['history']}
Reflection: {obs.get('reflection')}

You can use tools:
query_db, calculate, search, reflect, finish

Think step-by-step:
1. Get data
2. Process data
3. Compute
4. Finish

Return ONLY JSON:
{{"tool_name": "...", "tool_input": "..."}}
"""

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                )

                raw_text = response.choices[0].message.content

            except Exception as e:
                raw_text = str(e)

            action = extract_json(raw_text)

            # 🔹 STEP ENV
            res = requests.post(f"{ENV_URL}/step", json=action).json()
            obs = res["observation"]

            reward = res.get("reward", 0.0)

            # ✅ REQUIRED STEP LOG
            print(
                f"STEP step={step} action={action} reward={reward:.2f}"
            )

            if res["done"]:
                score = res.get("info", {}).get("score", 0.0)
                scores.append(score)

                # ✅ REQUIRED END LOG
                print(f"END score={score:.2f}")
                break

    # ✅ FINAL SUMMARY
    avg_score = sum(scores) / len(scores) if scores else 0.0
    print(f"FINAL average_score={avg_score:.2f}")


if __name__ == "__main__":
    run()
