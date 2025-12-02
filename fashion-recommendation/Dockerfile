# ---- Base image ----
    FROM python:3.10-slim

    # ---- Working directory ----
    WORKDIR /app
    
    # ---- Copy project files ----
    COPY ./app ./app
    COPY ./embeddings ./embeddings
    COPY requirements.txt .
    
    # ---- Install dependencies ----
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---- Expose port ----
    EXPOSE 8501
    
    # ---- Run Streamlit ----
    CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    