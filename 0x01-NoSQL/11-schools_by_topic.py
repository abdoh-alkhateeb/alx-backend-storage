#!/usr/bin/env python3
"""
Defines `schools_by_topic`.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic.
    """
    return [doc for doc in mongo_collection.find({"topics": topic})]
