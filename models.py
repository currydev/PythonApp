import sqlite3

DATABASE = 'url_metadata.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def insert_url_metadata(metadata):
    conn = get_db_connection()
    conn.execute('INSERT INTO metadata (title, description, image, url) VALUES (?, ?, ?, ?)',
                 (metadata['title'], metadata['description'], metadata['image'], metadata['url']))
    conn.commit()
    conn.close()

def get_all_metadata():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM metadata').fetchall()
    conn.close()
    return items
