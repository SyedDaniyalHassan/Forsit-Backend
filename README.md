# Ecommerce Admin API

A robust RESTful API for managing an e-commerce platform's administrative functions, built with FastAPI and MySQL.

## Code Repo URL 
https://github.com/SyedDaniyalHassan/Forsit-Backend.git

## Technology Stack

- **Programming Language**: Python 3.12
- **Framework**: FastAPI
- **API Type**: RESTful
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Package Manager**: Poetry
- **Monitoring**: Prometheus & Grafana

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

### Tables and Relationships

The Scipts for dummy data are the "Ecommerce_Admin_API\db\init.sql"

#### Categories
- Primary table for product categories
- Fields:
  - `id`: Primary key
  - `name`: Category name
  - `description`: Category description
  - `created_at`: Timestamp
  - `updated_at`: Timestamp

#### Products
- Stores product information
- Fields:
  - `id`: Primary key
  - `name`: Product name
  - `description`: Product description
  - `price`: Product price
  - `category_id`: Foreign key to Categories
  - `created_at`: Timestamp
  - `updated_at`: Timestamp
- Relationships:
  - Belongs to one Category
  - Has one Inventory record
  - Has many SalesDetails

#### Inventory
- Tracks product stock levels
- Fields:
  - `id`: Primary key
  - `product_id`: Foreign key to Products
  - `quantity`: Current stock quantity
  - `low_stock_threshold`: Threshold for low stock alerts
  - `created_at`: Timestamp
  - `updated_at`: Timestamp
- Relationships:
  - Belongs to one Product

#### Sales
- Records sales transactions
- Fields:
  - `id`: Primary key
  - `sale_date`: Date and time of sale
  - `total_amount`: Total sale amount
  - `created_at`: Timestamp
  - `updated_at`: Timestamp
- Relationships:
  - Has many SalesDetails

#### SalesDetails
- Stores individual items in a sale
- Fields:
  - `id`: Primary key
  - `sale_id`: Foreign key to Sales
  - `product_id`: Foreign key to Products
  - `quantity`: Quantity sold
  - `unit_price`: Price per unit at time of sale
  - `total_price`: Total price for this item
  - `created_at`: Timestamp
  - `updated_at`: Timestamp
- Relationships:
  - Belongs to one Sale
  - Belongs to one Product

### Entity Relationship Diagram
```
Categories 1──┐
              │
              ▼
Products 1────┼────1 Inventory
              │
              ▼
Sales 1───────┼─────* SalesDetails
```

## Monitoring

The application includes Prometheus and Grafana for monitoring:

1. **Prometheus**:
   - Collects metrics from the FastAPI application
   - Available at http://localhost:9090

2. **Grafana**:
   - Visualizes metrics and provides dashboards
   - Available at http://localhost:3000
   - Default credentials: admin/admin

## Development

For development, the application includes:
- Hot reload enabled
- Interactive API documentation (Swagger UI)
- Automatic request validation
- Database migrations support
- Type checking with mypy
- Code formatting with black
- Linting with ruff
