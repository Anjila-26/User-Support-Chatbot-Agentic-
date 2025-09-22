  # Customer Support AI Chatbot

  A full-stack AI-powered customer support chatbot for massage booking, built with FastAPI (backend) and Streamlit (frontend).  
  Easily deployable with Docker Compose for local development or production.

  ---

  ## Features

  - **Conversational AI** for customer support and massage booking
  - **FastAPI backend** with RESTful endpoints and OpenAPI docs
  - **Streamlit frontend** for interactive chat and appointment management
  - **Persistent user sessions** and conversation state
  - **Service listing** and appointment viewing
  - **Dockerized** for easy deployment

  ---

  ## Project Structure

  ```
  chatbot/
  ├── backend/         # FastAPI backend
  │   ├── app/         # Application code
  │   ├── Dockerfile
  │   └── requirements.txt
  ├── frontend/        # Streamlit frontend
  │   ├── Dockerfile
  │   └── streamlit_app.py
  ├── docker-compose.yml
  ├── start.sh         # Startup script (Mac/Linux)
  ├── start.bat        # Startup script (Windows)
  └── notebooks/       # Data science & model training
  ```

  ---

  ## Getting Started

  ### Prerequisites

  - [Docker](https://www.docker.com/products/docker-desktop)
  - [Docker Compose](https://docs.docker.com/compose/)

  ### Quick Start

  1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd Task3/chatbot
    ```

  2. **Start the system (Mac/Linux):**
    ```sh
    ./start.sh
    ```
    Or on Windows:
    ```sh
    start.bat
    ```

    Alternatively, use Docker Compose directly:
    ```sh
    docker-compose up --build -d
    ```

  3. **Access the application:**
    - **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
    - **Backend API:** [http://localhost:8000](http://localhost:8000)
    - **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

  ---

  ## Development

  - **Backend:** FastAPI app in `backend/app/`
  - **Frontend:** Streamlit app in `frontend/`
  - **Notebooks:** Data science and model training in `notebooks/`

  ### Useful Commands

  - **Stop all services:**
    ```sh
    docker-compose down
    ```
  - **View logs:**
    ```sh
    docker-compose logs
    ```

  ---

  ## Customization

  - **API base URL:**  
    Set the `API_BASE_URL` environment variable in the frontend if deploying backend separately.

  - **Add new services:**  
    Update `backend/app/dataset/simple_dataset.csv`.

  - **Model retraining:**  
    Use the notebooks in `notebooks/` and update the model in `backend/app/model/`.

  ---

  ## License

  MIT License. See [LICENSE](LICENSE) for details.

  ---

  ## Authors

  - [Your Name or Team]
  - [Contact or Company]

  ---

  ## Acknowledgements

  - [Streamlit](https://streamlit.io/)
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [Docker](https://www.docker.com/)