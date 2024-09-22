import os
from dotenv import load_dotenv
from src.preprocessor import DataProcessor

load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

p = DataProcessor('data/poems')

p.generate_metadata_parallel('data/metadata', API_KEY, 2)