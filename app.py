import streamlit as st
import pickle
import pandas as pd
import requests
import os
import zipfile

if not os.path.exists("similarity.pkl"):
    with zipfile.ZipFile("similarity.pkl.zip", "r") as zip_ref:
        zip_ref.extractall()


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4a9344a1b884c0356bd04831c0f3ccb8&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# --- Load data ---
movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# --- Streamlit app ---
st.title("Movie Recommender System\nSAGAR SHARMA")

selected_movie_name = st.selectbox("Select a movie:", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
