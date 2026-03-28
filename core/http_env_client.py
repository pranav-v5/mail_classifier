import requests
from typing import Generic, TypeVar, Any

ActionT = TypeVar("ActionT")
ObservationT = TypeVar("ObservationT")

class HTTPEnvClient(Generic[ActionT, ObservationT]):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def reset(self) -> ObservationT:
        response = requests.post(f"{self.base_url}/reset")
        return self._parse_result(response.json()).observation

    def step(self, action: ActionT) -> Any:
        response = requests.post(
            f"{self.base_url}/step",
            json=self._step_payload(action)
        )
        return self._parse_result(response.json())

    def get_state(self) -> Any:
        response = requests.get(f"{self.base_url}/state")
        return self._parse_state(response.json())

    def _step_payload(self, action: ActionT):
        raise NotImplementedError

    def _parse_result(self, payload: dict):
        raise NotImplementedError

    def _parse_state(self, payload: dict):
        raise NotImplementedError
