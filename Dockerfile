# Base image with Python
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy your app into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]