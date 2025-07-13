# Use lightweight Python image
FROM python:3.10-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libglib2.0-0 \
  libsm6 \
  libxrender1 \
  libxext6 \
  && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
