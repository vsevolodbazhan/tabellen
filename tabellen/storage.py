from typing import Dict

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
    collection.replace_one(query, replacement, upsert=True)
