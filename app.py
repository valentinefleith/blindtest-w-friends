import streamlit as st
import sqlite3
import random
from pytubefix import YouTube

# Initialize database connection
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            user_name TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

# Update the schema and add the new column 'user_name'

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

# Streamlit interface
def main():
    st.title("Song Collector with Player")
    conn = init_db()

    # Navigation
    pages = ["Add a Song", "Random Song", "Information"]
    page = st.sidebar.selectbox("Choose a page", pages)

    if page == "Add a Song":
        st.header("Add a Song")
        song_link = st.text_input("Enter the song link:")
        first_name = st.text_input("Enter your First Name:")
        last_name = st.text_input("Enter your Last Name:")
        if st.button("Add Song"):
            if not first_name or not last_name:
                st.error("First name and last name are required!")
            if song_link and first_name and last_name:
                full_name = f"{first_name} {last_name}"
                add_song(conn, song_link, full_name)
                st.success("Song added successfully!")
    elif page == "Random Song":
        st.header("Random Song Picker")
        if st.button("Pick a Song"):
            random_song = get_random_song(conn)
            if random_song:
                st.success("Here's a random song for you!")
                
                # Embed YouTube or Spotify iframe if applicable
                if "youtube.com" in random_song or "youtu.be" in random_song:
                    st.markdown(
                        f'<iframe width="560" height="315" src="{random_song.replace("watch?v=", "embed/")}" frameborder="0" allowfullscreen></iframe>',
                        unsafe_allow_html=True,
                    )
                # Play audio files directly
                elif random_song.endswith((".mp3", ".wav")):
                    st.audio(random_song)
                else:
                    st.write(f"[Open the song here]({random_song})")
            else:
                st.warning("No songs in the database yet. Add some first!")
    elif page == "Information":
        st.header("Database Information")
        st.subheader("List of Songs")
        all_songs = get_all_songs(conn)
        if all_songs:
            for i, (link, user_name) in enumerate(all_songs, start=1):
                title = get_video_title(link)
                st.write(f"{i}. {title} ({link}) (Added by: {user_name})")
        else:
            st.warning("No songs in the database yet.")

if __name__ == "__main__":
    main()
