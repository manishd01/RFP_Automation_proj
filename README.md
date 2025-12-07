AI-Powered RFP System (FastAPI + React) - Complete

Use docker-compose for a full local dev env (Postgres + backend + frontend):
    cp .env.example .env
    docker-compose up --build

Or run backend and frontend locally:
Backend:
    cd backend
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Frontend:
    cd frontend
    npm install
    npm start

Testing:
    cd backend
    pytest
