#!/bin/bash
echo "Starting Customer Support Frontend..."
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py