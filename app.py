from flask import Flask, request, render_template, jsonify
import os
from utils.recommendation_functions import get_course_recommendations
from utils.recommendation_extended_functions import get_extended_course_recommendations
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        user_input = request.form['user_input']
        no_of_recommendations = 5  # Number of recommendations you want to show
        recommended_courses = get_course_recommendations(user_input, no_of_recommendations)
        return render_template('recommendations.html', recommended_courses=recommended_courses)

@app.route('/recommend_extended', methods=['POST'])
def recommend_extended():
    if request.method == 'POST':
        user_input = request.form['user_input']
        no_of_recommendations = 5  # Number of recommendations you want to show
        recommended_extended_courses = get_extended_course_recommendations(user_input, no_of_recommendations)
        return render_template('recommendations_extended.html', recommended_courses=recommended_extended_courses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=('/etc/letsencrypt/live/courserecommendation.chickenkiller.com/fullchain.pem', '/etc/letsencrypt/live/courserecommendation.chickenkiller.com/privkey.pem'))
