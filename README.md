<img src="https://your-image-link.com/banner.png" alt="Project Banner" width="100%" />

# DevNewsCopilot – Blackbox.ai-Powered News Assistant (
Lablab 2025 Hackathon Submission from AgentOps

**DevNewsCopilot** is a real-time, AI-powered tool designed to help developers cut through noisy tech updates and focus on what matters. It combines autonomous agents with LLMs to scan, summarize, and deliver actionable insights and code snippets from the latest AI and development news.

> 🔬 Built for the **lablab.ai Hackathon** using **Groq API**, **LLaMa 3**, **CrewAI**, and **Blackbox.ai**

---

## 🚀 What It Does
## What It Does

- Accepts user input on any tech/dev topic (e.g., "open-source LLMs", "AI evals")
- Uses **CrewAI Researcher Agent** to gather 7–10 recent, high-quality articles
- Sends articles to **Blackbox.ai API** for enhancement via an **Editor Agent**
- Returns:
  - 🔹 Concise 2–3 line summaries
  - 🔹 "Why it matters" dev insights
  - 🔹 Copy-pasteable code snippets
- Displays results in a sleek, animated UI optimized for developers

---

## 📽️ Demo Video

> 🎥 [Watch Demo](https://your-demo-link.com)

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React.js, TailwindCSS, Framer Motion, shadcn/ui |
| Backend | FastAPI (Python 3.11) |
| AI Agents | CrewAI (Researcher), Blackbox.ai (Editor) |
| LLM Runtime | Groq API + LLaMA 3 |
| Deployment | Railway (Backend), Vercel (Frontend) |

---

## 📐 Architecture Flow

```
User Topic Input → FastAPI Endpoint (/generate-news)
  → CrewAI Researcher Agent → Collect Articles
  → Blackbox.ai API → Enhanced Developer Summaries
  → Frontend UI → Result Cards (Summary + Code)
```

---

## 🌐 Live Demo

- Demo Link: https://qwtflr.csb.app/

---

## 🧪 Try It Yourself

Enter a topic like:

```bash
"AI Chips"
"LLM eval frameworks"
"Generative AI in healthcare"
```

Each result will include:
- 🔹 Title and source
- 🔹 Enhanced summary
- 🔹 Why it matters
- 🔹 Optional code snippet

---

## 📥 Local Development

```bash
# Frontend Setup
cd frontend
npm install
npm run dev

# Backend Setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

> Note: You’ll need valid API keys for Groq and Blackbox.ai

---

## 🔍 Features Summary

- ✅ Real-time topic input and API interaction
- ✅ CrewAI Researcher Agent for article aggregation
- ✅ Live Blackbox.ai API integration for editing
- ✅ Dev-focused summaries with code
- ✅ Fully responsive UI (mobile + desktop)
- ✅ Loader, error handling, and animated transitions

---

## 🧠 Optional Features

- 📊 Trend Analysis View (static graphs)
- 📌 Bookmarks (localStorage)
- 🗳️ Fetch.ai Voting Agent *(if enabled)*

---

## 👥 Team AgentOps

| Name | Role |
|------|------|
| Nosheen Irshad | PM, QA, Docs, Pitch Support|
| Taha Saddiqui | Backend, CrewAI, FastAPI, LLM Routing, Submission Lead  |
| Reda | Blackbox.ai Integration, Agent Logic Optimization |
| Ella | UI/UX Design, Frontend Engineering, UI Flow, Animations |
| Alishba |Presentation, Pitch Support |
| Sébastien | Product Vision, Ethics, Pitch Video |

---

## 📄 License

MIT – Free to use, remix, and build upon.

---

## 📬 Submission Checklist (lablab.ai)

- [x] ✅ Working full-stack project with live demo
- [x] ✅ 2-minute recorded video demo
- [x] ✅ GitHub repo with README and instructions
- [x] ✅ Deployment on Vercel (frontend) and Railway (backend)
- [x] ✅ Use of Groq + Blackbox.ai APIs with agentic architecture
