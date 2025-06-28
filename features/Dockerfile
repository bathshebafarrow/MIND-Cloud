# Set base image (host OS)
FROM python:3.11

# Copy everything from the source directory
COPY app/ /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the image
WORKDIR /app

CMD [ "python", "main.py" ]

# docker build . -t eeg-data-analysis:latest
# Obtain push commands from AWS ECR repository
