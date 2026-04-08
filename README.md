---

title: AI Data Analyst Environment
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
base_path: /web
---

# 🧠 AI Data Analyst Tool-Use Environment (OpenEnv)

An advanced **OpenEnv-compatible environment** where an AI agent acts as a **data analyst**, solving real-world business queries using **tool-based reasoning and self-reflection**.

---

## 🚀 Overview

This environment simulates a realistic workflow where an AI agent must:

* Retrieve structured data
* Perform calculations
* Use external knowledge
* Reflect on its reasoning
* Produce actionable insights

Unlike simple environments, this system evaluates **multi-step reasoning, tool usage, and self-correction behavior**.

---

## 🎯 Objective

The goal of the agent is to:

> Solve business-oriented data analysis tasks using structured tools and reasoning.

The agent must:

1. Choose the correct tool
2. Provide correct inputs
3. Chain multiple steps logically
4. Reflect when necessary
5. Produce a final answer

---

## 🧰 Available Tools

| Tool        | Description                              |
| ----------- | ---------------------------------------- |
| `query_db`  | Fetch structured employee data           |
| `calculate` | Perform numerical computations           |
| `search`    | Retrieve benchmark/global data           |
| `reflect`   | Analyze past steps and improve reasoning |
| `finish`    | Submit final answer                      |

---

## 🧠 Unique Feature — Self-Reflection (🔥)

This environment introduces a **reflection mechanism**:

* Agents can review past actions
* Detect mistakes
* Adjust strategy mid-episode

This mimics real-world **agent architectures used in modern AI systems**.

---

## 🎮 Action Space

```json
{
  "tool_name": "string",
  "tool_input": "string"
}
```

---

## 👁️ Observation Space

```json
{
  "task": "string",
  "history": ["string"],
  "last_tool_output": "string",
  "reflection": "string",
  "done": false
}
```

---

## 🧪 Tasks

The environment includes **3 progressively difficult tasks**:

### 🟢 Easy

**Task:**
Find the average salary of engineers in India

✔ Requires:

* Data retrieval
* Basic aggregation

---

### 🟡 Medium

**Task:**
Identify which role has the highest average salary

✔ Requires:

* Filtering
* Group comparison

---

### 🔴 Hard

**Task:**
Compare engineer salaries in India vs global benchmarks and recommend action

✔ Requires:

* Multi-tool reasoning
* External knowledge
* Decision-making

---

## 🏆 Reward System

The environment uses **dense reward shaping**:

| Behavior               | Reward        |
| ---------------------- | ------------- |
| Correct tool usage     | +0.2          |
| Useful reasoning steps | +0.1–0.2      |
| Reflection usage       | +0.3          |
| Incorrect tool         | -0.3          |
| Repeated actions       | -0.3          |
| Long trajectories      | small penalty |
| Final correct answer   | +score (0–1)  |

---

## 🧮 Grading System

Each task includes a **deterministic grader**:

* Score range: **0.0 → 1.0**
* Evaluates:

  * Final answer correctness
  * Tool usage
  * Reasoning trajectory
  * Reflection usage

---

## ⚙️ Environment API

### `reset()`

Initializes a new task

### `step(action)`

Executes tool action and returns:

* observation
* reward
* done
* info

### `state()`

Returns internal state

---

## 📦 Project Structure

```
are/
├── models.py
├── graders.py
├── inference.py
├── openenv.yaml
├── pyproject.toml
├── uv.lock
├── server/
│   ├── are_environment.py
│   ├── app.py
│   └── Dockerfile
```

---

## 🧪 Running Locally

### 1. Start server

```bash
uvicorn server.app:app --reload
```

### 2. Run agent

```bash
python inference.py
```

---

## 🐳 Docker

### Build

```bash
docker build -t ai-env -f server/Dockerfile .
```

### Run

```bash
docker run -p 8000:8000 ai-env
```

---

## 🌐 Deployment (Hugging Face Spaces)

```bash
openenv push
```

This will:

* Build Docker container
* Deploy environment
* Expose API + Web UI

---

## 🔐 Environment Variables

```env
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=meta-llama/Meta-Llama-3-8B-Instruct
HF_TOKEN=your_token_here
```

---

## 📊 Baseline Results

```
Scores: [0.8, 1.0, 0.7]
Average: 0.83
```

---

## 🧠 Why This Environment Matters

This environment evaluates:

* Tool-use reasoning
* Multi-step planning
* Error correction
* Reflection-based improvement

It reflects **real-world AI agent workflows**, making it highly relevant for:

* Agent evaluation
* RL training
* LLM benchmarking

---

## 🏁 Summary

This project provides:

✔ Real-world simulation
✔ Multi-step reasoning tasks
✔ Tool-use environment
✔ Self-reflection capability
✔ Deterministic grading
✔ OpenEnv compliance
✔ Full deployment pipeline

---

## 👨‍💻 Author

Built as part of OpenEnv environment challenge.
