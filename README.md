# 🍽️ Restaurant Management System

A full-featured REST API backend for managing restaurant operations — built with Django and Django REST Framework.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Reporting](#reporting)
- [What's Coming Next](#whats-coming-next)

---

## Overview

This system handles the core operations of a restaurant:

- Managing tables and their availability
- Taking and tracking reservations
- Placing and processing orders
- Auto-updating inventory when orders are placed
- Processing payments and generating bills
- Reporting on daily sales, popular items, and stock alerts

### The Full Restaurant Flow
```
Customer arrives
    → Check Table Availability
        → Make Reservation (table marked 'reserved')
            → Place Order (table marked 'occupied')
                → Inventory auto-decrements
                    → Process Payment (bill calculated automatically)
                        → Order completed (table marked 'available')
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Django 6.x | Web framework |
| Django REST Framework | API layer |
| SQLite | Database (development) |
| python-dotenv | Environment variable management |

---

## Project Structure

```
restaurant_system/          # Main Django project folder
    settings.py             # Project configuration
    urls.py                 # Root URL routing
    wsgi.py                 

core/                       # Main application
    models.py               # Database models (6 domains)
    views.py                # Business logic & API views
    serializers.py          # JSON translation layer
    urls.py                 # API URL routing
    admin.py                # Admin panel registration
    migrations/             # Database migration history

.env                        # Environment variables (never pushed to git)
.gitignore                  # Files excluded from git
manage.py                   # Django command center
requirements.txt            # Project dependencies
```

---

## Setup & Installation

### Prerequisites
- Python 3.x installed
- pip installed

### Steps

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd restaurant_system
```

**2. Create and activate virtual environment**
```bash
python -m venv resturant_env

# Windows
resturant_env\Scripts\activate.bat

# Mac/Linux
source resturant_env/bin/activate
```

**3. Install dependencies**
```bash
pip install django djangorestframework python-dotenv
```

**4. Set up environment variables**

Create a `.env` file in the root folder:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

**5. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create admin account**
```bash
python manage.py createsuperuser
```

**7. Start the server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/` to see all available endpoints.
Visit `http://127.0.0.1:8000/admin/` to access the admin panel.

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-xxxxx` |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hostnames | `127.0.0.1,localhost` |

---

## Database Models

### 1. Category
Organizes menu items into groups.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField | Category name (e.g. Food, Drinks) |

### 2. MenuItem
Items available for ordering.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField | Item name |
| description | TextField | Optional description |
| price | DecimalField | Item price |
| category | ForeignKey | Links to Category |
| is_available | BooleanField | Whether item can be ordered |
| inventory | ForeignKey | Links to Inventory item |

### 3. Table
Physical restaurant tables.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| number | IntegerField | Table number (unique) |
| capacity | IntegerField | Max number of guests |
| status | CharField | available / occupied / reserved |

### 4. Reservation
Advance table bookings.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| table | ForeignKey | Links to Table |
| customer_name | CharField | Guest name |
| customer_phone | CharField | Guest phone |
| party_size | IntegerField | Number of guests |
| date | DateField | Reservation date |
| time | TimeField | Reservation time |
| status | CharField | pending / confirmed / cancelled |

### 5. Order
Customer orders linked to tables.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| table | ForeignKey | Links to Table |
| reservation | ForeignKey | Links to Reservation (optional) |
| status | CharField | pending / preparing / served / completed / cancelled |
| created_at | DateTimeField | Auto timestamp on creation |
| updated_at | DateTimeField | Auto timestamp on update |

### 6. OrderItem
Individual items within an order.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| order | ForeignKey | Links to Order |
| menu_item | ForeignKey | Links to MenuItem |
| quantity | IntegerField | How many ordered |

### 7. Inventory
Stock tracking for ingredients.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField | Ingredient name |
| quantity | FloatField | Current stock level |
| unit | CharField | Unit of measurement (kg, litres, pieces) |
| low_stock_alert | FloatField | Threshold for low stock warning |

### 8. Payment
Payment records per order.
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| order | OneToOneField | Links to Order (one payment per order) |
| amount | DecimalField | Auto-calculated from order total |
| method | CharField | cash / card / online |
| status | CharField | pending / paid / failed |
| paid_at | DateTimeField | Timestamp of payment |

---

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories/` | List all categories |
| POST | `/categories/` | Create a category |
| GET | `/categories/{id}/` | Get one category |
| PATCH | `/categories/{id}/` | Update a category |
| DELETE | `/categories/{id}/` | Delete a category |

### Menu
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/menu/` | List all menu items |
| POST | `/menu/` | Create a menu item |
| GET | `/menu/{id}/` | Get one menu item |
| PATCH | `/menu/{id}/` | Update a menu item |
| DELETE | `/menu/{id}/` | Delete a menu item |
| GET | `/menu/available/` | List only available items |

### Tables
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tables/` | List all tables |
| POST | `/tables/` | Create a table |
| GET | `/tables/{id}/` | Get one table |
| PATCH | `/tables/{id}/` | Update a table |
| DELETE | `/tables/{id}/` | Delete a table |
| GET | `/tables/available/` | List only available tables |

### Reservations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reservations/` | List all reservations |
| POST | `/reservations/` | Create a reservation (auto-updates table status) |
| GET | `/reservations/{id}/` | Get one reservation |
| PATCH | `/reservations/{id}/` | Update a reservation |
| DELETE | `/reservations/{id}/` | Delete a reservation |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders/` | List all orders |
| POST | `/orders/` | Place an order (auto-updates inventory & table) |
| GET | `/orders/{id}/` | Get one order |
| PATCH | `/orders/{id}/` | Update an order |
| DELETE | `/orders/{id}/` | Delete an order |
| PATCH | `/orders/{id}/update_status/` | Update order status |

### Inventory
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/` | List all inventory items |
| POST | `/inventory/` | Create an inventory item |
| GET | `/inventory/{id}/` | Get one inventory item |
| PATCH | `/inventory/{id}/` | Update an inventory item |
| DELETE | `/inventory/{id}/` | Delete an inventory item |
| GET | `/inventory/low_stock/` | List items below stock threshold |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/payments/` | List all payments |
| POST | `/payments/` | Process a payment (auto-calculates amount) |
| GET | `/payments/{id}/` | Get one payment |

---

## Testing the API

Recommended tool: **Thunder Client** (VS Code extension) or **Postman**

### Example: Full Restaurant Flow

**Step 1 — Create a table**
```json
POST /api/tables/
{
    "number": 1,
    "capacity": 4,
    "status": "available"
}
```

**Step 2 — Create a category**
```json
POST /api/categories/
{
    "name": "Food"
}
```

**Step 3 — Create a menu item**
```json
POST /api/menu/
{
    "name": "Jollof Rice",
    "description": "Party jollof, the best kind",
    "price": "15.00",
    "category": 1,
    "is_available": true
}
```

**Step 4 — Create inventory**
```json
POST /api/inventory/
{
    "name": "Rice",
    "quantity": 10,
    "unit": "kg",
    "low_stock_alert": 3
}
```

**Step 5 — Link inventory to menu item**
```json
PATCH /api/menu/1/
{
    "inventory": 1
}
```

**Step 6 — Make a reservation**
```json
POST /api/reservations/
{
    "table": 1,
    "customer_name": "John Doe",
    "customer_phone": "08012345678",
    "party_size": 3,
    "date": "2026-05-21",
    "time": "18:00:00",
    "status": "confirmed"
}
```

**Step 7 — Place an order**
```json
POST /api/orders/
{
    "table": 1,
    "items": [
        {
            "menu_item": 1,
            "quantity": 2
        }
    ]
}
```

**Step 8 — Process payment**
```json
POST /api/payments/
{
    "order": 1,
    "method": "cash"
}
```

---

## Reporting

All reports are accessed via:
```
GET /api/reports/?type=<report_type>
```

### Daily Sales
```
GET /api/reports/?type=daily_sales&date=2026-05-21
```
Returns total revenue and order breakdown for a specific date.

### Most Ordered Items
```
GET /api/reports/?type=most_ordered
```
Returns menu items ranked by total quantity ordered across all time.

### Stock Alerts
```
GET /api/reports/?type=stock_alerts
```
Returns all inventory items currently below their low stock threshold.

---

## What's Coming Next

- **Phase 6 — Security & Authentication**
  - Login system with tokens
  - Role based access (Admin, Waiter, Kitchen Staff)
  - Protected endpoints

- **Phase 7 — Error Handling**
  - Global error handler
  - Proper error messages for all edge cases
  - Input validation improvements

---

## Author
Built as a project for CodeAlpha Intership — Django REST Framework restaurant management system.
