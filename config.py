import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


password = os.getenv('PASS')
database_path = f'postgresql://postgres:pr0t0TypingTheW0rld!@charo.gg/trivia_db'