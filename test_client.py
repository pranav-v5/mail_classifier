from envs.email_env.client import EmailEnvClient
from envs.email_env.models import EmailAction
import time

def test():
    client = EmailEnvClient("http://127.0.0.1:8000")

    # Start episode
    print("Resetting environment...")
    obs = client.reset()
    print(f"Initial Observation: {obs}")

    # Take step
    print("Taking step: classifying as 'spam'...")
    action = EmailAction(action_type="classify", content="spam")
    result = client.step(action)
    print(f"Step Result: {result}")

    # Get state
    state = client.get_state()
    print(f"Current State: {state}")

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(2)
    test()
