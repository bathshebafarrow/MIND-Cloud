# MIND-Cloud 
### Microservices for Innovative Neurotechnology Development in the Cloud (MIND Cloud)

This repository contains code to support research in cloud-based EEG preprocessing. 

It is currently being reworked to run independently of any specific cloud service provider.

## Starting the application

This application requires Docker and Docker Compose. 

To create the services and run the application locally:

1. Open a terminal window
2. Navigate the main project folder.
3. Type `docker compose up` and press Enter

## Application Services

Several services have been defined in the docker-compose.yml file. These services are described in the subsections that follow.

### Frontend

### Preprocessor

### Backend

API Documentation is found at http://localhost:8000/docs

### Pulsar

### PostgreSQL (db)

### Adminer

Adminer is a free and open-source web-based database management tool that provides access to the PostgreSQL database. To log into the adminer, use a web browser to go to the URL `http://localhost:8080/` and use the settings as found in `backend > app > config`:

    - System: PostgresQL
    - Server: eeg-db
    - Username: eeg_user
    - Password: password

These settings in config.py can be modified if desired.
