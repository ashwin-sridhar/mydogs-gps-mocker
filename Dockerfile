# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install websocket-client

# Run gpsmocker.py when the container launches
CMD ["python3", "gpsmocker.py"]
