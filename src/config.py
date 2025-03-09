import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Read values from environment
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
