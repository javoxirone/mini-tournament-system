# Mini Tournament System

A lightweight REST API to manage tournaments.

---

## 🛠 Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM for database interaction
- **Alembic** – Database migrations
- **PostgreSQL** – Default database
- **Docker & Docker Compose** – Optional containerization
- **Pytest** – For unit testing

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/javoxirone/mini-tournament-system.git
cd mini-tournament-system
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Update your `.env` with database credentials:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mini_tournament_system
DATABASE_URL=postgresql://user:password@localhost:5432/mini_tournament_system_test
```

---

## 🗃 Database Migrations

Run Alembic migrations:

```bash
alembic upgrade head
```

---

## ▶️ Running the App

Run the server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 API Overview

### Tournament

- `GET /tournaments/` — List tournaments  
- `POST /tournaments/` — Create a tournament  
- `GET /tournaments/{tournament_id}` — Get details  
- `DELETE /tournaments/{tournament_id}` — Delete tournament  

### Players

- `POST /tournaments/{tournament_id}/register/` — Register a player  
- `GET /tournaments/{tournament_id}/players/` — List players
---

## 🧪 Running Tests

Run all unit tests:

```bash
pytest
```

---

## 🐳 Docker Support

Run using Docker Compose:

```bash
docker-compose up --build
```

Services:

- `app`: FastAPI app  
- `db`: PostgreSQL database  

---
