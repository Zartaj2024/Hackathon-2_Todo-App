# AI Chatbot Deployment Notes

This document provides essential information for deploying the AI chatbot feature in production environments.

## Architecture Overview

The AI chatbot consists of multiple components that need to be deployed and configured properly:

1. **Main Backend API** - Handles authentication and general API requests
2. **MCP Server** - Runs on port 8001, handles AI tool execution
3. **Frontend Application** - React/Next.js UI for chat interface
4. **Database** - PostgreSQL with extended schema for conversations/messages
5. **OpenAI Service** - External AI provider (requires API key)

## Environment Variables

Add these environment variables to your deployment configuration:

```bash
# Hugging Face Configuration
HF_MODEL_NAME=microsoft/DialoGPT-medium
HF_API_KEY=your-huggingface-api-key-here

# MCP Server Configuration
MCP_SERVER_PORT=8001

# Database Configuration (already required by base app)
DATABASE_URL=postgresql://user:password@host:port/database

# JWT Configuration (already required by base app)
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME=Todo Web Application
DEBUG=False  # Set to True only in development
```

## Database Migration

Before deploying, run the database migration to create the new tables:

```bash
# Activate your virtual environment first
cd backend
python -m alembic upgrade head
```

This will create:
- `conversations` table
- `messages` table
- Add `ai_processed` column to `tasks` table

## Service Dependencies

### MCP Server Setup

The MCP server must be deployed separately from the main API:

1. **Port Configuration**: Ensure port 8001 is accessible and not blocked by firewalls
2. **Environment**: The MCP server needs access to the same environment variables as the main API
3. **Scaling**: Consider the load requirements when scaling the MCP server
4. **Monitoring**: Set up health checks for the MCP server

### Running the MCP Server

```bash
cd backend
python -m mcp_server.server
```

For production, consider using a process manager like systemd, supervisord, or PM2.

## Deployment Steps

### 1. Database Migration
Run the database migration before starting the application:

```bash
cd backend
python -m alembic upgrade head
```

### 2. Start MCP Server
Start the MCP server first:

```bash
cd backend
python -m mcp_server.server
```

### 3. Start Main API Server
Then start the main API server:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 5000
```

### 4. Deploy Frontend
Deploy the frontend with the appropriate API endpoints configured:

```bash
cd frontend
npm run build
npm run start  # or serve the build directory with your preferred static server
```

## Scaling Considerations

### API Gateway/Load Balancer
Configure your load balancer to route requests to both:
- Main API (port 5000)
- MCP Server (port 8001) - if accessed directly by clients

### MCP Server Scaling
- The MCP server can be scaled horizontally as it's stateless
- Use a load balancer in front of multiple MCP server instances if needed
- Ensure all MCP servers share the same configuration

### Database Scaling
- The new conversation/message tables follow the same scaling patterns as the existing task table
- Consider partitioning for large volumes of conversation data

## Monitoring and Logging

### Required Monitors
- MCP server health check (`GET /health` endpoint)
- Main API health check (`GET /health` endpoint)
- Database connection health
- OpenAI API availability
- Error rates for AI tool executions

### Log Aggregation
Ensure these logs are aggregated and monitored:
- Main API logs
- MCP server logs
- Database query logs (for performance)
- Error logs for AI interactions

## Security Considerations

### Rate Limiting
- The system implements rate limiting per user
- Default: 100 requests per hour per user
- Configure according to your capacity

### Authentication
- All chat endpoints require JWT authentication
- User ID validation ensures users can only access their own data
- Tokens must be properly secured and rotated

### Data Isolation
- Database queries verify user ownership of conversations and tasks
- MCP tools validate user permissions before operations
- Conversation data is properly isolated by user

## Troubleshooting Production Issues

### Common Issues

1. **MCP Server Not Reachable**
   - Check if MCP server is running on port 8001
   - Verify firewall rules allow internal communication
   - Check logs for MCP server startup errors

2. **AI Tool Execution Failures**
   - Verify OpenAI API key validity and quota
   - Check MCP server logs for specific tool errors
   - Review authentication tokens for validity

3. **Database Performance Issues**
   - Monitor query performance for new conversation/message tables
   - Ensure proper indexing (automatically created by migrations)
   - Consider partitioning for large datasets

### Health Checks

Implement these health checks in your monitoring system:

**Main API**: `GET /health` and `GET /ready`
**MCP Server**: `GET /health` (if implemented in MCP server)

## Rollback Plan

To rollback the AI chatbot feature:

1. Remove the chat API routes from the main application
2. Revert database changes using: `python -m alembic downgrade -1`
3. Stop the MCP server
4. Remove the chat UI from the frontend

## Performance Tuning

### Caching
Consider implementing caching for:
- User conversation history (with appropriate TTL)
- Frequently accessed AI responses (if applicable)

### Database Optimization
- Monitor query performance on new tables
- Consider read replicas for conversation history
- Archive old conversations if needed