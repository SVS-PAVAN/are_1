# Copyright (c) Meta Platforms, Inc.
# OpenEnv-compatible client for AI Data Analyst Environment

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import AreAction, AreObservation


class AreEnv(
    EnvClient[AreAction, AreObservation, State]
):
    """
    Client for AI Data Analyst Environment.

    Supports:
    - Tool-based actions
    - Multi-step reasoning
    - Reflection tracking
    """

    def _step_payload(self, action: AreAction) -> Dict:
        """
        Convert action to JSON payload for server.
        """
        return {
            "tool_name": action.tool_name,
            "tool_input": action.tool_input,
        }

    def _parse_result(self, payload: Dict) -> StepResult[AreObservation]:
        """
        Convert server response → StepResult
        """

        obs_data = payload.get("observation", {})

        observation = AreObservation(
            task=obs_data.get("task", ""),
            history=obs_data.get("history", []),
            last_tool_output=obs_data.get("last_tool_output"),
            reflection=obs_data.get("reflection"),
            done=payload.get("done", False),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse state() response
        """

        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("steps", 0),
        )