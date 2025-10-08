# fastapi-address-book

A RESTful API for managing addresses with geolocation capabilities. Built with FastAPI, SQLAlchemy, and SQLite.

# Features

* CRUD Operations: Create, Read, Update, Delete addresses
* Geolocation Support: Store and query addresses with latitude/longitude coordinates
* Distance-based Search: Find addresses within a specified radius
* Data Validation: Robust input validation using Pydantic
* SQLite Database: Persistent storage with SQLAlchemy ORM
* Logging: Comprehensive logging for debugging and monitoring
* API Documentation: Auto-generated Swagger UI and ReDoc
* Best Practices: Clean architecture, type hints, proper error handling

## Project Structure
```
address-book-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 
│   ├── api/
│   │   └── routes/addresses.py
│   ├── core/config.py
│   ├── crud/address.py
│   ├── db/database.py
│   ├── models/address.py
│   └── schemas/address.py
├── requirements.txt
├── test_api.py
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Prerequisites

* Python 3.8 or higher
* pip


### Option 1: Manual Setup

#### 1. Clone the Repository

```aiignore
git clone https://github.com/gaikwadanil/fastapi-address-book.git

cd address-book-api

```

#### 2. Create a Virtual Environment
```aiignore
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### 3. Install Dependencies
```aiignore
pip install -r requirements.txt
```
#### 4. Run the Application
```aiignore
uvicorn app.main:app --reload
```

### Option 2: Docker Setup

#### 1. Build and Run with Docker Compose
```aiignore
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t address-book-api .
docker run -p 8000:8000 address-book-api
```

### API Documentation
Once the server is running, access the interactive API documentation:

```aiignore
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

