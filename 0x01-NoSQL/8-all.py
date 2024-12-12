#!/usr/bin/env python3
"""
Defines `list_all`.
"""


def list_all(mongo_collection):
    """
    Returns a list of docs in a given collection.
    """
    return [doc for doc in mongo_collection.find()]
