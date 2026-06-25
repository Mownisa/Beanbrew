# BeanBrew ☕ — AI-Powered Coffee Shop Chatbot

A full-stack coffee shop ordering system powered by a LangGraph ReAct agent, MCP tools, Gemini LLM, and a whimsical React frontend.

## Architecture

```
Frontend (React/Vite)  →  Backend (FastAPI)  →  MCP Server  →  Neon Postgres
                               ↕
                         LangGraph Agent
                               ↕
                         Gemini 1.5 Flash
```

## Free Cloud Deployment

| Service     | Provider       | Free Tier |
|-------------|----------------|-----------|
| Frontend    | Vercel / Netlify | Permanent free |
| Backend     | Render         | 1 free web service |
| MCP Server  | Render         | 1 free web service |
| Database    | Neon           | Permanent free Postgres |

---

## Local Development

### 1. Prerequisites
- Python 3.11+
- Node.js 18+
- A free [Neon](https://neon.tech) account (or local Postgres)
- A free [Google AI Studio](https://aistudio.google.com) Gemini API key

### 2. Database (Neon)
1. Sign up at https://neon.tech
2. Create a project → Copy your connection strings:
   - `DATABASE_URL` (postgres://...)
   - `POSTGRES_CONN_STRING` (postgresql+psycopg://...)

### 3. MCP Server

```bash
cd mcp_server
cp .env.example .env
# Edit .env with your DATABASE_URL
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8001
```

### 4. Backend

```bash
cd backend
cp .env.example .env
# Edit .env with all values
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8000
```

### 5. Frontend

```bash
cd frontend
npm install
# Create .env.local:
echo "VITE_API_URL=http://localhost:8000/api" > .env.local
npm run dev
# Runs on http://localhost:5173
```

---

## Deploy to Cloud (Free)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/beanbrew.git
git push -u origin main
```

### Step 2: Neon Database
1. Go to https://neon.tech → Create project `beanbrew`
2. Copy both connection strings (psycopg2 format and psycopg3 format)

### Step 3: Deploy MCP Server on Render
1. Go to https://render.com → New → Web Service
2. Connect your GitHub repo
3. Settings:
   - **Root Directory**: `mcp_server`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
4. Environment variables:
   - `DATABASE_URL` = your Neon postgres URL
   - `PORT` = 8001
5. Deploy → Copy the public URL (e.g. `https://beanbrew-mcp.onrender.com`)

### Step 4: Deploy Backend on Render
1. New → Web Service
2. Settings:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
3. Environment variables:
   - `DATABASE_URL` = Neon URL (psycopg2 format)
   - `POSTGRES_CONN_STRING` = Neon URL (psycopg3 format: `postgresql+psycopg://...`)
   - `GEMINI_API_KEY` = your key
   - `MCP_SERVER_URL` = `https://beanbrew-mcp.onrender.com/mcp`
   - `SECRET_KEY` = any random 32-char string
4. Deploy → Copy public URL

### Step 5: Deploy Frontend on Vercel
1. Go to https://vercel.com → New Project → Import from GitHub
2. Settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
3. Environment variables:
   - `VITE_API_URL` = `https://your-backend.onrender.com/api`
4. Deploy → Done! 🎉

---

## Features
- 🔐 JWT auth (register/login)
- 🤖 LangGraph ReAct agent with memory (per-customer thread)
- ☕ MCP tools: get_menu, create_order, check_order_status, get_last_order
- 🛡️ PII guard (blocks API keys, redacts email/IP)
- 💾 Conversation history persisted in Postgres
- 🎨 Whimsical, cozy frontend

## API Endpoints
- `POST /api/auth/register` — create account
- `POST /api/auth/login` — sign in, get JWT
- `GET /api/auth/me` — current user
- `POST /api/chat` — send message (auth required)
- `GET /health` — health check
