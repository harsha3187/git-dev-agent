# Use an official Python image as the base
FROM python:3.10-slim

# Set work directory
WORKDIR /workspace

# Install dependencies
COPY requirements.txt .
COPY .env.example .
COPY app.py .
COPY git_plugin.py .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Optional: Install some useful tools
RUN apt-get update && apt-get install -y curl git

# Default command (you can override this in devcontainer.json)