# Python ko base image
FROM python:3.13.0

# Environment variables for python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Path to install required dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Command to run the application with port
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
