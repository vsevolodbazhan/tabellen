from typing import Dict, Optional

from .config import mongo

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
    collection = db[collection_name]
    return collection.find_one(filter=query)
