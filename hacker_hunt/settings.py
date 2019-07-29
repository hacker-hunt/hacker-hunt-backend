import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Accessing variables.
TOKEN = os.getenv('TOKEN')
DB = os.getenv('DB')
DB_NAME = os.getenv('DB_NAME')
