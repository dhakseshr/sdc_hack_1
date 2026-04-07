# BuildSpace - Technical Documentation

## Architecture Overview

### Backend Architecture (Flask + SQLAlchemy)
```
backend/
├── app.py           # Flask app factory
├── config.py        # Configuration
├── extensions.py    # SQLAlchemy, JWT setup
├── models/
│   ├── user.py      # User model
│   ├── project.py   # Project & ProjectMember models
│   ├── opportunity.py # Opportunity model
│   ├── post.py      # Post model (feed)
│   └── response.py  # NEW: OpportunityResponse, Comment, Notification
└── routes/
    ├── auth.py      # Authentication endpoints
    ├── users.py     # User profile endpoints
    ├── projects.py  # Project CRUD + join/leave
    ├── opportunities.py # Opportunity + response handling
    ├── feed.py      # Feed aggregation
    ├── comments.py  # Project comments (NEW)
    ├── notifications.py # Notification management (NEW)
    └── search.py    # Global search (NEW)
```

### Frontend Architecture (Vue 3 + Pinia)
```
frontend/src/
├── App.vue          # Root component
├── main.js          # Entry point
├── router/
│   └── index.js     # Route definitions
├── stores/
│   ├── auth.js      # Auth state
│   ├── feed.js      # Feed state
│   ├── projects.js  # Projects state
│   ├── opportunities.js # Opportunities state
│   ├── user.js      # User state
│   ├── notifications.js # Notifications (NEW)
│   └── search.js    # Search state (NEW)
├── services/
│   └── api.js       # API client with all endpoints
├── utils/
│   └── dateFormatter.js # Relative date utilities (NEW)
├── views/
│   ├── LandingView.vue
│   ├── FeedView.vue
│   ├── ProjectsView.vue
│   ├── ProjectDetailView.vue (NEW)
│   ├── OpportunitiesView.vue
│   ├── ProfileView.vue
│   ├── ExploreView.vue
│   ├── SearchView.vue (NEW)
│   ├── NotificationsView.vue (NEW)
│   └── SettingsView.vue (NEW)
└── components/
    ├── layout/
    │   └── NavBar.vue (ENHANCED)
    └── ... other components
```

## Database Schema

### New Models

#### OpportunityResponse
```python
- id (Integer, PK)
- opportunity_id (Integer, FK→Opportunity)
- user_id (Integer, FK→User)
- message (Text, nullable)
- created_at (DateTime)
```

#### Comment
```python
- id (Integer, PK)
- content (Text)
- author_id (Integer, FK→User)
- project_id (Integer, FK→Project, nullable)
- post_id (Integer, FK→Post, nullable)
- created_at (DateTime)
- updated_at (DateTime)
```

#### Notification
```python
- id (Integer, PK)
- user_id (Integer, FK→User)
- type (String) - 'project_invite', 'joined_project', 'new_comment', 'opp_response'
- title (String)
- message (Text)
- related_id (Integer) - ID of related resource
- read (Boolean)
- created_at (DateTime)
```

## API Endpoints

### Projects
```
GET     /api/projects                      # List all projects
POST    /api/projects                      # Create project
GET     /api/projects/<id>                 # Get project details
PUT     /api/projects/<id>                 # Update project
POST    /api/projects/<id>/join            # Join project (NEW)
DELETE  /api/projects/<id>/leave           # Leave project (NEW)
```

### Opportunities
```
GET     /api/opportunities                 # List opportunities
POST    /api/opportunities                 # Create opportunity
DELETE  /api/opportunities/<id>            # Delete opportunity
POST    /api/opportunities/<id>/respond    # Respond to opportunity (NEW)
GET     /api/opportunities/<id>/responses  # Get responses (NEW)
DELETE  /api/opportunities/<id>/responses/<rid> # Delete response (NEW)
```

### Comments
```
GET     /api/comments/project/<id>        # Get project comments (NEW)
POST    /api/comments/project/<id>        # Add comment (NEW)
PUT     /api/comments/<id>                # Edit comment (NEW)
DELETE  /api/comments/<id>                # Delete comment (NEW)
```

### Notifications
```
GET     /api/notifications                # Get notifications (NEW)
PUT     /api/notifications/<id>/read      # Mark as read (NEW)
PUT     /api/notifications/read-all       # Mark all as read (NEW)
DELETE  /api/notifications/<id>           # Delete notification (NEW)
```

