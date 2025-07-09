<img src="https://github.com/nosheen/DevNews-Copilot-Blackbox.ai/blob/main/DevNewsCopilotBanner%20Image.png" alt="Project Banner" width="100%" />

# DevNewsCopilot – Blackbox.ai-Powered Developer News Assistant  
**Lablab.ai 2025 Hackathon Submission by Team AgentOps**

**DevNewsCopilot** is an AI-native, real-time tool that transforms noisy tech news into short, actionable developer updates — complete with insights, relevance, and code snippets. Built with Groq, Blackbox.ai, FastAPI, and React, it's your developer-focused AI news companion.

> 🔍 Built for the **Blackbox.ai x Groq Hackathon** on **lablab.ai**  
> ⚡ Powered by **Groq**, **LLaMA 3**, and **Blackbox.ai API**  
> 🧠 No simulation — 100% real integration with **Blackbox.ai for coding intelligence**

---

## 🚀 What It Does

- Accepts a dev/AI topic from the user (e.g., "AI evals", "open-source LLMs")
- FastAPI backend uses Groq + LLaMA 3 to collect high-quality articles
- Sends article content to **Blackbox.ai API** for developer-focused enhancement
- Returns:
  - ✅ Concise 2–3 line summaries
  - ✅ "Why it matters" insights
  - ✅ Real code snippets or usage examples
- Displays results in a responsive, animated developer UI

## Technology & Category Tags
#BlackboxAI #Groq #CrewAI #FastAPI #React #DevTools #AIProductivity #HackathonFinalist

## 📽️ Demo Video

🎥 [Watch Full Demo](https://github.com/nosheen/DevNews-Copilot-Blackbox.ai/blob/Documents/DevNewsCopilot%20Demo.mp4)

---

## ⚙️ Tech Stack

| Layer        | Technology                                  |
|--------------|---------------------------------------------|
| Frontend     | React.js, TailwindCSS, Framer Motion, shadcn/ui |
| Backend      | FastAPI (Python 3.11)                        |
| LLM Runtime  | Groq API + LLaMA 3                           |
| Coding Assistant | Blackbox.ai API (Real-time summaries + code) |
| Deployment   | Railway (Backend), Vercel (Frontend)         |

---

## 🧠 Architecture Flow
User Input → FastAPI → Groq + LLaMA → Article Set → Blackbox.ai API → Enhanced Developer Digest → UI Cards

Each summary card includes:
- 🔹 Title & Source Link  
- 🔹 Summary (2–3 lines)  
- 🔹 Why it Matters  
- 🔹 Optional: Copyable code snippet  

---

## 🌐 Live Demo

- 🔗 [Try DevNewsCopilot →](https://qwtflr.csb.app)

---

## 🧪 Try It Yourself

Use any of these inputs:
```bash
"AI Chips"
"LLM eval frameworks"
"Vector DBs with RAG"
"Generative AI in healthcare"
-----
📥 Local Development
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
⚠️ Requires valid API keys for Groq and Blackbox.ai in .env file.
------
🧩 Features
✅ Real-time dev-focused news summarization
✅ Blackbox.ai API for intelligent, code-aware output
✅ Responsive UI for desktop + mobile
✅ Framer Motion animation and smooth UX
✅ Summary cards with title, insight, code, and source

------------
🔮 Optional Enhancements (Built-In or Planned)
📊 Trend Analysis Tab (static graph)
📌 Bookmark system (browser localStorage)
🗳️ Fetch.ai Voting Agent (optional module)

-----------
🧑‍💻 Team AgentOps
Name	Role
Nosheen Irshad	PM, QA, Documentation, GitHub & Submission
Taha Saddiqui	Backend, FastAPI, Groq, LLM Routing
Reda	Blackbox.ai API Integration, Testing
Ella	Frontend Engineering, UI, Transitions
Alishba Shehzadi	UI/UX Design, Slides, Presentation Polishing
Sébastien	Product Vision, Ethics, Pitch Video Scripting

--------------
📄 License
MIT – Open for experimentation and extension.
------
✅ Lablab.ai Submission Checklist
 ✅ Project Title + Descriptions
 ✅ Public GitHub Repo
 ✅ Live App (Vercel / Railway)
 ✅ Demo Video (≤ 5 mins)
 ✅ Slide Deck (PDF)
 ✅ Tags: Groq, Blackbox.ai, Developer Tools
 ✅ Use of real Blackbox.ai API
 ✅ Functional app with real-time code summaries
-----
💬 Questions?
For technical issues or deployment help, open an issue or connect via the lablab Discord under #blackbox-groq-track.
