from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from typing import Any, Dict

class Action:
    pass

class Observation:
    pass

class State:
    pass

class Environment:
    def reset(self):
        raise NotImplementedError
    def step(self, action):
        raise NotImplementedError
    @property
    def state(self):
        raise NotImplementedError

def create_fastapi_app(env: Environment):
    app = FastAPI(title="Email Intel Dashboard")

    @app.get("/", response_class=HTMLResponse)
    def dashboard():
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Intelligence UI</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Outfit', sans-serif; }
                .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
                .scroll-hide::-webkit-scrollbar { display: none; }
            </style>
        </head>
        <body class="bg-[#0f172a] text-slate-100 flex h-screen overflow-hidden">
            <!-- Sidebar -->
            <div class="w-72 glass flex flex-col p-8 border-r border-slate-700/50">
                <div class="flex items-center gap-3 mb-12">
                    <div class="w-10 h-10 bg-gradient-to-tr from-sky-400 to-indigo-500 rounded-xl flex items-center justify-center font-bold text-xl text-white">E</div>
                    <span class="text-xl font-bold tracking-tight">EmailIntel <span class="text-sky-400">Pro</span></span>
                </div>

                <div class="space-y-6 flex-1">
                    <div class="p-5 bg-slate-800/50 rounded-2xl border border-slate-700/30">
                        <p class="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1">Total Intelligence Score</p>
                        <p id="total-reward" class="text-3xl font-bold text-sky-400">0.0</p>
                    </div>
                    <div class="p-5 bg-slate-800/50 rounded-2xl border border-slate-700/30">
                        <p class="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1">Emails Processed</p>
                        <p id="step-count" class="text-3xl font-bold text-indigo-400">0</p>
                    </div>
                </div>

                <button onclick="resetEnv()" class="w-full py-4 bg-slate-800 hover:bg-slate-700 rounded-2xl border border-slate-700 transition font-bold text-sm tracking-wide">
                    🔄 Reset Training Module
                </button>
            </div>

            <!-- Main Content Area -->
            <div class="flex-1 flex flex-col p-12 overflow-hidden">
                <div class="flex justify-between items-center mb-10">
                    <div>
                        <h2 class="text-3xl font-bold text-white mb-2">Live Training Environment</h2>
                        <p class="text-slate-400">Evaluating AI classifications in real-time...</p>
                    </div>
                    <div id="status-badge" class="px-4 py-2 bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-full text-xs font-bold uppercase tracking-widest animate-pulse">
                        Active Simulation
                    </div>
                </div>

                <div class="grid grid-cols-3 gap-8 flex-1 overflow-hidden">
                    <!-- Email Content Card -->
                    <div class="col-span-2 glass rounded-3xl p-10 flex flex-col shadow-2xl relative overflow-hidden">
                        <div class="absolute top-0 right-0 p-8">
                            <span id="current-id" class="text-slate-700 font-bold text-8xl transition-all">01</span>
                        </div>
                        
                        <div class="relative z-10 flex flex-col h-full">
                            <div class="mb-8">
                                <p id="sender" class="text-sky-400 text-xs font-bold tracking-widest uppercase mb-1">FROM: LOADING...</p>
                                <h3 id="subject" class="text-3xl font-bold text-white">Connecting to server...</h3>
                            </div>

                            <div class="flex-1 text-xl text-slate-300 italic leading-relaxed scroll-hide overflow-y-auto mb-10" id="email-text">
                                Please wait while we initialize the environment.
                            </div>

                            <div class="flex gap-4">
                                <button onclick="sendAction('spam')" class="flex-1 py-5 bg-red-500/10 hover:bg-red-500 border border-red-500/30 text-red-500 hover:text-white rounded-2xl font-bold transition-all text-sm uppercase">Mark as Spam</button>
                                <button onclick="sendAction('important')" class="flex-1 py-5 bg-emerald-500/10 hover:bg-emerald-500 border border-emerald-500/30 text-emerald-500 hover:text-white rounded-2xl font-bold transition-all text-sm uppercase">Mark Important</button>
                                <button onclick="sendAction('promotion')" class="flex-1 py-5 bg-amber-500/10 hover:bg-amber-500 border border-amber-500/30 text-amber-500 hover:text-white rounded-2xl font-bold transition-all text-sm uppercase">Mark Promotion</button>
                            </div>
                        </div>
                    </div>

                    <!-- AI Insights Panel -->
                    <div class="flex flex-col gap-6">
                        <div class="glass rounded-3xl p-8 border border-sky-500/20">
                            <h4 class="text-sky-400 text-[10px] font-bold uppercase tracking-[0.2em] mb-4">AI Reasoning Analysis</h4>
                            <p id="reasoning" class="text-sm text-slate-400 leading-relaxed italic">The AI is analyzing the content for potential security risks and metadata patterns...</p>
                        </div>
                        
                        <div class="glass rounded-3xl p-8 flex-1 flex flex-col">
                            <h4 class="text-indigo-400 text-[10px] font-bold uppercase tracking-[0.2em] mb-4">Suggested Auto-Reply</h4>
                            <textarea id="draft" class="w-full bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 text-sm text-slate-300 h-full resize-none scroll-hide" readonly>Waiting for classification...</textarea>
                            <button class="w-full mt-6 py-4 bg-gradient-to-r from-sky-400 to-indigo-500 hover:from-sky-500 hover:to-indigo-600 rounded-2xl font-bold text-sm transition-all shadow-lg text-white">Review & Commit</button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                async function fetchState() {
                    const res = await fetch('/state');
                    const data = await res.json();
                    document.getElementById('total-reward').innerText = data.total_reward.toFixed(1);
                    document.getElementById('step-count').innerText = data.step_count;
                }

                async function updateDisplay(obs) {
                    if (obs.done) {
                        document.getElementById('status-badge').innerText = "Session Done";
                        document.getElementById('status-badge').classList.remove('animate-pulse');
                        document.getElementById('email-text').innerText = "All emails have been processed successfully. High five! 🙌";
                        return;
                    }
                    document.getElementById('email-text').innerText = obs.email_text;
                    document.getElementById('sender').innerText = "FROM: " + obs.sender;
                    document.getElementById('subject').innerText = obs.subject;
                    document.getElementById('reasoning').innerText = obs.reasoning;
                    document.getElementById('draft').value = obs.draft_reply;
                    document.getElementById('current-id').innerText = (obs.step_count || 1).toString().padStart(2, '0');
                }

                async function resetEnv() {
                    const res = await fetch('/reset', { method: 'POST' });
                    const obs = await res.json();
                    updateDisplay(obs);
                    fetchState();
                }

                async function sendAction(label) {
                    const res = await fetch('/step', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ action_type: 'classify', content: label })
                    });
                    const obs = await res.json();
                    updateDisplay(obs);
                    fetchState();
                }

                resetEnv();
            </script>
        </body>
        </html>
        """

    @app.post("/reset")
    def reset():
        res = env.reset()
        if hasattr(res, "__dict__"): return res.__dict__
        return res

    @app.post("/step")
    def step(action: Dict[str, Any]):
        class ActionWrapper:
            def __init__(self, d): self.content = d.get('content')
        return env.step(ActionWrapper(action))

    @app.get("/state")
    def get_state():
        res = env.state
        if hasattr(res, "__dict__"): return res.__dict__
        return res

    return app
