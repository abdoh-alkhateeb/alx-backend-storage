#!/usr/bin/env python3
"""
Defines `insert_school`.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a doc in a given collection.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
