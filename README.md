### Predicting Storm Incidents

#### Project Set Up

Project is configured with `python=3.11`. If you do not have this version installed, 
but you have `pyenv`, you can install this version by simply running:

```bash
pyenv install 3.11
```

Then to run this version in your terminal, simply run:

```bash
pyenv shell 3.11
```

Project uses `pipenv` as the default package and virtual environment manager.

To install `pipenv`, run the following command:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pipenv
```

#### Setting up the project

Before starting the project ensure the database has been configured correctly.
1. **Set up the database connection** - The current project uses a `.env` file to configure the database connection. 
These files are not save on git but must be configured manually and individually.
To configure the file:

   1. copy the existing `example.env` and rename it to: `.env`.
   2. open the newly created `.env` file and edit the environment variables inside it as follows:
      ```text
       DB_NAME="EXAMPLE_NAME" # the name of your database
       DB_USER="EXAMPLE_USER" # the name of your database user
       DB_PASSWORD="EXAMPLE_PASSWORD" # the name of your user's password
       DB_HOST_NAME="EXAMPLE_HOST" # the host name of your database
       DB_PORT=5432 # the name of your database
       OPEN_WEATHER_URL="https://api.openweathermap.org/data/2.5/forecast"
       OPEN_WEATHER_API_KEY="API_KEY"
       OPEN_WEATHER_LATITUDE=52.370216
       OPEN_WEATHER_LONGITUDE=4.895168
       ```
2. **Migrate the database** - after you have configured the database settings, you need to migrate the django models into database tables. 
To create the necessary migrations run:

   ```bash
   pipenv run python3 manage.py makemigrations incident_predictions
   pipenv run python3 manage.py migrate
   ```

3. **Create the database views** - these will be needed to actually model our data and create the different relations between our tables. To do this run the following command:
   ```bash
    pipenv run python3 utils/load_data.py
   ```

4. **Load the necessary data** - In order to load the necessary data into our database tables, do the following:
   1. Run the django server
   ```bash
   pipenv run python3 manage.py runserver
   ```
   
   2. Call the following endpoints
   ```
   http://127.0.0.1:8000/load_data/high_ground_water
   http://127.0.0.1:8000/load_data/tree_data
   http://127.0.0.1:8000/load_data/load_grid
   http://127.0.0.1:8000/load_data/load_incidents
   http://127.0.0.1:8000/load_data/load_soil
   http://127.0.0.1:8000/load_data/load_buildings
   http://127.0.0.1:8000/load_data/load_vunerable_locations
   http://127.0.0.1:8000/load_data/load_weather_data
   ```