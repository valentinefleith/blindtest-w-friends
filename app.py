import streamlit as st
import sqlite3
import random

# Initialize database connection
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

# Add a song to the database
def add_song(conn, link):
    c = conn.cursor()
    c.execute("INSERT INTO songs (link) VALUES (?)", (link,))
    conn.commit()

# Get all songs
def get_all_songs(conn):
    c = conn.cursor()
    c.execute("SELECT link FROM songs")
    return [row[0] for row in c.fetchall()]

# Get a random song
def get_random_song(conn):
    songs = get_all_songs(conn)
    if songs:
        return random.choice(songs)
    return None

# Streamlit interface
def main():
    st.title("Song Collector with Player")
    conn = init_db()

    # Navigation
    pages = ["Add a Song", "Random Song"]
    page = st.sidebar.selectbox("Choose a page", pages)

    if page == "Add a Song":
        st.header("Add a Song")
        song_link = st.text_input("Enter the song link:")
        if st.button("Add Song"):
            if song_link:
                add_song(conn, song_link)
                st.success("Song added successfully!")
            else:
                st.error("Please enter a valid link.")
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
                elif "spotify.com" in random_song:
                    st.markdown(
                        f'<iframe src="{random_song}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>',
                        unsafe_allow_html=True,
                    )
                # Play audio files directly
                elif random_song.endswith((".mp3", ".wav")):
                    st.audio(random_song)
                else:
                    st.write(f"[Open the song here]({random_song})")
            else:
                st.warning("No songs in the database yet. Add some first!")

if __name__ == "__main__":
    main()
