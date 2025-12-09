# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (ffmpeg is required for audio processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run model download script to bake models into the image (Optional - makes image large but truly offline)
# PRO: Container runs offline instantly. CON: Image is huge (3GB+).
# For this task, "Offline" implies the running container doesn't need internet. So we bake them in.
RUN python download_models.py

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
