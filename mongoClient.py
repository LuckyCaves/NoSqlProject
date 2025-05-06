#!/usr/bin/env python3
import argparse
import logging
import os
import requests
import json


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('clinic.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv("CLINIC_API_URL", "http://localhost:8000")

def main():
    log.info(f"Welcome to books catalog. App requests to: {BOOKS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    parser.add_argument("-i", "--id",
            help="Provide a book ID which related to the book action", default=None)
    parser.add_argument("-r", "--rating",
            help="Search parameter to look for books with average rating equal or above the param (0 to 5)", default=None)

    args = parser.parse_args()

    if args.id and not args.action in ["get", "update", "delete"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if args.rating and args.action != "search":
        log.error(f"Rating arg can only be used with search action")
        exit(1)

    if args.action == "search":
        list_books(args.rating)
    elif args.action == "get" and args.id:
        get_book_by_id(args.id)
    elif args.action == "update":
        update_book(args.id)
    elif args.action == "delete":
        delete_book(args.id)

if __name__ == "__main__":
    main()