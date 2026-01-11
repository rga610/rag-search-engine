#!/usr/bin/env python3

import argparse

from InvertedIndex import InvertedIndex
from utils.preprocess_text import preprocess_text


def search(query: str) -> None:
    """Search using the inverted index."""

    # Load the inverted index
    try:
        idx = InvertedIndex()
        idx.load()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run 'build' command first to create the index.")
        return

    # Preprocess and tokenize the query
    original_query = query
    preprocessed_query = preprocess_text(query)
    query_tokens = preprocessed_query.split()

    # Remove empty tokens
    query_tokens = [token for token in query_tokens if token]

    # Collect document IDs from ALL tokens
    result_doc_ids = []

    # For each token in the query, get matching documents
    for token in query_tokens:
        doc_ids = idx.get_documents(token)

        # Add document IDs to results (avoid duplicates)
        for doc_id in doc_ids:
            if doc_id not in result_doc_ids:
                result_doc_ids.append(doc_id)

    # Limit to 5 results AFTER processing all tokens
    result_doc_ids = result_doc_ids[:5]

    # Print results
    print(f"Searching for: {original_query}")
    for i, doc_id in enumerate(result_doc_ids, 1):
        movie = idx.docmap[doc_id]
        print(f"{i}. {movie['title']} (ID: {doc_id})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build the inverted index")

    args = parser.parse_args()

    match args.command:
        case "search":
            search(args.query)
        case "build":
            idx = InvertedIndex()
            idx.build()
            idx.save()

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
