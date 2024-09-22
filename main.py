from src.llm_client import get_mistral_response
from src.preprocessor import DataProcessor
from src.doc_search import DocumentSearcher
from src.interface import start_interface

p = DataProcessor('data/poems')

p.load_metadata('data/metadata')
s = DocumentSearcher(p.metadata)

start_interface(p.files, s)