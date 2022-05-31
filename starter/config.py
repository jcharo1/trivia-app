import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


password = os.getenv('PASS')
database_path = f'postgresql://postgres:{password}@44.199.91.37:5432/trivia_db'