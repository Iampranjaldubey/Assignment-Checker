"""
Assignment Checker Backend
A Flask application that checks student assignments for:
- Word count
- Missing sections (Introduction, Body, Conclusion)
- Long sentences (over 20 words)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
# Enable CORS to allow frontend to communicate with backend
CORS(app)

# Database file path
DATABASE = 'assignments.db'

def init_db():
    """
    Initialize the SQLite database.
    Creates a table to store assignment submissions if it doesn't exist.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            assignment_text TEXT NOT NULL,
            word_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create reports table to store analysis results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            word_count INTEGER,
            has_introduction BOOLEAN,
            has_body BOOLEAN,
            has_conclusion BOOLEAN,
            long_sentences_count INTEGER,
            long_sentences TEXT,
            overall_score INTEGER,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assignment_id) REFERENCES assignments (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def count_words(text):
    """
    Count the number of words in a text.
    Splits text by whitespace and counts non-empty strings.
    
    Args:
        text (str): The text to count words in
        
    Returns:
        int: Number of words
    """
    words = text.split()
    return len(words)

def check_sections(text):
    """
    Check if the assignment has required sections:
    - Introduction
    - Body
    - Conclusion
    
    Args:
        text (str): The assignment text
        
    Returns:
        dict: Dictionary with boolean values for each section
    """
    text_lower = text.lower()
    
    # Check for introduction (look for keywords)
    has_intro = any(keyword in text_lower for keyword in 
                   ['introduction', 'intro', 'introduce'])
    
    # Check for body (look for keywords or assume it exists if text is long enough)
    has_body = any(keyword in text_lower for keyword in 
                  ['body', 'main', 'content', 'discuss']) or len(text.split()) > 50
    
    # Check for conclusion (look for keywords)
    has_conclusion = any(keyword in text_lower for keyword in 
                        ['conclusion', 'conclude', 'summary', 'summarize'])
    
    return {
        'has_introduction': has_intro,
        'has_body': has_body,
        'has_conclusion': has_conclusion
    }

def find_long_sentences(text, max_words=20):
    """
    Find sentences that exceed the maximum word count.
    
    Args:
        text (str): The assignment text
        max_words (int): Maximum words allowed per sentence (default: 20)
        
    Returns:
        tuple: (count of long sentences, list of long sentences)
    """
    # Split text into sentences using common punctuation
    sentences = re.split(r'[.!?]+', text)
    
    long_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:  # Skip empty strings
            word_count = len(sentence.split())
            if word_count > max_words:
                long_sentences.append(sentence)
    
    return len(long_sentences), long_sentences

def analyze_assignment(text):
    """
    Analyze an assignment and generate a comprehensive report.
    
    Args:
        text (str): The assignment text
        
    Returns:
        dict: Analysis report with scores and feedback
    """
    # Count words
    word_count = count_words(text)
    
    # Check sections
    sections = check_sections(text)
    
    # Find long sentences
    long_count, long_sentences = find_long_sentences(text)
    
    # Calculate overall score (out of 100)
    score = 100
    
    # Deduct points for missing sections (20 points each)
    if not sections['has_introduction']:
        score -= 20
    if not sections['has_body']:
        score -= 20
    if not sections['has_conclusion']:
        score -= 20
    
    # Deduct points for long sentences (2 points each, max 20 points)
    score -= min(long_count * 2, 20)
    
    # Deduct points if word count is too low (less than 200 words)
    if word_count < 200:
        score -= min((200 - word_count) // 10, 20)
    
    # Ensure score doesn't go below 0
    score = max(0, score)
    
    # Generate feedback
    feedback_parts = []
    
    if word_count < 200:
        feedback_parts.append(f"⚠️ Word count is {word_count}, which is below the recommended 200 words.")
    else:
        feedback_parts.append(f"✅ Word count: {word_count} words (Good!)")
    
    if not sections['has_introduction']:
        feedback_parts.append("❌ Missing Introduction section.")
    else:
        feedback_parts.append("✅ Introduction section found.")
    
    if not sections['has_body']:
        feedback_parts.append("❌ Missing Body section.")
    else:
        feedback_parts.append("✅ Body section found.")
    
    if not sections['has_conclusion']:
        feedback_parts.append("❌ Missing Conclusion section.")
    else:
        feedback_parts.append("✅ Conclusion section found.")
    
    if long_count > 0:
        feedback_parts.append(f"⚠️ Found {long_count} sentence(s) with more than 20 words. Consider breaking them into shorter sentences.")
    else:
        feedback_parts.append("✅ All sentences are within the recommended length.")
    
    feedback = "\n".join(feedback_parts)
    
    return {
        'word_count': word_count,
        'sections': sections,
        'long_sentences_count': long_count,
        'long_sentences': long_sentences[:5],  # Limit to first 5 for display
        'overall_score': score,
        'feedback': feedback
    }

@app.route('/api/submit', methods=['POST'])
def submit_assignment():
    """
    API endpoint to submit an assignment.
    Accepts POST request with JSON containing student_name and assignment_text.
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        student_name = data.get('student_name', '').strip()
        assignment_text = data.get('assignment_text', '').strip()
        
        if not student_name:
            return jsonify({'error': 'Student name is required'}), 400
        
        if not assignment_text:
            return jsonify({'error': 'Assignment text is required'}), 400
        
        # Count words
        word_count = count_words(assignment_text)
        
        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO assignments (student_name, assignment_text, word_count)
            VALUES (?, ?, ?)
        ''', (student_name, assignment_text, word_count))
        
        assignment_id = cursor.lastrowid
        
        # Analyze assignment
        analysis = analyze_assignment(assignment_text)
        
        # Save report to database
        cursor.execute('''
            INSERT INTO reports (
                assignment_id, word_count, has_introduction, has_body, 
                has_conclusion, long_sentences_count, long_sentences, 
                overall_score, feedback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            assignment_id,
            analysis['word_count'],
            analysis['sections']['has_introduction'],
            analysis['sections']['has_body'],
            analysis['sections']['has_conclusion'],
            analysis['long_sentences_count'],
            '\n'.join(analysis['long_sentences']),
            analysis['overall_score'],
            analysis['feedback']
        ))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Return success response with report
        return jsonify({
            'success': True,
            'assignment_id': assignment_id,
            'report_id': report_id,
            'report': analysis
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report/<int:assignment_id>', methods=['GET'])
def get_report(assignment_id):
    """
    API endpoint to retrieve a report for a specific assignment.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM reports WHERE assignment_id = ?
        ''', (assignment_id,))
        
        report = cursor.fetchone()
        conn.close()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Convert to dictionary
        report_dict = {
            'id': report[0],
            'assignment_id': report[1],
            'word_count': report[2],
            'has_introduction': bool(report[3]),
            'has_body': bool(report[4]),
            'has_conclusion': bool(report[5]),
            'long_sentences_count': report[6],
            'long_sentences': report[7].split('\n') if report[7] else [],
            'overall_score': report[8],
            'feedback': report[9],
            'created_at': report[10]
        }
        
        return jsonify(report_dict), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assignments', methods=['GET'])
def get_assignments():
    """
    API endpoint to retrieve all assignments.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.student_name, a.word_count, a.created_at, r.overall_score
            FROM assignments a
            LEFT JOIN reports r ON a.id = r.assignment_id
            ORDER BY a.created_at DESC
        ''')
        
        assignments = cursor.fetchall()
        conn.close()
        
        assignments_list = []
        for assignment in assignments:
            assignments_list.append({
                'id': assignment[0],
                'student_name': assignment[1],
                'word_count': assignment[2],
                'created_at': assignment[3],
                'overall_score': assignment[4]
            })
        
        return jsonify(assignments_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return jsonify({'status': 'healthy', 'message': 'Assignment Checker API is running'}), 200

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    print("Database initialized!")
    print("Starting Flask server on http://localhost:5000")
    # Run the Flask app
    app.run(debug=True, port=5000)

