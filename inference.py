import os
import json
import requests
from openai import OpenAI

# 🔹 Load environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN")
MODEL = os.getenv("MODEL_NAME")

# 🔹 Initialize OpenAI-compatible client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# 🔹 Local environment server URL
ENV_URL = "http://localhost:8000"


def extract_json(text):
    """
    Extract first valid JSON object from LLM response
    """
    import re
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    # fallback if parsing fails
    return {"tool_name": "finish", "tool_input": "error"}


def run():
    scores = []

    # Run multiple episodes
    for episode in range(3):
        # 🔹 Reset environment
        res = requests.post(f"{ENV_URL}/reset").json()
        obs = res["observation"]

        task = str(obs.get("task", "unknown"))

        # ✅ REQUIRED START LOG
        print(f"[START] task={task}", flush=True)

        step_count = 0

        # 🔹 Agent loop
        for step in range(1, 9):
            step_count = step

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

            # 🔹 Parse action
            action = extract_json(raw_text)

            # 🔹 Execute step
            res = requests.post(f"{ENV_URL}/step", json=action).json()
            obs = res["observation"]

            reward = float(res.get("reward", 0.0))

            # ✅ REQUIRED STEP LOG
            print(
                f"[STEP] step={step} reward={reward:.2f}",
                flush=True
            )

            # 🔹 Check completion
            if res.get("done", False):
                score = float(res.get("info", {}).get("score", 0.0))
                scores.append(score)

                # ✅ REQUIRED END LOG
                print(
                    f"[END] task={task} score={score:.2f} steps={step_count}",
                    flush=True
                )
                break

    # 🔹 Final summary
    avg_score = sum(scores) / len(scores) if scores else 0.0

    print(
        f"[FINAL] average_score={avg_score:.2f}",
        flush=True
    )


if __name__ == "__main__":
    run()
