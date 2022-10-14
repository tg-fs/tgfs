""""Tag Based File System"""

import sys
import sqlite3


def check_if_init(sqlite_connection: sqlite3.Connection):
    """"Check if database has been initialized"""
    check_tags_table_query = """SELECT name
FROM sqlite_master
WHERE type='table'
AND name='tags';"""

    check_file_list_table_query = """SELECT name
FROM sqlite_master
WHERE type='table'
AND name='file_list';"""

    cursor = sqlite_connection.cursor()
    tags_table_exists = cursor.execute(check_tags_table_query).fetchall() != []
    file_list_table_exists = cursor.execute(check_file_list_table_query).fetchall() != []

    return tags_table_exists and file_list_table_exists


def abort_if_no_init(sqlite_connection: sqlite3.Connection):
    """If database not initialized, exit the program"""
    if not check_if_init(sqlite_connection):
        print("Database not initialized")
        sys.exit()


def add_tag_to_file(_tag_name, _list_of_files: list[str]):
    """"Add a tag to a list of files"""
    print("add tag to file function")


def create_tag(sqlite_connection: sqlite3.Connection, tag_name: str):
    """Create a new tag"""
    abort_if_no_init(sqlite_connection)

    create_tag_query = f"INSERT INTO tags VALUES ('{tag_name}')"
    sqlite_connection.cursor().execute(create_tag_query)
    sqlite_connection.commit()


def show_tags(sqlite_connection: sqlite3.Connection):
    """"Show all existing tags"""
    abort_if_no_init(sqlite_connection)

    create_tag_query = "SELECT * FROM tags"
    tags = sqlite_connection.cursor().execute(create_tag_query)
    for tag in tags:
        print(tag[0]) # first element of row only


def remove_tag_from_file(_tag_name: str, _list_of_files: list[str]):
    """"Remove a tag from list of files"""
    print("removed tag to file function")


def delete_tag(_tag_name: str):
    """"Delete a tag"""
    print("delete tag")


def init_db(sqlite_connection: sqlite3.Connection):
    """"Initialize the tgfs database"""
    create_tags_table_query = '''CREATE TABLE tags
(
  name VARCHAR(256) NOT NULL,
  PRIMARY KEY (name)
);'''
    create_file_list_table_query = '''CREATE TABLE file_list
(
  file_name VARCHAR(1024) NOT NULL,
  tag_name VARCHAR(256) NOT NULL,
  PRIMARY KEY (file_name, tag_name)
);'''

    if check_if_init(sqlite_connection):
        print("Database already exists")
    else:
        sqlite_connection.cursor().execute(create_tags_table_query)
        sqlite_connection.cursor().execute(create_file_list_table_query)
        sqlite_connection.commit()
        print("Database initialized")


def main():
    """The entrypoint"""

    sqlite_connection = sqlite3.connect('.tgfs.db')

    if len(sys.argv) < 2:
        print("Not enough arguments")
        sys.exit()

    subcommand = sys.argv[1]
    if subcommand == "add":
        add_tag_to_file(sys.argv[2],sys.argv[3:])
    elif subcommand == "create":
        create_tag(sqlite_connection, sys.argv[2])
    elif subcommand == "remove":
        remove_tag_from_file( sys.argv[2],sys.argv[3:])
    elif subcommand == "delete":
        delete_tag(sys.argv[2])
    elif subcommand == "init":
        init_db(sqlite_connection)
    elif subcommand == "tags":
        show_tags(sqlite_connection)
    else:
        print("Incorrect command format")

    if sqlite_connection:
        sqlite_connection.close()


if __name__ == "__main__":
    main()
