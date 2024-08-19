import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

ratings_data = {
    'User': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'The Godfather': [5, 4, np.nan, 3, np.nan],
    'Pulp Fiction': [4, np.nan, 5, 2, 1],
    'The Dark Knight': [np.nan, 2, 4, 1, 5],
    'Inception': [2, 3, np.nan, 5, 4],
    'Forrest Gump': [np.nan, np.nan, 4, 4, 3]
}

ratings_df = pd.DataFrame(ratings_data)
ratings_df.set_index('User', inplace=True)

def find_similar_users(ratings_df):
    filled_ratings = ratings_df.apply(lambda row: row.fillna(row.mean()), axis=1)
    user_correlation = filled_ratings.T.corr()
    return user_correlation

def suggest_items_collab(user_name, ratings_df, similarity_matrix, top_n=2):
    similar_users = similarity_matrix[user_name].drop(user_name).sort_values(ascending=False)
    recommended_movies = pd.Series(dtype='float64')

    for user, sim_score in similar_users.items():
        user_ratings = ratings_df.loc[user]
        unseen_movies = user_ratings[user_ratings.notna() & ~user_ratings.index.isin(ratings_df.loc[user_name].dropna().index)]
        
        for movie, score in unseen_movies.items():
            if movie not in recommended_movies:
                recommended_movies[movie] = sim_score * score
            else:
                recommended_movies[movie] += sim_score * score

    return recommended_movies.sort_values(ascending=False).head(top_n)

movie_features = {
    'The Godfather': ['Crime', 'Drama', None],
    'Pulp Fiction': ['Crime', 'Drama', None],
    'The Dark Knight': ['Action', 'Crime', 'Drama'],
    'Inception': ['Action', 'Adventure', 'Sci-Fi'],
    'Forrest Gump': ['Drama', 'Romance', None]
}

features_df = pd.DataFrame(movie_features).T

def compute_item_similarity(features_df):
    binary_features = pd.get_dummies(features_df.apply(pd.Series).stack()).groupby(level=0).sum()
    similarity_matrix = cosine_similarity(binary_features)
    return pd.DataFrame(similarity_matrix, index=binary_features.index, columns=binary_features.index)

def suggest_items_content(user_name, ratings_df, item_similarity_matrix, top_n=2):
    user_movies = ratings_df.loc[user_name].dropna()
    content_recommendations = pd.Series(dtype='float64')

    for movie, user_rating in user_movies.items():
        similar_movies = item_similarity_matrix[movie].drop(movie)
        
        for similar_movie, sim_score in similar_movies.items():
            if similar_movie not in content_recommendations:
                content_recommendations[similar_movie] = sim_score * user_rating
            else:
                content_recommendations[similar_movie] += sim_score * user_rating

    return content_recommendations.sort_values(ascending=False).head(top_n)

if __name__ == "__main__":
    print("Choose a user:")
    for idx, user in enumerate(ratings_df.index, 1):
        print(f"{idx}. {user}")

    user_choice = int(input("Enter the user number: "))

    if 1 <= user_choice <= len(ratings_df.index):
        chosen_user = ratings_df.index[user_choice - 1]
        print(f"\nYou selected: {chosen_user}")

        user_corr_matrix = find_similar_users(ratings_df)
        print(f"\nUser Correlation Matrix for {chosen_user}:")
        print(user_corr_matrix)

        collab_recommendations = suggest_items_collab(chosen_user, ratings_df, user_corr_matrix)
        print(f"\nCollaborative Filtering Suggestions for {chosen_user}:")
        print(collab_recommendations)

        item_similarity_matrix = compute_item_similarity(features_df)
        print("\nMovie Similarity Matrix:")
        print(item_similarity_matrix)

        content_recommendations = suggest_items_content(chosen_user, ratings_df, item_similarity_matrix)
        print(f"\nContent-Based Suggestions for {chosen_user}:")
        print(content_recommendations)
    else:
        print("Invalid choice. Please restart and select a valid user.")
