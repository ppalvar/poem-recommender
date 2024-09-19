import os
from math import ceil

from src.llm_client import get_mistral_response

class DataProcessor:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.get_txt_files_content()

    def load_metadata(self, metadata_path: str):
        self.metadata = self.__load_from_path__(metadata_path)
        
    def get_txt_files_content(self):
        self.files = self.__load_from_path__(self.data_path)
    
    def __load_from_path__(self, path: str):
        txt_files = {}
        
        def read_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    txt_files[file] = lambda file_path=file_path: read_file(file_path)

        return txt_files

    def chunk_files(self, chunk_size=20):
        chunked_files = [{} for i in range(ceil(len(self.files) / chunk_size))]

        for i, filename in enumerate(self.files):
            chunked_files[i // chunk_size][filename] = self.files[filename]
        
        return chunked_files

    def get_prompt(self, filename: str, poem: str):
        return f"""
Analyze the following poem and provide detailed metadata. Your analysis should include:

1. Title: The poem's title.
2. Author: The poet's name (if known).
3. Year: The year of composition or publication (if known).
4. Form: The poem's structure (e.g., sonnet, haiku, free verse).
5. Meter: The metrical pattern, if applicable (e.g., iambic pentameter).
6. Rhyme Scheme: The rhyme pattern, if present.
7. Themes: Main themes explored in the poem (list at least 3).
8. Mood: The overall emotional tone of the poem.
9. Literary Devices: Identify at least 5 literary devices used (e.g., metaphor, alliteration, personification).
10. Imagery: Describe the dominant imagery in the poem.
11. Symbolism: Identify key symbols and their potential meanings.
12. Historical Context: Any relevant historical or cultural context.
13. Interpretation: A brief (2-3 sentences) interpretation of the poem's meaning.
14. Keywords: 5-7 keywords that capture the essence of the poem.
15. Related Poems: Suggest 2-3 thematically similar poems or works.
16. Difficulty Level: Rate the poem's complexity (Easy, Moderate, Challenging).
17. Target Audience: Suggest an appropriate audience for this poem.
18. Emotional Impact: Describe the likely emotional effect on readers.
19. Cultural Significance: Note any cultural or literary significance of the poem.
20. Language: Identify the language of the poem and any dialect or linguistic features.
21. Small summary: A small paragraph describing the core meaning of the poem.

File name:
{filename}

Poem:
{poem}

Please provide the metadata in a structured format, clearly labeling each category.
"""
    
    def generate_metadata(self, output_dir: str, api_key: str="api-key"):
        def read_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.load_metadata(output_dir)
        
        for name, file in self.files.items():
            if name in self.metadata:
                print(f'Using cached metadata for file {name}.')
                continue

            msg = self.get_prompt(name, file())
            response = get_mistral_response(msg, api_key)
            
            path = os.path.join(output_dir, name)

            with open(path, 'w') as f:
                f.write(response)
            
            self.metadata[name] = lambda: read_file(path)

            print(f'Successfully generated metadata for file {name}. Total processed={len(self.metadata)} Remaining = {len(self.files) - len(self.metadata)}')