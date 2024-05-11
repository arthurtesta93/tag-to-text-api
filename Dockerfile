# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /ttt-api

# Copy the Python requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY main.py .

# Command to run the Python script when the container starts
CMD ["python", "main.py"]
