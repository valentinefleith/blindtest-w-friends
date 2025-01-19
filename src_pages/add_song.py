import streamlit as st
from db import add_song


def show_add_song(conn):
    st.header("Ajouter une chanson")
    song_link = st.text_input("Entre le lien d'une chanson (vidéo youtube):")
    first_name = st.text_input("Entre ton prénom:")
    last_name = st.text_input("Entre ton nom de famille:")
    if st.button("Ajouter une chanson"):
        if not first_name or not last_name:
            st.error("Les prénom et nom sont obligatoires!")
        if song_link and first_name and last_name:
            full_name = f"{first_name} {last_name}"
            add_song(conn, song_link, full_name)
            st.success("Chanson ajoutée avec succès!")
