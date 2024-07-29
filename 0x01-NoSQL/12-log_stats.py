#!/usr/bin/env python3
"""
Module for logging statistics from a MongoDB collection.

This script connects to a MongoDB instance, retrieves logs from the
nginx collection, and prints out statistics about the HTTP methods
and status checks present in the logs.
"""

from pymongo import MongoClient


def log_stats():
    """
    Prints log statistics from the nginx logs collection.

    Connects to the MongoDB server, retrieves the logs from the nginx
    collection, and prints the total number of logs, as well as the
    counts of different HTTP methods (GET, POST, PUT, PATCH, DELETE).
    Additionally, prints the number of logs that have a GET request
    to the path '/status'.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})

    # Define the query as a separate variable
    query = {"method": "GET", "path": "/status"}
    path = logs_collection.count_documents(query)

    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")


if __name__ == "__main__":
    log_stats()
