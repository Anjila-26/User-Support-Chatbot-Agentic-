# Task 3: Customer Support Chatbot

## Overview

This project implements a **Customer Support Chatbot** system with a modular backend (FastAPI) and a frontend (Streamlit). The chatbot can answer customer queries, schedule appointments, and interact with a simple dataset and ML model. The project is containerized for easy deployment and includes tools for data handling and inference.

---

## Features

- **Conversational AI:** Responds to customer queries using a trained ML model.
- **Appointment Scheduling:** Allows users to book appointments via chat.
- **Data Tools:** Utilities for data ingestion and management.
- **Modular Backend:** FastAPI-based backend with clear separation of API, services, models, and tools.
- **Frontend:** Streamlit app for user interaction.
- **Dockerized:** Ready-to-use Docker and Docker Compose setup for both development and production.
- **Notebooks:** Jupyter notebooks for data analysis and model training.

---

## Screenshots

| Book Massage | Cancel Appointment |
|--------------|-------------------|
| ![Book Massage](screenshots/Book%20Massage.png) | ![Cancel Appointment](screenshots/Cancel%20Appointment.png) |

| See Appointment | View Service |
|-----------------|--------------|
| ![See Appointment](screenshots/See%20Appointment.png) | ![View Service](screenshots/View%20Service.png) |

---

## Project Structure

```
Task3/
├── chatbot/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/                # FastAPI routers
│   │   │   ├── core/               # Configurations
│   │   │   ├── dataset/            # Data files
│   │   │   ├── model/              # Trained ML model
│   │   │   ├── models/             # Pydantic schemas
│   │   │   ├── services/           # Business logic
│   │   │   ├── tools/              # Data and inference tools
│   │   │   ├── main.py             # FastAPI entrypoint
│   │   │   └── __init__.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── appointments.db         # SQLite DB for appointments
│   ├── frontend/
│   │   ├── streamlit_app.py        # Streamlit UI
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── run-backend.sh
│   ├── run-frontend.sh
│   ├── start.sh
│   └── start.bat
├── notebooks/
│   ├── data_ingestion.ipynb
│   ├── intent_analysis.ipynb
│   ├── simple_dataset.csv
│   ├── training_data.json
│   └── model/
├── screenshots/
│   ├── Book Massage.png
│   ├── Cancel Appointment.png
│   ├── See Appointment.png
│   └── View Service.png
└── README.md
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11+ (for local development)

---

### 1. Clone the Repository

```bash
git clone 
```

---

### 2. Build and Run with Docker Compose

#### Development

```bash
docker-compose up --build
```

#### Production

```bash
docker-compose -f docker-compose.prod.yml up --build
```

---

### 3. Run Backend and Frontend Locally (Without Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd ../frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## API Endpoints

- **GET /**  
  Health check for backend.

- **POST /api/v1/chat**  
  Send a message to the chatbot.

- **POST /api/v1/appointments**  
  Book an appointment.

- **GET /api/v1/appointments/{id}**  
  List all appointments.

---

## Customization

- **Dataset:**  
  Update `backend/app/dataset/simple_dataset.csv` for new intents or responses.

- **Model:**  
  Retrain and replace `backend/app/model/chatbot_model.pkl` as needed.

- **Configuration:**  
  Edit `backend/app/core/config.py` for environment variables and settings.

---

## Development Notes

- **Backend:**  
  Modular FastAPI app with routers, services, and tools for easy extension.

- **Frontend:**  
  Streamlit app connects to backend API for chat and appointment features.

- **Database:**  
  Uses SQLite (`appointments.db`) for appointment storage.

- **Testing:**  
  Add tests in `backend/app/tests/` (not included by default).

---

## Notebooks

- **Data Ingestion:**  
  `notebooks/data_ingestion.ipynb` for loading and preprocessing data.

- **Intent Analysis:**  
  `notebooks/intent_analysis.ipynb` for exploring and training intent models.

---

## Scripts

- `run-backend.sh` / `run-frontend.sh`:  
  Helper scripts to start backend/frontend.

- `start.sh` / `start.bat`:  
  Cross-platform startup scripts.

---

## Acknowledgements

- Built with [FastAPI](https://fastapi.tiangolo.com/), [Streamlit](https://streamlit.io/), and [Docker](https://www.docker.com/).