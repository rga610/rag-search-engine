import string

def preprocess_text(text: str) -> str:
    """Preprocess text by converting to lowercase, stripping whitespace, and removing punctuation."""
    return text.lower().strip().translate(str.maketrans("", "", string.punctuation))
