
from src.llm_client import get_mistral_response
from src.preprocessor import DataProcessor
from src.doc_search import DocumentSearcher
from src.interface import start_interface

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

p = DataProcessor('data/poems')

# p.generate_metadata('data/metadata', API_KEY)

p.load_metadata('data/metadata')
s = DocumentSearcher(p.metadata)

start_interface(p.files, s)