### Search
```
GET     /api/search?q=<query>&type=<type>         # Global search (NEW)
GET     /api/search/users?q=<query>&skill=<skill> # Search users (NEW)
GET     /api/search/projects/by-tech?tech=<tech>  # Search by tech (NEW)
```

## State Management (Pinia Stores)

### NotificationsStore
```javascript
State:
- notifications: Array
- unreadCount: Number
- loading: Boolean

Actions:
- fetchNotifications(unread?: Boolean)
- markAsRead(id)
- markAllRead()
- deleteNotification(id)
```

### SearchStore
```javascript
State:
- results: {users, projects, opportunities}
- loading: Boolean
- lastQuery: String

Actions:
- search(query, type)
- searchUsers(query, skill)
- searchProjectsByTech(tech)
- clearSearch()
```

## Key Components

### ProjectDetailView.vue
- Full project information display
- Members list with roles
- Comments section with add/edit/delete
- Join/Leave functionality
- Project edit (owner only)
- Responsive layout with sidebar

### SearchView.vue
- Search input with icon
- Filter tabs for content type
- Results displayed in cards/lists
- Link navigation to full detail pages
- Empty states and loading

### NotificationsView.vue
- Notification list
- Filter tabs (All, Unread)
- Unread count badge
- Individual notification actions
- Mark read/delete functionality

### SettingsView.vue
- Tabbed settings interface
- Profile editing form
- Skill management
- Preferences toggles
- Account information
- Logout/Delete account

## Authentication & Security

- **JWT** tokens stored in localStorage
- **Password hashing** with bcrypt
- **CORS** configured for frontend origin
- **Protected endpoints** with @jwt_required()
- **Authorization checks** on resource-specific operations

## Performance Optimizations

- Skeleton loading states for better UX
- Lazy-loaded components (route-based)
- Computed properties for derived state
- Efficient API calls with proper pagination (50 posts limit)
- Debounced search input
- Local storage for preferences

## Error Handling

- API error interception with auto-logout on 401
- User-friendly error messages
- Input validation on both frontend and backend
- Try-catch blocks in async operations
- Error banners and notifications

## Responsive Design

- **Desktop First** approach
- **Mobile breakpoints** at 768px, 640px
- **Flexbox/Grid** layouts
- **Touch-friendly** buttons and inputs
- **Mobile navigation** with hamburger menu
- **Optimized typography** for readability

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES2020+ JavaScript
- CSS Custom Properties (CSS Variables)
- CSS Grid & Flexbox

## Development Tools

**Frontend**:
- Vue 3
- Vite
- Pinia
- Vue Router
- Axios

**Backend**:
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Flask-Migrate
- bcrypt

## Testing Recommendations

### API Testing
- Test all CRUD operations
- Test authentication flows
- Test authorization (owner checks)
- Test validation errors
- Test pagination

### UI Testing
- Test responsive layout
- Test form validations
- Test navigation
- Test error states
- Test loading states

### Integration Testing
- Test complete workflows (create → join → comment)
- Test notification triggers
- Test search results
- Test cross-feature interactions

## Deployment Considerations

### Environment Variables
Backend:
- `FLASK_ENV` (development/production)
- `DATABASE_URL` (PostgreSQL)
- `SECRET_KEY` (JWT secret)
- `CORS_ORIGINS` (frontend URL)

Frontend:
- `VITE_API_URL` (backend API URL)

### Database
- PostgreSQL recommended for production
- SQLite for development
- Migrations with Flask-Migrate

### Frontend Build
```bash
npm run build
# Output: dist/ folder for deployment
```

### Backend Deployment
```bash
gunicorn app:app
# Or with waitress, uwsgi, etc.
```

---

## File Size Summary

### Backend
- Models: ~200 lines
- Routes: ~500 lines (combined)
- Total: ~1000 lines

### Frontend
- Views: ~1500 lines
- Stores: ~300 lines
- Services: ~150 lines
- Total: ~2000 lines

## Code Quality

- **Linting**: ESLint (frontend), Black/Pylint (backend recommended)
- **Formatting**: Prettier (frontend), Black (backend)
- **Type checking**: Vue TypeScript support available
- **Comments**: Documented complex logic

---

**This is a production-ready architecture scalable for future enhancements!**
