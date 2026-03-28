from dataclasses import dataclass
from core.env_server import Action, Observation, State

@dataclass
class EmailAction(Action):
    action_type: str 
    content: str     

@dataclass
class EmailObservation(Observation):
    email_text: str
    sender: str
    subject: str
    reasoning: str    # Why classify this way?
    draft_reply: str  # AI generated draft
    done: bool
    reward: float

@dataclass
class EmailState(State):
    step_count: int
    current_email_id: int
    total_reward: float
