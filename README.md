# AI-Powered RFP Management System

A full-stack Request for Proposal (RFP) management system built with **FastAPI** backend, **React** frontend, and automated **email handling**. The system helps track RFPs, send emails to vendors, receive proposals, and automatically score them.

---

## Features

- Create and manage RFPs
- Manage vendors
- Send RFP emails to vendors automatically
- Track communication logs (outbound & inbound)
- Capture email replies and auto-create proposal entries
- Score proposals automatically based on price, delivery, and quality
- Compare proposals and rank vendors
- Responsive frontend with React and TailwindCSS
- PostgreSQL or MySQL database support
- Dockerized backend and frontend for easy deployment

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic, Python 3.11+
- **Frontend:** React, TailwindCSS
- **Database:** PostgreSQL / MySQL
- **Email Handling:** SMTP/IMAP for sending and receiving vendor emails
- **Docker:** For containerized development and production

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Backend Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Setup environment variables:

```bash
cp backend/.env.example backend/.env
# Edit .env with your database credentials and email SMTP/IMAP settings
```

4. Run database migrations:

```bash
alembic upgrade head
```

5. Start backend server:

```bash
uvicorn backend.app.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173` (or port shown in terminal).

---

## Project Structure

```
backend/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   ├── email_polling.py
│   ├── services/
│   │   └── email_service.py
│   └── routers/
│       ├── rfp_router.py
│       ├── vendor_router.py
│       ├── communication_router.py
│       └── proposal_router.py
├── migrations/
├── requirements.txt
frontend/
├── src/
│   ├── pages/
│   ├── App.jsx
│   └── api/
└── package.json
```

---

## Usage

- Create RFPs via frontend
- Add vendors
- Send RFPs to vendors via automated emails
- Replies are captured automatically, proposals created and scored
- Compare proposals and choose the best vendor

---

## Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes with clear messages  
4. Submit a pull request

---

## License

MIT License © 2025

