import streamlit as st
import cbr

class visualizer():
    def __init__(self):
        self.name = None
        self.age = None
        self.gender = None
        self.origin = None
        self.favorite_genre = None
        self.recent_movies = []
        self.cbr_system = cbr.cbr()
        pass
    def run(self):
        st.title("Movie Recommender System")
        st.subheader("this system using case base reasoning method to recommend Movies for you")
        if "page" not in st.session_state:
            st.session_state.page = 0

        if st.session_state.page == 0:
            st.write("Sebutkan namamu?")
            self.name = st.text_input("Nama")
        elif st.session_state.page == 1:
            st.write("sebutkan gendermu?")
            self.gender = st.text_input("laki-laki/perempuan")
        elif st.session_state.page == 2:
            st.write("darimana asalmu?")
            self.origin = st.text_input("Asal")
        elif st.session_state.page == 3:
            st.write("Berapa umurmu?")
            self.age = st.text_input("Umur")
        elif st.session_state.page == 4:
            st.write("Apa genre favoritmu? (pisahkan dengan koma - contoh: Action, Comedy, Drama, adventure, animation, horror, thriller, romance)")
            self.recent_movies = st.text_area("Genre favoritmu (pisahkan dengan koma)").split(",")
            self.favorite_genre = st.text_input("Genre Favorit")
        elif st.session_state.page == 5:
            st.write("beritahu aku 3 film terakhir kamu baca")
            self.recent_movies = st.text_area("Film Terakhir (pisahkan dengan koma)").split(",")
        elif st.session_state.page == 6:
            st.write("Terima kasih telah mengisi data! Berikut adalah ringkasan informasi Anda:")
            st.write(f"**Nama:** {self.name}")
            st.write(f"film yang direkomendasikan untukmu adalah:")

            user_profile = f"{self.favorite_genre} " + " ".join(self.recent_movies)
            recommendations = self.cbr_system.recommend_movies(user_profile)
            for i, movie in enumerate(recommendations['title'], 1):
                st.write(f"{i}. {movie}")


        col1, col2, col3 = st.columns([1, 2, 1])

        if(st.session_state.page > 0):
            with col1:
                if st.button("← Previous"):
                    st.session_state.page = (st.session_state.page - 1)

        with col2:
            pass

        if st.session_state.page != 6:
            with col3:
                if st.button("Next →"):
                    st.session_state.page = (st.session_state.page + 1)

        if(st.session_state.page < 0):
            st.session_state.page = 0
        elif(st.session_state.page > 6):
            st.session_state.page = 6

        st.divider()

       