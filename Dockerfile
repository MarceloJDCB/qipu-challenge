# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script into the container
COPY . /app/

COPY requirements.txt /app/

RUN pip install -r requirements.txt
