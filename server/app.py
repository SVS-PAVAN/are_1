from fastapi import FastAPI
import uvicorn

from .are_environment import AreEnvironment
from ..models import AreAction

app = FastAPI()
env = AreEnvironment()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: AreAction):
    return env.step(action)


@app.get("/state")
def state():
    return env.state()


def main():
    # ✅ FIX: pass app object directly
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()