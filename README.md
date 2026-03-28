# Email Management AI Simulator 📧🚀

A next-generation **Training Environment** for testing and building AI-driven email assistants. This project features a full-featured **Enterprise Dashboard**, **Intelligence Logs**, and **Pro-Level Triage Simulations**.

## 🏗️ Project Architecture
- **Core (OpenEnv)**: A standardized framework for RL-style training.
- **Gym (EmailEnvironment)**: A realistic classification and reward system.
- **Enterprise UI**: A modern dashboard using Glassmorphism design and TailwindCSS.
- **AI Engine**: Advanced simulated reasoning for suspicious patterns and phishing detection.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Vanilla JS, HTML, TailwindCSS (for the dashboard)
- **RL Pattern**: OpenAI Gym style `step()` and `reset()` API

## 🚀 Getting Started
1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn requests
   ```
2. **Launch the Server**:
   ```bash
   python -m uvicorn envs.email_env.server.app:app --reload
   ```
3. **Interact with the Environment**:
   - Web: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - CLI: `python test_client.py`

## 🧠 Simulation Features
- **Reward System**: Bonuses for high-risk spam detection.
- **Reasoning**: AI explains "Why" it made a classification.
- **Drafting**: Automatic professional reply suggestions for important emails.

---
Project created with ❤️ by **Antigravity**.
