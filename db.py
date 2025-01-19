import sqlite3
import random
from pytubefix import YouTube


# Initialize database connection
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            user_name TEXT NOT NULL
        )
    """
    )
    conn.commit()
    return conn


# Add a song to the database
def add_song(conn, link, user_name):
    c = conn.cursor()
    c.execute("INSERT INTO songs (link, user_name) VALUES (?, ?)", (link, user_name))
    conn.commit()


# Get all songs
def get_all_songs(conn):
    c = conn.cursor()
    c.execute("SELECT link, user_name FROM songs")
    return c.fetchall()


# Get a random song
def get_random_song(conn):
    songs = [song[0] for song in get_all_songs(conn)]
    if songs:
        return random.choice(songs)
    return None


# Extract video title from YouTube link
def get_video_title(youtube_link):
    try:
        yt = YouTube(youtube_link)
        return yt.title
    except Exception as e:
        return "Unknown Title (Invalid Link)"
