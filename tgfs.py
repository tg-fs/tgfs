""""Tag Based File System"""

import sys
import sqlite3


def add_tag_to_file(_tag_name, _list_of_files: list[str]):
    """"Add a tag to a list of files"""
    print("add tag to file function")


def create_tag(_tag_name: str):
    """Create a new tag"""
    print("created tag to file function")


def remove_tag_from_file(_tag_name: str, _list_of_files: list[str]):
    """"Remove a tag from list of files"""
    print("removed tag to file function")


def delete_tag(_tag_name: str):
    """"Delete a tag"""
    print("delete tag")


def init_db(sqlite_connection: sqlite3.Connection):
    """"Initialize the tgfs database"""
    init_db_query = '''CREATE TABLE tags
(
  name VARCHAR(256) NOT NULL,
  PRIMARY KEY (name)
);

CREATE TABLE file_list
(
  file_name VARCHAR(1024) NOT NULL,
  tag_name VARCHAR(256) NOT NULL,
  PRIMARY KEY (file_name, tag_name)
);'''
    sqlite_connection.cursor().execute(init_db_query)
    sqlite_connection.commit()
    print("Database initialized")


def main():
    """The entrypoint"""

    print("we are in main function")

    sqlite_connection = sqlite3.connect('~/.tgfs.db')

    subcommand = sys.argv[1]

    if subcommand == "add":
        add_tag_to_file(sys.argv[2],sys.argv[3:])
    elif subcommand == "create":
        create_tag( sys.argv[2])
    elif subcommand == "remove":
        remove_tag_from_file( sys.argv[2],sys.argv[3:])
    elif subcommand == "delete":
        delete_tag(sys.argv[2])
    elif subcommand == "init":
        init_db(sqlite_connection)
    else:
        print("Incorrect command format")

    if sqlite_connection:
        sqlite_connection.close()


if __name__ == "__main__":
    main()
