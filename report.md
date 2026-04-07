# BuildSpace Report

## Overview
BuildSpace is a full-stack developer collaboration platform with:
- user authentication and profiles
- project creation and team collaboration
- opportunity posting and responses
- comments and notifications
- global search across users, projects, and opportunities

## Tech Stack
- Backend: Flask, SQLAlchemy, JWT, CORS
- Frontend: Vue 3, Vite, Pinia, Vue Router
- Database: SQLite (development default)

## How To Run

### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create backend/.env:
```env
DATABASE_URL=sqlite:///buildspace.db
JWT_SECRET_KEY=dev-secret-key
FLASK_ENV=development
CORS_ORIGINS=http://localhost:5173
```

Start backend:
```bash
python app.py
```
Backend runs at http://127.0.0.1:5000

### 2) Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173 (or next free port like 5174/5175)

## Optional One-Command Start
From project root:
```bash
bash start.sh
```

## Quick Verification
- Open frontend URL in browser
- Register/login
- Create a project
- Post an opportunity
- Check notifications and search
