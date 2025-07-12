# Set base image (host OS)
FROM python:3.12.11-alpine

# Set the working directory in the image
WORKDIR /src

COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from the source directory
COPY /src .

EXPOSE 5000

# Set environment variables used by the flask command
ENV FLASK_APP=application.py
ENV FLASK_RUN_PORT=5000

# Specify the command to run on container start
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]