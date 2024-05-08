
# Importing required modules
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Function to extract keywords from user input
def extract_user_keywords(user_input):
    # Tokenization and preprocessing with lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(user_input.lower())
    stop_words = set(stopwords.words("english"))
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]

    # Convert tokens back to text for TF-IDF
    input_text = " ".join(tokens)

    # Compute TF-IDF scores
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([input_text])
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Rank and select keywords based on TF-IDF scores
    keywords = [feature_names[idx] for idx in tfidf_matrix.indices]

    return keywords

# Function to calculate cosine similarity between user input and course descriptions
def similarity_scores(user_tfidf, tfidf_matrix):
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix)
    return similarity_scores

# Function to rank courses based on similarity scores
def rank_course(similarity_scores, course_data):
    course_data['similarity'] = similarity_scores[0]

# Function to recommend courses
def recommend_courses(course_data, no_of_recommendations):
    recommended_courses = course_data.sort_values(by='similarity', ascending=False)[['name', 'similarity']].head(no_of_recommendations)
    return recommended_courses

# Function to get course recommendations based on user input
def get_course_recommendations(user_input, no_of_recommendations):
    # Importing the csv file
    course_data = pd.read_csv("./data/output_updated.csv")

    # Data cleaning
    # Drop the unnecessary columns
    course_data.drop(columns=['figma_link', 'created_at', 'author_id', 'grade_low', 'grade_high'], inplace=True)
    # Rename the columns
    course_data.rename(columns={'title': 'name', 'topic_group': 'category', 'skill_group':'competency_area' }, inplace=True)

    # Data manipulation
    # Create a WordNetLemmatizer object
    lemmatizer = WordNetLemmatizer()

    # Convert text attributes to lowercase
    course_data['course_name'] = course_data['name'].str.lower()
    course_data['description'] = course_data['description'].str.lower()
    course_data['category'] = course_data['category'].str.lower()
    course_data['skill_groups'] = course_data['skill_groups'].str.lower()
    course_data['skills'] = course_data['skills'].str.lower()

    # Remove "-" characters and replace them with spaces
    course_data['course_name'] = course_data['course_name'].apply(lambda x: x.replace("-", " "))
    course_data['description'] = course_data['description'].apply(lambda x: x.replace("-", " "))
    course_data['category'] = course_data['category'].apply(lambda x: x.replace("-", " "))

    # Remove punctuation from text attributes
    course_data['course_name'] = course_data['course_name'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    course_data['description'] = course_data['description'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    course_data['category'] = course_data['category'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))

    # Lemmatize text attributes in each row of the DataFrame
    course_data['course_name'] = course_data['course_name'].apply(lambda x: [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(x)])
    course_data['category'] = course_data['category'].apply(lambda x: [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(x)])
    course_data['description'] = course_data['description'].apply(lambda x: [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(x)])
    course_data['skill_groups'] = course_data['skill_groups'].apply(lambda x: [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(x)])
    course_data['skills'] = course_data['skills'].apply(lambda x: [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(x)])

    # Combine text attributes
    course_data['combined_text'] = course_data['skills'] + course_data['skill_groups'] + course_data['description'] + course_data['category'] + course_data['course_name']

    # Combine text attributes
    course_data['combined_text'] = course_data['combined_text'].apply(lambda x: ' '.join(x))

    # Vectorize text data
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(course_data['combined_text'])

    # Transform user input into TF-IDF vector
    keywords = extract_user_keywords(user_input)
    user_tfidf = vectorizer.transform([' '.join(keywords)])

    # Calculate cosine similarity
    scores = similarity_scores(user_tfidf, tfidf_matrix)

    # Rank courses based on similarity scores
    rank_course(scores, course_data)

    # Recommend top courses
    recommended_courses = recommend_courses(course_data, no_of_recommendations)

    recommendations_json = recommended_courses.to_json(orient='records')
    # print(recommended_courses_json)
    # Print recommended courses
    # print("Recommended Courses:")
    # for course in recommended_courses:
    #     print(course)
    
    return recommendations_json

# Sample usage:
get_course_recommendations("I want to learn how to effectively communicate with my team", 5)
