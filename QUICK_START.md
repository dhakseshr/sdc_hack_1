# BuildSpace - Quick Start Guide

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+ (or SQLite for dev)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
FLASK_ENV=development
DATABASE_URL=sqlite:///buildspace.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
EOF

# Run migrations (if needed)
flask db init
flask db migrate
flask db upgrade

# Start backend server
python app.py
# Runs on http://localhost:5000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env if needed (optional, defaults to localhost:5000)
# VITE_API_URL=http://localhost:5000

# Start dev server
npm run dev
# Runs on http://localhost:5173
```

## Testing the Features

### 1. Authentication
1. Click "Join Now" on landing page
2. Create account with email and password
3. Login with credentials

### 2. Create a Project
1. Navigate to Projects tab
2. Click "New Project" button
3. Fill in project details and tech stack
4. Click "Create Project"

### 3. Join a Project
1. View any project card
2. Click "Join" button
3. See member count increase

### 4. Project Collaboration
1. Click project name to view details
2. Add comments on project
3. View team members
4. Edit project (if owner)

### 5. Post Opportunity
1. Go to Opportunities section
2. Click "Post Opportunity"
3. Select category, add title and description
4. Submit

### 6. Respond to Opportunity
1. View any opportunity
2. Click "I'm Interested"
3. Add optional message
4. Submit response

### 7. Search
1. Click on search icon or bar in navbar
2. Enter search term
3. Filter by type (Developers, Projects, Opportunities)
4. Click results to view details

### 8. Notifications
1. Perform actions (join project, comment, respond)
2. Click notification icon (bell) in navbar
3. View all notifications
4. Mark as read or delete

### 9. User Settings
1. Click profile avatar → Settings
2. Update profile information
3. Add/remove skills
4. Toggle preferences (dark mode, notifications)
5. View account info

### 10. Explore Developers
1. Click "Explore" in navigation
2. Search for developers
3. View profiles and skills
4. Click profiles to see details

## API Testing with cURL

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Create Project
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description",
    "stack": ["Vue", "Python", "PostgreSQL"],
    "status": "recruiting"
  }'
```

### Join Project
```bash
curl -X POST http://localhost:5000/api/projects/1/join \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Notifications
```bash
curl -X GET http://localhost:5000/api/notifications \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Global Search
```bash
curl -X GET "http://localhost:5000/api/search?q=vue&type=projects" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Troubleshooting

### Backend Issues

**Port already in use (5000)**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Database errors**
```bash
# Reset database
rm backend/instance/buildspace.db
python app.py  # Creates fresh database
```

**ImportError for models**
```bash
# Make sure all models are imported in app.py
# Check models/ __init__.py for proper imports
```

### Frontend Issues

**Port already in use (5173)**
```bash
npm run dev -- --port 5174
```

**API connection errors**
```bash
# Check CORS_ORIGINS in backend .env
# Should match your frontend URL
# Default: http://localhost:5173
```

**Blank page**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Performance Tips

1. **Use browser DevTools** to monitor network requests
2. **Check Console** for JavaScript errors
3. **Enable Redux DevTools** in browser for state debugging
4. **Use Chrome DevTools Network tab** to analyze API calls
5. **Monitor database queries** in Flask debug toolbar (development only)

## Common Tasks

### Add New Environment Variable
```bash
# Backend
# 1. Add to .env file
# 2. Update config.py if needed
# 3. Access in code: os.getenv('VAR_NAME')

# Frontend
# 1. Create .env file in frontend/
# 2. Prefix with VITE_: VITE_VAR_NAME=value
# 3. Access in code: import.meta.env.VITE_VAR_NAME
```

### Database Reset
```bash
# Backend
rm backend/instance/buildspace.db
python backend/app.py
```

### Stop Services
```bash
# Frontend
# Press Ctrl+C in the terminal

# Backend  
# Press Ctrl+C in the terminal
```

## Production Deployment

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy dist/ folder
```

### Backend (Heroku/Railway)
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Pin dependencies
pip freeze > requirements.txt

# Deploy
git push heroku main
```

### Environment for Production
```
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=<long-random-string>
CORS_ORIGINS=https://yourdomain.com
```

## Documentation Files

- **IMPLEMENTATION_SUMMARY.md** - Feature overview and completion status
- **TECHNICAL_DOCS.md** - Detailed technical architecture
- **README.md** - General project information

## Support

### Common Questions

**Q: How do I reset my password?**
A: Use login with correct email, update password in Settings

**Q: Can I delete my account?**
A: Account deletion button available in Settings (Danger Zone)

**Q: How do notifications work?**
A: Check `/api/notifications` when certain events occur (joining, commenting, responding)

**Q: Is real-time sync available?**
A: Currently uses polling. WebSocket support can be added later.

**Q: Can I deploy with SQLite?**
A: Yes! Perfect for dev/demo. Switch to PostgreSQL for production.

---

**Happy building! 🚀**

For more details, check:
- Backend: `backend/app.py` and route files
- Frontend: `frontend/src/views/` for component examples
- API: Test endpoints with Postman or cURL
