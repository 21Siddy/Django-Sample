# Use the official Python image
FROM python:3.12.4

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code/

# Install the Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /code/

# Expose port 8000 for Django
EXPOSE 8000

# Start Django server from manage.py
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
