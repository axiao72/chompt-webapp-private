# Use an official Python runtime as a parent image
FROM python:3.11

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y nodejs npm

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install npm packages
RUN npm install
RUN npm audit fix --force

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt