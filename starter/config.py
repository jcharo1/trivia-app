import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


password = os.getenv('PASS')
SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{password}@charo.gg:5432/fyyurrapp'