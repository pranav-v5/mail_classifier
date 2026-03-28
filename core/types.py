from dataclasses import dataclass
from typing import Any

@dataclass
class StepResult:
    observation: Any
    reward: float
    done: bool
