import pandas as pd

favourite_movie = ""

#define a function to compute row average
def row_average(row):
    return row.mean()

#importing csv files
links = pd.read_csv("ml-latest-small/links.csv")
movies = pd.read_csv("ml-latest-small/movies.csv")
ratings = pd.read_csv("ml-latest-small/ratings.csv")
tags = pd.read_csv("ml-latest-small/tags.csv")

while True:
    #choose favourite movies
    favourite_movie = input("What's your favourite movie? (If you want to end the program enter end): ")

    if favourite_movie=="end":
        quit()

    #information on the basic movie
    favourite_movie_list = movies.loc[movies["title"].str.contains(favourite_movie, case=False, na=False)]

    if favourite_movie_list.empty:
        print("We couldn't find this movie.")
    else:
        favourite_genres = str(favourite_movie_list["genres"].values[0])

        #making a dataframe of movies that could possibly be liked by the user BASED ON THE GENRE
        possibly_liked_movies_genre = movies.loc[movies["genres"] == favourite_genres]

        sorted_ratings_genre = pd.merge(possibly_liked_movies_genre, ratings, on="movieId").sort_values("rating", ascending=False)

        #find similar tags

        #get movie IDs for the favourite movie to find tags associated with it
        favourite_movie_id = favourite_movie_list["movieId"].values[0]
        movie_tags = tags.loc[tags["movieId"] == favourite_movie_id]["tag"].unique()

        #find all movies with the same tags as the favourite movie
        similar_tagged_movies = tags[tags["tag"].isin(movie_tags)]
        similar_movie_ids = similar_tagged_movies["movieId"].unique()

        #filter movies with similar tags
        possibly_liked_movies_tags = movies[movies["movieId"].isin(similar_movie_ids)]

        #merge with ratings and sort by rating
        sorted_ratings_tags = pd.merge(possibly_liked_movies_tags, ratings, on="movieId").sort_values("rating", ascending=False)

        #combine genre and tag ratings
        combine = [sorted_ratings_genre, sorted_ratings_tags]
        sorted_ratings_avg = pd.concat(combine)

        #group the ratings by 'title' and calculate the mean rating for each movie and sort it
        sorted_ratings_avg = sorted_ratings_avg.groupby("title")["rating"].mean().reset_index().sort_values("rating", ascending=False).head(5)

        delimiter_space = ", "

        recommended_movies = sorted_ratings_avg["title"].to_list()

        #find any duplicates

        found_double_movie = False

        for movie in recommended_movies:
            if favourite_movie.upper() in movie.upper():
                recommended_movies.remove(movie)  
                found_double_movie = True
                break

        if not found_double_movie:
            recommended_movies.pop()

        print("Based on your preferences we would recommend the following movies:\n" + delimiter_space.join(recommended_movies))