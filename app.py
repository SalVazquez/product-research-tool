"""
Product Research Tool - Main Flask Application
Analyzes customer feedback from UserVoice and competitive landscape
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from analyzer import UserVoiceAnalyzer, CompetitiveAnalyzer

app = Flask(__name__)

# Initialize analyzers
uservoice_analyzer = UserVoiceAnalyzer()
competitive_analyzer = CompetitiveAnalyzer()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze a pain point:
    1. Search UserVoice for related feedback
    2. Synthesize themes and customer impact
    3. Research competitor solutions
    """
    try:
        data = request.json
        pain_point = data.get('pain_point', '').strip()

        if not pain_point:
            return jsonify({'error': 'Please provide a pain point description'}), 400

        # Step 1: Analyze UserVoice feedback
        print(f"Analyzing UserVoice for: {pain_point}")
        uservoice_results = uservoice_analyzer.analyze(pain_point)

        # Step 2: Analyze competitors
        print(f"Analyzing competitors for: {pain_point}")
        competitive_results = competitive_analyzer.analyze(pain_point)

        # Combine results
        response = {
            'pain_point': pain_point,
            'uservoice': uservoice_results,
            'competitive': competitive_results
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Product Research Tool...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
