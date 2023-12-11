# # === Build Stage ===
# FROM python:3.11 AS build

# # Install Node.js and npm for the build stage
# RUN apt-get update && \
#     apt-get install -y nodejs npm

# # Set the working directory to /app
# WORKDIR /app

# # Copy all files to the build stage
# COPY . /app

# # Install npm packages
# RUN npm install --force
# RUN npm audit fix --force

# === Final Stage ===
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files for installing Python packages
COPY requirements.txt /app/

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code from the build stage
COPY . /app

