import os
import random
import threading
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv

from src.doc_search import DocumentSearcher
from src.llm_client import get_mistral_response


load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

class SearchInterface:
    def __init__(self, master, documents: dict, doc_searcher: DocumentSearcher):
        self.documents = documents
        self.doc_searcher = doc_searcher

        self.master = master
        self.master.title("Poem recommender")
        self.master.geometry("600x400")
        self.master.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TEntry", foreground="#ffffff", fieldbackground="#3c3c3c", bordercolor="#007acc")
        self.style.configure("TButton", foreground="#ffffff", background="#007acc", bordercolor="#007acc")
        self.style.map("TButton", background=[("active", "#0098ff")])

        self.create_widgets()

    def create_widgets(self):
        # Frame para la barra de búsqueda y el botón
        search_frame = tk.Frame(self.master, bg="#1e1e1e")
        search_frame.pack(pady=20, padx=20, fill=tk.X)

        # Barra de búsqueda
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 12), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Botón de búsqueda
        search_button = ttk.Button(search_frame, text="Search", command=self.perform_search)
        search_button.pack(side=tk.LEFT)

        # Cuadro de texto para resultados
        self.result_text = tk.Text(self.master, wrap=tk.WORD, font=("Arial", 12), bg="#252526", fg="#ffffff", insertbackground="#ffffff")
        self.result_text.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)
    
    def perform_search(self):
        search_query = self.search_entry.get()
    
        thread = threading.Thread(target=self.search_thread, args=(search_query,))
        thread.start()

    def search_thread(self, search_query):
        try:
            self.update_search_results("Loading...")

            self.update_search_results("Improving query...")
            improved_query = get_mistral_response(self.get_query_prompt(search_query), API_KEY)

            self.update_search_results("Fetching context...")
            search_results = self.doc_searcher.search_tfidf(improved_query, 3)

            # docs = [self.documents[doc['document']]() for doc in search_results]
            docs = [(name, self.documents[name]) for name in search_results]

            self.update_search_results("Generating an answer...")
            docs = [f'# {name}{get_mistral_response(self.get_result_prompt(name, poem(), search_query), API_KEY)}\n\n{poem()}'
                    for name, poem in docs]

            result = '\n\n\n======================================================\n\n\n'.join(docs)
            
            # Actualiza los resultados en el hilo principal
            self.master.after(0, lambda: self.update_search_results(result))
        
        except Exception as e:
            # Maneja cualquier error que pueda ocurrir durante la búsqueda
            self.master.after(0, lambda: messagebox.showerror("Error", str(e)))

    def update_search_results(self, text):
        # Actualiza la interfaz de usuario desde el hilo principal
        self.master.after(0, lambda: self._update_search_results(text))

    def _update_search_results(self, text):
        # Actualiza el widget de resultados
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
    
    def get_query_prompt(self, user_query):
        return f"""
You are an intelligent poetry assistant. Your task is to interpret a user's natural language request for a poem and generate a detailed description of the type of poem they are looking for. This description should be based on the following criteria:

Themes: List at least 3 main themes that the poem should explore.
Mood: Describe the overall emotional tone the poem should have.
Literary Devices: Identify at least 5 literary devices that would enhance the poem.
Imagery: Describe the type of imagery that should be dominant.
Symbolism: Suggest key symbols that could be used and their meanings.
Keywords: List 5-7 keywords that capture the essence of the desired poem.
Related Poems: Suggest 2-3 existing poems that might be similar (If existing).
Difficulty Level: Indicate the appropriate complexity level (If provided).
Target Audience: Suggest an appropriate audience (If provided).
Emotional Impact: Describe the intended emotional effect on readers.
Language: Specify the language and any particular linguistic features.
Small summary: Provide a concise paragraph describing the core meaning the poem should convey.

User input: "{user_query}"

Based on this input, generate a comprehensive description of the poem the user is looking for, addressing as many of the above points as relevant. Your response should be detailed enough to guide a search for an existing poem or inspire the creation of a new one that matches the user's request.
"""
    def get_result_prompt(self, file_name, poem_text, user_query):
        return f"""
You are a poetry expert tasked with explaining why a particular poem matches a user's request. You will be given the user's original query and the text of a recommended poem. Your job is to create a concise summary (maximum 3 sentences) that explains how the poem aligns with the user's description.

User's original query: "{user_query}"

File name:
{file_name}

Recommended poem:
{poem_text}

Based on the user's query and the provided poem, generate a brief summary (no more than 3 sentences) that explains:
1. How the poem's main themes or content relate to the user's request.
2. Any specific elements (such as mood, imagery, or literary devices) that particularly match the user's description.
3. Why this poem is a good recommendation for the user.

Your summary should be clear, concise, and focused on the most relevant aspects that connect the poem to the user's request. Avoid general statements and instead highlight specific features of the poem that make it a suitable match.
"""

    def update_search_results(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)


def start_interface(documents, doc_searcher):
    master = tk.Tk()
    app = SearchInterface(master, documents, doc_searcher)
    master.mainloop()