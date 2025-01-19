import streamlit as st
from db import get_random_song


def show_random_song(conn):
    st.header("Chanson aléatoire")
    if st.button("Tirer une chanson"):
        random_song = get_random_song(conn)
        if random_song:
            st.success("Voici une chanson aléatoire sélectionnée!")

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
