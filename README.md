# Star Wars API

A Django REST API for Star Wars universe data.

## 🚀 Quick Start

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/VGeroutskis/django_swapi.git
   cd django_swapi
   pipenv install
   pipenv shell
   ```

2. **Database setup**
   ```bash
   python manage.py migrate
   ```

3. **Import Star Wars data**
   ```bash
   python manage.py download_and_import
   ```

4. **Run server**
   ```bash
   python manage.py runserver
   ```

5. **Visit API**
   - Documentation: `http://localhost:8000/api/v1/swagger/`

## 📋 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/people/` | Star Wars characters |
| `/api/v1/planets/` | Planets and worlds |
| `/api/v1/starships/` | Starships and vessels |
| `/api/v1/vehicles/` | Vehicles and transports |
| `/api/v1/species/` | Species and races |
| `/api/v1/films/` | Star Wars movies |

## 🔍 Search & Filter

**Search by name:**
```
GET /api/v1/people/?name=luke
GET /api/v1/planets/?name=tatooine
```

**Search films by title:**
```
GET /api/v1/films/?title=hope
```

## 📄 Pagination

```
GET /api/v1/people/?page=2&page_size=10
```

## 📚 Documentation

Interactive API documentation available at:
- **Swagger UI**: `http://localhost:8000/api/v1/swagger/`

## 🛠 Tech Stack

- Python 3.13
- Django 5.0+
- Django REST Framework
- django-filter
- drf-yasg (Swagger)

---

**May the Force be with you!** ⭐