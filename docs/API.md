# API Documentation

Dhatree AI uses Django REST Framework for API creation.
A Swagger/OpenAPI UI is available in development mode at \/api/docs/\.

## Authentication
All protected endpoints require a JWT token in the Authorization header:
\Authorization: Bearer <access_token>\

- \POST /api/v1/auth/register/\: Register a new account.
- \POST /api/v1/auth/login/\: Obtain access and refresh tokens.

## AI Assistant
- \POST /api/v1/assistant/chat/\:
  - Payload: \{ "message": "What is NPK?" }\
  - Response: \{ "data": { "response": "NPK stands for Nitrogen, Phosphorus, and Potassium..." } }\

## Farm Management
- \GET /api/v1/farms/\: List all farms.
- \POST /api/v1/farms/\: Create a new farm.

