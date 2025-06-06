from dotenv import load_dotenv
import os
def read_secret(secret_name):
    try:
        load_dotenv(dotenv_path="../database/.env")
        return os.getenv(secret_name)
    except FileNotFoundError:
        return None