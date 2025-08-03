# Retain Coding Challenge Solutions

This repository contains solutions for both tasks in the Retain coding challenge.

## Task 1: Code Refactoring Challenge

### Overview
Refactored a legacy user management API to improve security, code organization, and maintainability.

### Key Improvements
- **Security**: Fixed SQL injection vulnerabilities, implemented secure password hashing
- **Architecture**: Modular design with proper separation of concerns
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Testing**: Added unit tests and API tests

### Running Task 1
```bash
cd task1-refactoring/refactored
pip install -r requirements.txt
python app.py
```

### API Endpoints
- `GET /` - Health check
- `GET /api/users` - Get all users (with pagination)
- `GET /api/users/<id>` - Get specific user
- `POST /api/users` - Create new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user
- `GET /api/users/search?name=<name>` - Search users by name
- `POST /api/login` - User login

## Task 2: URL Shortener Service

### Overview
Built a complete URL shortening service with analytics and click tracking.

### Features
- URL shortening with 6-character alphanumeric codes
- URL redirection with click tracking
- Analytics endpoint for statistics
- Proper error handling and validation
- Thread-safe concurrent request handling

### Running Task 2
```bash
cd task2-url-shortener
pip install -r requirements.txt
python -m flask --app app.main run
```

### API Endpoints
- `GET /` - Health check
- `POST /api/shorten` - Shorten a URL
- `GET /<short_code>` - Redirect to original URL
- `GET /api/stats/<short_code>` - Get URL statistics

### Example Usage
```bash
# Shorten URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Use short URL (redirects)
curl -L http://localhost:5000/abc123

# Get analytics
curl http://localhost:5000/api/stats/abc123
```

## Testing

### Task 1 Tests
```bash
cd task1-refactoring/refactored
python -m pytest tests/ -v
```

### Task 2 Tests
```bash
cd task2-url-shortener
python -m pytest tests/ -v
```

## Architecture Decisions

### Task 1 Refactoring
- **Flask Blueprints**: For modular route organization
- **SQLite with Context Managers**: Thread-safe database operations
- **Bcrypt**: Secure password hashing
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Centralized error handling with proper HTTP codes

### Task 2 URL Shortener
- **In-Memory SQLite**: Simple but effective for the requirements
- **Thread-Safe Design**: Proper handling of concurrent requests
- **Modular Architecture**: Clean separation of concerns
- **Comprehensive Testing**: Tests covering all core functionality

## Security Considerations

### Task 1
- Fixed SQL injection vulnerabilities
- Implemented secure password hashing
- Added input validation and sanitization
- Removed sensitive data from API responses

### Task 2
- URL validation to prevent malicious URLs
- Proper error handling to prevent information leakage
- Thread-safe operations for concurrent access
- Input validation for all endpoints

Both solutions are production-ready with proper error handling, logging, and security measures.
