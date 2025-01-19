import streamlit as st
from db import get_all_songs, get_video_title


def show_information(conn):
    st.header("Database Information")
    st.subheader("Liste des chansons")
    all_songs = get_all_songs(conn)
    if all_songs:
        for i, (link, user_name) in enumerate(all_songs, start=1):
            title = get_video_title(link)
            st.write(f"{i}. {title} ({link}) (Added by: {user_name})")
    else:
        st.warning("No songs in the database yet.")
