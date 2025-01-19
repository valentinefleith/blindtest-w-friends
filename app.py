import streamlit as st
from db import init_db
from src_pages import add_song, random_song, information


# Streamlit interface
def main():
    st.title("Blindtest avec les copaings")
    conn = init_db()

    # Navigation
    pages = ["Ajouter une chanson", "Chanson aléatoire", "Information"]
    page = st.sidebar.selectbox("Choisissez une page", pages)

    if page == "Ajouter une chanson":
        add_song.show_add_song(conn)
    elif page == "Chanson aléatoire":
        random_song.show_random_song(conn)
    elif page == "Information":
        information.show_information(conn)


if __name__ == "__main__":
    main()
