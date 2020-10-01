from typing import Dict, Optional

from .config import mongo

__all__ = ["insert_or_replace", "find"]

db = mongo.db


def insert_or_replace(collection_name: str, query: Dict, replacement: Dict) -> None:
    """Insert a new document or replace an existing one.

    Insert a new document or replace an existing one in a collection.

    Args:
        collection_name (str): A collection name.
        query (Dict): A query that matches the document to replace.
        replacement (Dict): The new document.

    Returns:
        None
    """

    collection = db[collection_name]
    collection.replace_one(filter=query, replacement=replacement, upsert=True)


def find(collection_name: str, query: Dict) -> Optional[Dict]:
    """Get an existing document.

    Args:
        collection_name (str): A collection name.
        query (Dict): A query that matches the document to find.

    Returns:
        Dict: The document (if it exists).
        None: if the document does not exist.
    """

    collection = db[collection_name]
    return collection.find_one(filter=query)
