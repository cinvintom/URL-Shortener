# URL Shortener

A modern web application that allows users to shorten long URLs into compact, shareable links. Built with a FastAPI backend and React frontend, this application provides a clean and efficient way to manage URL shortening with database persistence.

## 🏗️ Architecture Overview

The application follows a microservices architecture with the following components:

- **Frontend**: React.js application running on port 3000
- **Backend**: FastAPI REST API running on port 8080
- **Database**: PostgreSQL database for URL storage
- **Containerization**: Docker and Docker Compose for easy deployment
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ React App │────│ FastAPI │────│ PostgreSQL │
│ (Port 3000) │ │ (Port 8080) │ │ Database │
└─────────────────┘ └─────────────────┘ └─────────────────┘

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM)
- **PostgreSQL** - Robust, open-source relational database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running FastAPI applications

### Frontend
- **React.js** - JavaScript library for building user interfaces
- **React Router DOM** - Declarative routing for React
- **CSS3** - Modern styling with responsive design

### DevOps & Deployment
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker application orchestration
- **Nginx** - Web server (configured in frontend)

## 🚀 Setup and Installation

### Prerequisites
- Docker and Docker Compose installed on your system
- Git (for cloning the repository)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd URL-Shortener
   ```

2. **Environment Configuration**
   ```bash
   # Copy the environment sample file
   cp env.sample .env
   ```
   
   The `.env` file contains the following configuration:
   ```env
   BACKEND_CORS_ORIGINS=["http://localhost:3000"]
   BACKEND_PORT = 8080
   PROJECT_NAME="URL Shortener"
   
   POSTGRES_SERVER=db
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=urlshortener
   SHORT_URL_LENGTH=10
   ```

3. **Build and Run the Application**
   ```bash
   # Build and start all services
   docker-compose up --build
   ```

## 🏃‍♂️ How to Run the Application Locally

### Option 1: Run Everything (Recommended)
```bash
docker-compose up --build
```

### Option 2: Development Mode
```bash
# Run only backend and database for backend development
docker-compose up backend db

# Run only frontend for frontend development
docker-compose up frontend
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **API Documentation**: http://localhost:8080/url-shortener/docs

## 📚 API Documentation

### Base URL
http://localhost:8080

### Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "status": "ok",
  "message": "URL Shortener API is running"
}
```

#### 2. Generate Short URL
```http
POST /api/v1/generate
```

**Request Body:**
```json
{
  "original_url": "https://example.com/very/long/url/here",
  "url_type": "RANDOM"
}
```

**Response:**
```json
{
  "short_url": "http://localhost:8080/abc123def",
  "original_url": "https://example.com/very/long/url/here",
  "is_short_url_exists": false,
  "created_at": "2024-01-15T10:30:00"
}
```

#### 3. Redirect to Original URL
```http
GET /{short_code}
```
**Response:** HTTP 307 Redirect to the original URL

### Error Responses
The API returns structured error responses:
```json
{
  "error_code": "SHORT_URL_NOT_FOUND",
  "error_message": "Short URL not found",
  "status_code": 404
}
```

## 🎯 Features

- **URL Shortening**: Convert long URLs into short, manageable links
- **Database Persistence**: All URLs are stored in PostgreSQL database
- **Duplicate Handling**: Returns existing short URL if the same original URL is shortened again
- **Responsive Design**: Modern, mobile-friendly user interface
- **Copy to Clipboard**: Easy sharing of shortened URLs
- **Click to Redirect**: Direct access to shortened URLs
- **API Documentation**: Interactive Swagger/OpenAPI documentation

## Design Decisions

### Backend Architecture
- **FastAPI**: Chosen for its automatic API documentation, type safety, and high performance
- **SQLAlchemy ORM**: Provides database abstraction and migration capabilities
- **Alembic**: Handles database schema migrations automatically
- **Pydantic**: Ensures data validation and serialization

### Frontend Architecture
- **React**: Selected for its component-based architecture and ecosystem
- **Functional Components**: Modern React patterns with hooks
- **Responsive Design**: Mobile-first approach for better user experience

### Database Design
- **PostgreSQL**: Reliable, ACID-compliant database for data integrity
- **URL Storage**: Stores both original and shortened URLs with metadata
- **Indexing**: Optimized for fast lookups on short URLs

### Security Considerations
- **CORS Configuration**: Properly configured for frontend-backend communication
- **Input Validation**: All inputs are validated using Pydantic schemas
- **Error Handling**: Structured error responses without exposing sensitive information

## 🐳 Docker Configuration

The application uses Docker Compose with the following services:

- **backend**: FastAPI application with hot-reload for development
- **frontend**: React application with development server
- **db**: PostgreSQL database with persistent volume storage

## 📺 Demonstration of Usage

Watch the demonstration on YouTube: [https://youtu.be/6WJfy-os_6U](https://youtu.be/6WJfy-os_6U)

## 📝 Development Notes

- The backend supports hot-reload during development
- Database migrations are handled automatically by Alembic
- Frontend proxy is configured to communicate with the backend API
- All services are connected through a custom Docker network

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source.
