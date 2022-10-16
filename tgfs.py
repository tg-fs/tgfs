#!/usr/bin/env python

""""Tag Based File System"""

import sys
import sqlite3
import os


def check_if_init(cursor: sqlite3.Cursor):
    """"Check if database has been initialized"""
    check_tags_table_query = """SELECT name
FROM sqlite_master
WHERE type='table'
AND name='tags';"""

    check_file_list_table_query = """SELECT name
FROM sqlite_master
WHERE type='table'
AND name='file_list';"""

    tags_table_exists = cursor.execute(check_tags_table_query).fetchall() != []
    file_list_table_exists = cursor.execute(check_file_list_table_query).fetchall() != []

    return tags_table_exists and file_list_table_exists


def abort_if_no_init(cursor: sqlite3.Cursor):
    """If database not initialized, exit the program"""
    if not check_if_init(cursor):
        print("Database not initialized")
        sys.exit()


def add_tag_to_file(cursor: sqlite3.Cursor, tag_name: str, list_of_files: list[str]):
    """"Add a tag to a list of files"""
    abort_if_no_init(cursor)

    for file in list_of_files:
        add_query = f"INSERT INTO file_list VALUES('{os.path.abspath(file)}', '{tag_name}')"
        cursor.execute(add_query)
        # handle situation where same tag is added again


def create_tag(cursor: sqlite3.Cursor, tag_name: str):
    """Create a new tag"""
    abort_if_no_init(cursor)

    create_tag_query = f"INSERT INTO tags VALUES ('{tag_name}')"
    cursor.execute(create_tag_query)


def show_tags(cursor: sqlite3.Cursor):
    """"Show all existing tags"""
    abort_if_no_init(cursor)

    create_tag_query = "SELECT * FROM tags"
    tags = cursor.execute(create_tag_query)
    for tag in tags:
        print(tag[0]) # first element of row only


def remove_tag_from_file(cursor: sqlite3.Cursor, tag_name: str, list_of_files: list[str]):
    """"Remove a tag from list of files"""
    abort_if_no_init(cursor)

    # handle incorrect tag name

    for file in list_of_files:
        remove_query = f"""
        DELETE FROM file_list
WHERE tag_name = '{tag_name}' AND file_name = '{os.path.abspath(file)}'
"""
        cursor.execute(remove_query)

def delete_tag(cursor: sqlite3.Cursor, list_of_tags: list[str]):
    """"Delete a tag"""
    abort_if_no_init(cursor)

    # handle incorrect tag name
    for tag in list_of_tags:
        delete_tag_query = f"DELETE FROM tags WHERE name = '{tag}'"
        cursor.execute(delete_tag_query)


def init_db(cursor: sqlite3.Cursor):
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

    if check_if_init(cursor):
        print("Database already exists")
    else:
        cursor.execute(create_tags_table_query)
        cursor.execute(create_file_list_table_query)
        print("Database initialized")


def list_files_from_tag(cursor: sqlite3.Cursor, tag_name: str):
    """Shows all files with a given tag"""
    abort_if_no_init(cursor)

    fetch_files_query = f"SELECT * FROM file_list WHERE tag_name = '{tag_name}'"
    files = cursor.execute(fetch_files_query)
    for file in files:
        print(file[0])


def edit_tag(cursor: sqlite3.Cursor, old_tag_name: str, new_tag_name: str):
    """Edit tag name"""
    abort_if_no_init(cursor)

    cursor.execute("SELECT count(*) FROM tags WHERE name = ?", (new_tag_name,))
    data = cursor.fetchone()[0]
    if not data == 0:
        print(f"Tag with name {new_tag_name} alread exists")
        sys.exit(32)

    update_tag_name_query = f"""UPDATE tags
SET name = "{new_tag_name}"
WHERE name = "{old_tag_name}";
"""
    print(update_tag_name_query)
    cursor.execute(update_tag_name_query)

    update_file_tags_query = f"""UPDATE file_list
SET tag_name = "{new_tag_name}"
WHERE tag_name = "{old_tag_name}";
    """
    cursor.execute(update_file_tags_query)

def main():
    """The entrypoint"""

    sqlite_connection = sqlite3.connect(
        os.getenv("TGFS_DATABASE_PATH",
        os.path.expanduser("~/.tgfs.db")))

    if len(sys.argv) < 2:
        print("Not enough arguments")
        sys.exit()

    cursor = sqlite_connection.cursor()

    subcommand = sys.argv[1]
    if subcommand == "add":
        add_tag_to_file(cursor, sys.argv[2],sys.argv[3:])
    elif subcommand == "create":
        create_tag(cursor, sys.argv[2])
    elif subcommand == "remove":
        remove_tag_from_file(cursor, sys.argv[2],sys.argv[3:])
    elif subcommand == "delete":
        delete_tag(cursor, sys.argv[2:])
    elif subcommand == "init":
        init_db(cursor)
    elif subcommand == "tags":
        show_tags(cursor)
    elif subcommand == 'ls':
        list_files_from_tag(cursor, sys.argv[2])
    elif subcommand == "edit":
        edit_tag(cursor, sys.argv[2], sys.argv[3])
    else:
        print("Incorrect command format")

    sqlite_connection.commit()

    if cursor:
        cursor.close()

    if sqlite_connection:
        sqlite_connection.close()


if __name__ == "__main__":
    main()
