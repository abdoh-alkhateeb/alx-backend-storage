#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def main():
    """
    Entry point of program.
    """
    client = MongoClient()

    db = client.logs
    collection = db.nginx

    print(f"{collection.count_documents({})} logs")
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        condition = {"method": method}
        print(f"\tmethod {method}: {collection.count_documents(condition)}")

    condition = {"method": "GET", "path": "/status"}
    print(f"{collection.count_documents(condition)} status check")


if __name__ == "__main__":
    main()
