import sys
import sqlite3


def add_tag_to_file(tag_name, list_of_files: list[str]):
    print("add tag to file function")


def create_tag(tag_name: str):
    print("created tag to file function")

def remove_tag_from_file(tag_name: str, list_of_files: list[str]):
    print("removed tag to file function")

def delete_tag(tag_name: str):
    print("delete tag")


if __name__ == "__main__":

    print("we are in main function")

    if sys.argv[1] == "add":
        add_tag_to_file( sys.argv[2],sys.argv[3:]) 
    elif sys.argv[1] == "create":
        create_tag( sys.argv[2])
    elif sys.argv[1] == "remove":
        remove_tag_from_file( sys.argv[2],sys.argv[3:])
    elif sys.argv[1] == "delete":
        delete_tag(sys.argv[2])
