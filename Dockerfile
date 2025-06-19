FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y g++ python3-dev libgdal-dev gdal-bin libproj-dev proj-data proj-bin && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port
EXPOSE 10000

# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"] 