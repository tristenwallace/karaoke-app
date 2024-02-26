# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /karaoke-app

# Copy the current directory contents into the container at /karaoke-app
COPY . /karaoke-app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]