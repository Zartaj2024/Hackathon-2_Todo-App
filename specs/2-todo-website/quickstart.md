# Quickstart Guide for Multi-User Todo Application

## Development Environment Setup

### Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.9+ for FastAPI backend
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)
- Better Auth account/config

### Frontend Setup (Next.js)
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` - Base URL for the backend API
   - `NEXTAUTH_SECRET` - Secret for authentication (Better Auth)
4. Run in development: `npm run dev`

### Backend Setup (FastAPI)
1. Navigate to the backend directory
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables:
   - `DATABASE_URL` - Connection string for PostgreSQL database
   - `JWT_SECRET_KEY` - Secret key for JWT signing
   - `BETTER_AUTH_SECRET` - Secret for Better Auth
6. Run the server: `uvicorn main:app --reload`

## Integration Scenarios

### Frontend-Backend Integration
- Frontend makes API calls to backend using JWT tokens in Authorization header
- Authentication flow: User logs in → JWT token received → Token stored in frontend → Subsequent API calls include token
- Task operations: All task CRUD operations require authentication and user ownership validation

### Authentication Flow Integration
- Better Auth handles user registration/login on frontend
- JWT tokens are exchanged for API access
- Frontend stores token securely and attaches to all API requests
- Backend validates JWT tokens and enforces user ownership

### Database Integration
- SQLModel models define the data schema
- FastAPI endpoints use SQLModel to interact with PostgreSQL
- Foreign key relationships ensure data integrity
- Backend enforces user ownership at the application level

## Key Configuration Points

### Environment Variables
- API endpoints and CORS settings
- Database connection parameters
- Authentication secrets and configuration
- JWT token expiration settings

### API Endpoint Mapping
- `/api/auth/*` routes handled by Better Auth
- `/api/tasks/*` routes handled by custom FastAPI endpoints
- Frontend pages correspond to different user flows

### Security Configuration
- JWT middleware for authentication
- User ownership validation middleware
- Input validation and sanitization
- Secure token storage and transmission