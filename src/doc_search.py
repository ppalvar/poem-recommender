import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentSearcher:
    def __init__(self, documents):
        self.documents = documents
        self.doc_contents = {name: func() for name, func in documents.items()}
        self.vectorizer = None
        self.tfidf_vectorizer = None
        self.bow_matrix = None
        self.tfidf_matrix = None
        
    def preprocess(self):
        self.vectorizer = CountVectorizer()
        self.bow_matrix = self.vectorizer.fit_transform(self.doc_contents.values())
        
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.doc_contents.values())
    
    def search_bow(self, query, top_n=5):
        if self.bow_matrix is None:
            self.preprocess()
        
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.bow_matrix).flatten()
        
        return self._get_top_results(similarities, top_n)
    
    def search_tfidf(self, query, top_n=5):
        if self.tfidf_matrix is None:
            self.preprocess()
        
        query_vec = self.tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        return self._get_top_results(similarities, top_n)
    
    def _get_top_results(self, similarities, top_n):
        top_indices = similarities.argsort()[-top_n:][::-1]
        doc_names = list(self.doc_contents.keys())
        
        results = []
        for idx in top_indices:
            results.append({
                'document': doc_names[idx],
                'similarity': similarities[idx]
            })
        
        return results
