import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import os


# this class holds the implementation for case based reasoning method for expert system, 
# the historic cases are stored in data/tmdb_s5000_movies.csv, and based on user input,
# the system will recommend movies that fit the user's profile

class cbr : 
    def __init__(self, data_path='data/tmdb_5000_movies.csv'):
        """Initialize CBR system with movie cases from CSV file"""
        path = os.path.join(os.path.dirname(__file__), data_path)
        self.cases = pd.read_csv(path)
        self.features = None
        self.similarity_matrix = None

    def recommend_movies(self, user_profile, top_k=5):
        """Recommend movies based on user profile"""
        similar_movies, scores = self.__retrieve_similar_cases(user_profile, top_k)
        similar_movies = similar_movies.copy()
        similar_movies['similarity_score'] = scores
        
        return similar_movies
    
    def __retrieve_similar_cases(self, user_profile, top_k=5):
        """Retrieve top-k most similar cases"""
        similarities = self.__calculate_similarity(user_profile)
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        return self.cases.iloc[top_indices], similarities[top_indices]
    
    def __calculate_similarity(self, user_profile):
        """Calculate cosine similarity between user profile and cases"""
        # Decision-tree based CBR similarity

        # Build textual feature corpus
        text_series = (self.cases['genres'].fillna('') + ' ' +
                       self.cases['keywords'].fillna('') + ' ' +
                       self.cases['overview'].fillna('') + ' ' +
                       self.cases['overview'].fillna(''))

        vectorizer = CountVectorizer(max_features=500)
        X = vectorizer.fit_transform(text_series)

        # Choose a historical target to let the tree learn feature importance
        target_col = next((c for c in ['vote_average', 'popularity', 'vote_count'] if c in self.cases.columns), None)
        if target_col:
            y_raw = self.cases[target_col].fillna(self.cases[target_col].median())
            # Bin continuous targets to classification labels
            if y_raw.nunique() > 15:
                y = pd.qcut(y_raw, 5, labels=False, duplicates='drop')
            else:
                y = y_raw
        else:
            # Fallback synthetic target: coarse text length bucket
            y = (text_series.str.len() // 100).astype(int)

        clf = DecisionTreeClassifier(max_depth=10, random_state=42)
        clf.fit(X, y)

        # Vectorize user profile and get decision paths
        user_vector = vectorizer.transform([user_profile])
        user_path = clf.decision_path(user_vector)
        case_paths = clf.decision_path(X)

        # Compute Jaccard similarity over decision path node indices
        user_indices = set(user_path.indices[user_path.indptr[0]:user_path.indptr[1]])
        similarities = np.zeros(X.shape[0], dtype=float)

        for i in range(X.shape[0]):
            start, end = case_paths.indptr[i], case_paths.indptr[i + 1]
            case_indices = case_paths.indices[start:end]
            if not user_indices and len(case_indices) == 0:
                similarities[i] = 0.0
                continue
            intersection = len(user_indices.intersection(case_indices))
            union = len(user_indices.union(case_indices))
            similarities[i] = intersection / union if union else 0.0

        return similarities
        
    def __preprocess_features(self):
        """Extract and normalize features from cases"""
        # Select relevant features for similarity computation
        feature_cols = ['genres', 'keywords', 'overview']
        self.features = self.cases[feature_cols].fillna('')
        
    
        
    
        
  

