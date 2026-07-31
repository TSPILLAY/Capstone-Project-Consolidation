# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory in the container
WORKDIR /app

# Install system dependencies needed to compile mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Apply migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]