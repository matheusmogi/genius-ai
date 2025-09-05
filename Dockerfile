# ─── Stage 1: base image ────────────────────────────────
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (better build caching)
COPY app/requirements.txt .

# Install system deps if needed, then Python deps
# (add "apt-get install -y build-essential" etc. if some libs require it)
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the rest of the project
COPY app .

# Streamlit default port
EXPOSE 8501

# Run streamlit when the container starts
CMD ["streamlit", "run", "chat.py", "--server.port=8501", "--server.address=0.0.0.0"]
