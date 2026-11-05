FROM python:3.11-slim

WORKDIR /app

# Copy all project files into the container
COPY . .

CMD ["python", "main.py"]