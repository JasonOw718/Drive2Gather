FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
RUN python create_admin.py

# Expose port
EXPOSE 5000

# Run the application with Gunicorn
CMD ["python", "run.py"] 