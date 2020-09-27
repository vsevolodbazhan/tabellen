from typing import Dict

from .config import mongo

db = mongo.db


def insert_or_replace(collection_name: str, _filter: Dict, replacement: Dict) -> None:
    """Insert a new document or replace an existing one.

    Insert a new document or replace an existing one in a collection.

    Args:
        collection_name (str): A collection name.
        _filter (Dict): A query that matches the document to replace.
        replacement (Dict): The new document.

    Returns:
        None
    """

    collection = db[collection_name]
    collection.replace_one(_filter, replacement, upsert=True)
