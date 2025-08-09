# config.py
# Loads environment variables for the survey_service microservice

import os
from dotenv import load_dotenv,find_dotenv

# Load .env from the root backend directory
load_dotenv(find_dotenv())

class Config:
    # API key for OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN") 

