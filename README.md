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

This does not provide any scaling of containers. 

## Application Services

Several services have been defined in the docker-compose.yml file. These services are described in the subsections that follow.

### Frontend

The frontend services provides the user interface. Users can select EEG studies for processing and view the status of any jobs submitted. 

The current frontend is built using React. An NGINX web server is used to deploy the application.

### Preprocessor (Pyprep)

There is currently only one preprocessor, which uses the Pyprep library to preprocess raw EEG data files.

Boto3 is used to retrieve files from an AWS bucket.

### Backend

The Backend provides the RESTful API for the application. It was created using the FastAPI framework. When the application is deployed, the API Documentation can be found at http://localhost:8000/docs.

### PostgreSQL (db)

PostgreSQL is a relational database used to manage repository, study, job, and file data for the application.

### Pulsar

Processing jobs are queued as messages in an Apache Pulsar topic.

### Adminer

Adminer is a free and open-source web-based database management tool that provides access to the PostgreSQL database. To log into the adminer, use a web browser to go to the URL `http://localhost:8080/` and use the settings as found in `backend > app > config` to log in:

    - System: PostgresQL
    - Server: eeg-db
    - Username: eeg_user
    - Password: password

These settings in config.py can be modified if desired.
