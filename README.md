<div align="center">

# ☕ BeanBrew

### *Coffee, ordered the clever way.*

**Chat with an AI barista. Browse the menu, place orders, track your brew — all in a single delightful conversation.**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_BeanBrew-8B4513?style=for-the-badge)](https://beanbrew-okok-jtifrqs7i-chatbot-11921eff.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-Mownisa%2FBeanbrew-181717?style=for-the-badge&logo=github)](https://github.com/Mownisa/Beanbrew)

![BeanBrew Preview](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi)

</div>

---

> ⚠️ **Heads up!** This project runs on free-tier servers (Render). If the app feels slow on first load, give it **30–60 seconds** to wake up — the backend and MCP server spin down after inactivity. Totally normal! ☕

---

## ✨ What is BeanBrew?

BeanBrew is a full-stack AI-powered coffee shop where you order through natural conversation. No buttons, no dropdowns — just chat with your barista and your coffee is on its way.

**Try saying:**
- *"What's on the menu?"*
- *"I'd like a Cappuccino and a Brownie"*
- *"What's the status of my order?"*
- *"Repeat my last order"*

---

## 🎯 Features

| Feature | Description |
|---|---|
| 💬 **Conversational Ordering** | Chat naturally to browse, order, and track |
| 🤖 **AI Barista** | Powered by Google Gemini 1.5 Flash |
| 🧠 **Smart Memory** | Remembers your order history per session |
| 📋 **Live Menu** | Real menu fetched from the database |
| 🔐 **Secure Auth** | JWT-based register & login |
| 🛡️ **PII Guard** | Protects sensitive data in chat |
| 🎨 **Cozy UI** | Warm, whimsical frontend design |

---

## 🧠 How It Works

```
You (Browser)
     ↓
React + Vite Frontend
     ↓
FastAPI Backend  ←→  LangGraph ReAct Agent
                           ↓
                    Gemini 1.5 Flash (LLM)
                           ↓
                     MCP Server (Tools)
                           ↓
                    Neon Postgres (DB)
```

The backend runs a **LangGraph ReAct agent** that decides which tool to call based on your message:

| Tool | What it does |
|---|---|
| `get_menu` | Fetches all available drinks & food |
| `create_order` | Places a new order |
| `check_order_status` | Returns current order status |
| `get_last_order` | Retrieves your most recent order |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React, Vite, CSS Modules |
| **Backend** | FastAPI, Python 3.11 |
| **AI Agent** | LangGraph ReAct |
| **LLM** | Google Gemini 1.5 Flash |
| **Tool Protocol** | MCP (Model Context Protocol) |
| **Database** | Neon Postgres |
| **Auth** | JWT + Passlib |
| **Deployment** | Vercel + Render + Neon |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Neon](https://neon.tech) account (free)
- [Google AI Studio](https://aistudio.google.com) Gemini API key (free)

### 1. Clone the repo
```bash
git clone https://github.com/Mownisa/Beanbrew.git
cd Beanbrew
```

### 2. Set up MCP Server
```bash
cd mcp_server
cp .env.example .env
# Fill in DATABASE_URL in .env
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8001
```

### 3. Set up Backend
```bash
cd backend
cp .env.example .env
# Fill in all values in .env
pip install -r requirements.txt
bash start.sh
# Runs on http://localhost:8000
```

### 4. Set up Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000/api" > .env.local
npm run dev
# Runs on http://localhost:5173
```

---

## ☁️ Cloud Deployment (Free)

| Service | Provider | Cost |
|---|---|---|
| Frontend | Vercel | Free forever |
| Backend | Render | Free tier |
| MCP Server | Render | Free tier |
| Database | Neon | Free forever |

### Deploy Order
1. Push to GitHub
2. Create Neon database → copy connection strings
3. Deploy MCP server on Render (`mcp_server/`)
4. Deploy backend on Render (`backend/`)
5. Deploy frontend on Vercel (`frontend/`)

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Create a new account |
| `POST` | `/api/auth/login` | Sign in, receive JWT |
| `GET` | `/api/auth/me` | Get current user info |
| `POST` | `/api/chat` | Send a message (auth required) |
| `GET` | `/health` | Health check |

---

## 📁 Project Structure

```
Beanbrew/
├── frontend/          # React + Vite UI
│   ├── src/
│   │   ├── pages/     # Landing & Chat pages
│   │   └── components/
│   └── vite.config.js
├── backend/           # FastAPI + LangGraph agent
│   ├── src/
│   │   ├── routes/    # Auth & Chat routes
│   │   ├── migrations/# DB setup & seeding
│   │   └── repositories/
│   └── main.py
├── mcp_server/        # MCP tool server
│   └── main.py
└── README.md
```

---

## 🛡️ Security

- JWT authentication on all protected routes
- PII guard blocks API keys and redacts emails/IPs from chat
- Conversation history scoped per user thread

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">

Built with ☕ love and cozy vibes by [Mownisa](https://github.com/Mownisa)

*Your AI barista is always ready to brew* ✨

</div>