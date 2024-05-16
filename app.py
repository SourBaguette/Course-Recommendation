from flask import Flask, request, render_template, jsonify, redirect
import os
from utils.recommendation_functions import get_course_recommendations
from utils.recommendation_extended_functions import get_extended_course_recommendations
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        data = request.json
        user_input = data.get('user_input')
        no_of_recommendations = 5  # Number of recommendations you want to show
        recommended_courses = get_course_recommendations(user_input, no_of_recommendations)
        print(recommended_courses)
        # return render_template('recommendations.html', recommended_courses=recommended_courses)
        return ({'recommended_courses': recommended_courses})

@app.route('/recommend_extended', methods=['POST'])
def recommend_extended():
    if request.method == 'POST':
        data = request.json
        user_input = data.get('user_input')
        no_of_recommendations = 5  # Number of recommendations you want to show
        recommended_extended_courses = get_extended_course_recommendations(user_input, no_of_recommendations)
        # return render_template('recommendations_extended.html', recommended_courses=recommended_extended_courses)
        return ({'recommended_courses': recommended_extended_courses})


from flask import redirect

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        feedback_data = request.json
        
        # Extract values from feedback_data
        feedback = feedback_data['feedback']
        search_type = feedback_data['searchType']
        recommended_courses = feedback_data['recommendedCourses']
        
        # Modify the connection string according to your database location
        with sqlite3.connect('../feedback/userfeedback.db') as connection:
            cursor = connection.cursor()
            # Insert feedback data into SQLite database
            cursor.execute("INSERT INTO userfeedback (search_type, feedback, recommended_courses) VALUES (?, ?, ?)",
                           (search_type, feedback, recommended_courses))
            connection.commit()
    
    # If the request method is not POST
    return jsonify({'error': 'Invalid request method'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=('/etc/letsencrypt/live/courserecommendation.chickenkiller.com/fullchain.pem', '/etc/letsencrypt/live/courserecommendation.chickenkiller.com/privkey.pem'))
    # app.run()