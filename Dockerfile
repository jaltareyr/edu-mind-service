# Use a minimal Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script and dependencies to the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Make the script executable
RUN chmod +x edumind.py

# Set the entrypoint to run the CLI
ENTRYPOINT ["python", "/app/edumind.py"]