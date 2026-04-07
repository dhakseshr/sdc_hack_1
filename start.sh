#!/bin/bash
echo "Starting BuildSpace..."

# Backend
cd backend
.venv/bin/python app.py &
BACKEND_PID=$!
echo "Backend running on http://localhost:5000 (PID: $BACKEND_PID)"

# Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend running on http://localhost:5173 (PID: $FRONTEND_PID)"

echo ""
echo "BuildSpace is live!"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"

wait
