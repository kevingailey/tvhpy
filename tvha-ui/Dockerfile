# Use an official lightweight Python image.
FROM python:3.9-slim

# Prevent Python from writing pyc files to disc & enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container.
WORKDIR /app

# Upgrade pip and install Flask and Requests.
RUN pip install --upgrade pip \
    && pip install flask requests

# Copy the current directory contents into the container at /app.
COPY . /app

# Set environment variables for Flask.
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose port 5000 for the Flask app.
EXPOSE 5000

# Run the Flask app when the container launches.
CMD ["flask", "run", "--host=0.0.0.0"]

