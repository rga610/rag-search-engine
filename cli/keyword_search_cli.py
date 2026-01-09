#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer


def preprocess_text(text: str) -> str:
    """Preprocess text by converting to lowercase, stripping whitespace, and removing punctuation."""
    return text.lower().strip().translate(str.maketrans("", "", string.punctuation))


def search(query: str) -> None:
    """Load movies and search for query in titles."""

    # Load the full JSON object
    data_path = "data/movies.json"
    with open(data_path) as f:
        data = json.load(f)

    # Query preprocessing
    original_query = query
    preprocessed_query = preprocess_text(query)

    # Tokenize the query
    query_tokens = preprocessed_query.split()

    # Remove stopwords
    stopwords_path = "data/stopwords.txt"
    with open(stopwords_path) as f:
        stopwords = f.read().splitlines()

    # Remove empty query tokens
    query_tokens = [ token for token in query_tokens if token not in stopwords ]

    # Stemming
    stemmer = PorterStemmer()
    query_tokens = [ stemmer.stem(token) for token in query_tokens ]

    # Search for the query in the titles
    results = []
    for movie in data["movies"]:
        movie_title = movie["title"]

        # Title text preprocessing
        preprocessed_movie_title = preprocess_text(movie_title)
        title_tokens = preprocessed_movie_title.split()
        title_tokens = [
            token for token in title_tokens if token
        ]  # Remove empty title tokens

        # Check if ANY query token appears in ANY title token
        found_match = False
        for query_token in query_tokens:
            for title_token in title_tokens:
                if query_token in title_token:
                    found_match = True
                    break  # Exit inner loop
            if found_match:
                break  # Exit outer loop

        if found_match:
            results.append(movie)

    # Sort the results by id
    results.sort(key=lambda x: x["id"])
    results = results[:5]

    # Print the results
    print(f"Searching for: {original_query}")
    for index, movie in enumerate(results, 1):
        print(f"{index}. {movie['title']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # Search for the query using the search function
            search(args.query)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
