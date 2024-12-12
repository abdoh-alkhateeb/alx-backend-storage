#!/usr/bin/env python3
"""
Defines `update_topics`.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates docs with a given name to set given topics.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
