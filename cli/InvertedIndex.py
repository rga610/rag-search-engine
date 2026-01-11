import json
import pickle
import os

from utils.preprocess_text import preprocess_text


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        tokens = preprocess_text(text).split()
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term):
        """
        Return all document IDs whose token contains the search term as a substring.
        This allows matching 'assault' against tokens like 'assaulted'.
        """
        term = term.lower()
        doc_ids = set()
        for token, ids in self.index.items():
            if term in token:
                doc_ids.update(ids)
        return sorted(list(doc_ids))

    def build(self):
        # Load JSON
        with open("data/movies.json") as f:
            data = json.load(f)

        # For each movie
        for movie in data["movies"]:
            doc_id = movie["id"]

            # Store in docmap
            self.docmap[doc_id] = movie

            # Combine title + description
            text = f"{movie['title']} {movie['description']}"

            # Add to index
            self.__add_document(doc_id, text)

    def save(self):
        # Create cache directory
        os.makedirs("cache", exist_ok=True)

        # Save index
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)

        # Save docmap
        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self):
        # Check if files exist, raise error if not
        index_path = "cache/index.pkl"
        docmap_path = "cache/docmap.pkl"

        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")
        if not os.path.exists(docmap_path):
            raise FileNotFoundError(f"Docmap file not found: {docmap_path}")

        # Load the files ("rb" for binary read)
        with open(index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(docmap_path, "rb") as f:
            self.docmap = pickle.load(f)
