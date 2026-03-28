from core.http_env_client import HTTPEnvClient
from core.types import StepResult
from .models import EmailAction, EmailObservation, EmailState

class EmailEnvClient(HTTPEnvClient[EmailAction, EmailObservation]):

    def _step_payload(self, action: EmailAction):
        return {
            "action_type": action.action_type,
            "content": action.content
        }

    def _parse_result(self, payload):
        return StepResult(
            observation=EmailObservation(**payload),
            reward=payload["reward"],
            done=payload["done"]
        )

    def _parse_state(self, payload):
        return EmailState(**payload)
