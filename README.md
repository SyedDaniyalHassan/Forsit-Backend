# Ecommerce Admin API

A RESTful API for managing an e-commerce platform's administrative functions, built with FastAPI and MySQL.

## Technology Stack

- **Programming Language**: Python 3.12
- **Framework**: FastAPI
- **API Type**: RESTful
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Package Manager**: Poetry

## Setup Instructions

1. **Install Poetry** (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Install Dependencies**:
```bash
poetry install
```

3. **Configure Environment Variables**:
Create a `.env` file in the root directory with the following variables:
```bash
ECOMMERCE_ADMIN_API_ENVIRONMENT=development
ECOMMERCE_ADMIN_API_DB_HOST=localhost
ECOMMERCE_ADMIN_API_DB_PORT=3306
ECOMMERCE_ADMIN_API_DB_USER=your_username
ECOMMERCE_ADMIN_API_DB_PASS=your_password
ECOMMERCE_ADMIN_API_DB_BASE=your_database
```

4. **Run the Application**:
```bash
poetry run uvicorn Ecommerce_Admin_API.web.application:get_app --reload
```

The API will be available at `http://localhost:8000`
API documentation is available at `http://localhost:8000/api/docs`


## Database Schema

The application uses MySQL with the following main tables:
- Products
- Categories
- Inventory
- Sales
- Sales_Details
The Default scripts for dummy data is Ecommerce_Admin_API\db\init.sql (Tables can be created by starting the Application)

## Development

For development, the application includes:
- Hot reload enabled
- Interactive API documentation (Swagger UI)
- Automatic request validation
- Database migrations support
- Type checking with mypy
- Code formatting with black
- Linting with ruff
