# Technical Evaluation Test

This repository contains the solution for the problem proposed by Mississipi (Ambar).
the proposed problem has the following challenges:
 * Retrieve data from an external API (climatempo)
 * Persist the data in a sqllite database
 * Making the endpoints:
       - Retrieve city information (from climatempo)
       - Retrieve statistical information from the collected data

## Setup

This project was created with [Python 3.7](https://www.python.org/downloads/).
I recommend the use of virtualenv to install this project.

## Install
Install all the app packages:

    pip install -r requirenments.txt

Change any necessary settings with enviroment variables.
To load a enviroment variable, run `export VARIABLE=VALUE`
Here all the app configuration (located in app/config.py):

| Enviroment Variable | Description | Default Value |
| ------ | ------ | ------ |
| DEBUG | Run the flask application with debug on | True |
| HOST | Which host to bind | 0.0.0.0 (all) |
| PORT | Port of the application | 5000 |
| SQLALCHEMY_DATABASE_URI | URI to connect to the database | sqlite:////tmp/app.db |
| CLIMA_TEMPO_URL | Clima Tempo default URL | http://apiadvisor.climatempo.com.br/api/v1/ |
| CLIMA_TEMPO_TOKEN | Clima Tempo Authentication Token | **Must be set** |

## Run the project
Just run:
```
python run.py
```

## Endpoints
| URL | Parameters | Description |
| --- | ---------- | ----------- |
| /city/<city_id> | **city_id** -> id of the city (in clima tempo) | Return the fetched data from clima tempo |
| /city/analysis/<initial_date>/<final_date> | **initial_date** -> initial date for the analysis in the format YYYY-MM-DD. <br/> **final_date** -> final date for the analysis in the format YYYY-MM-DD. | Return weather analysis from the cities that wore (at some point), retrieved from clima tempo |
