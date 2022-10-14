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

def init_db(sqliteConnection: sqlite3.Connection):
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
    sqliteConnection.cursor().execute(init_db_query)
    sqliteConnection.commit()
    print("Database initialized")


if __name__ == "__main__":

    print("we are in main function")

    sqliteConnection = sqlite3.connect('~/.tgfs.db')

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
        init_db(sqliteConnection)
    else:
        print("Incorrect command format")
    
    if sqliteConnection:
        sqliteConnection.close()
