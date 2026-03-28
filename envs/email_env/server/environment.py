from core.env_server import Environment
from ..models import EmailObservation, EmailState

class EmailEnvironment(Environment):
    def __init__(self):
        # Advanced Dataset: Real-world scenarios with AI info
        self.emails = [
            {
                "text": "URGENT: Your bank account is locked! Click here to verify your identity now.",
                "label": "spam", "subject": "Security Alert", "sender": "security@fakebank.com",
                "reason": "Warning: High-pressure language and suspicious sender domain identified as a phishing attempt.",
                "draft": "No reply drafted for blacklisted security risk."
            },
            {
                "text": "Hey, can we push our 2 PM sync to 4 PM? My previous meeting is running over.",
                "label": "important", "subject": "Meeting Sync", "sender": "manager@company.com",
                "reason": "Internal request from a high-priority contact regarding project scheduling.",
                "draft": "Sure, I have updated the invite to 4 PM. See you then!"
            },
            {
                "text": "Flash Sale! Get 50% OFF on all premium subscriptions this weekend only.",
                "label": "promotion", "subject": "50% OFF SALE!", "sender": "marketing@streamingplus.com",
                "reason": "Commercial content identified as a bulk marketing promotion.",
                "draft": "Interested. Send me details about the premium features."
            },
            {
                "text": "Attached is the invoice for last month's consultation fees. Payment due in 7 days.",
                "label": "important", "subject": "Invoice #492", "sender": "finance@partner.com",
                "reason": "Financial document with tight deadline. Requires immediate attention.",
                "draft": "Received. Forwarding to our billing department for processing."
            }
        ]
        self.reset()

    def reset(self):
        self.index = 0
        self.state_data = EmailState(step_count=0, current_email_id=0, total_reward=0.0)
        
        email = self.emails[self.index]
        return EmailObservation(
            email_text=email["text"],
            sender=email["sender"],
            subject=email["subject"],
            reasoning=email["reason"],
            draft_reply=email["draft"],
            done=False,
            reward=0.0
        )

    def step(self, action):
        email = self.emails[self.index]
        
        # Advanced Reward Logic
        reward = 1.5 if action.content == email["label"] else -1.0
        
        self.state_data.total_reward += reward
        self.index += 1
        self.state_data.step_count += 1
        self.state_data.current_email_id = self.index
        
        done = self.index >= len(self.emails)
        
        if not done:
            next_e = self.emails[self.index]
            return EmailObservation(
                email_text=next_e["text"],
                sender=next_e["sender"],
                subject=next_e["subject"],
                reasoning=next_e["reason"],
                draft_reply=next_e["draft"],
                done=False,
                reward=reward
            )
        else:
            return EmailObservation(
                email_text="Session Complete",
                sender="None",
                subject="Done",
                reasoning="All emails processed.",
                draft_reply="",
                done=True,
                reward=reward
            )

    @property
    def state(self):
        return self.state_data
