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
# Import our AI feedback module (using Google Gemini)
from gemini_feedback import generate_ai_feedback

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
    # Added AI feedback fields: ai_overall_evaluation, ai_strengths, ai_weaknesses, ai_suggestions
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
            ai_overall_evaluation TEXT,
            ai_strengths TEXT,
            ai_weaknesses TEXT,
            ai_suggestions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assignment_id) REFERENCES assignments (id)
        )
    ''')
    
    # Add AI feedback columns to existing reports table if they don't exist
    # This is a migration: checks if columns exist before adding them
    cursor.execute("PRAGMA table_info(reports)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'ai_overall_evaluation' not in columns:
        cursor.execute('ALTER TABLE reports ADD COLUMN ai_overall_evaluation TEXT')
    if 'ai_strengths' not in columns:
        cursor.execute('ALTER TABLE reports ADD COLUMN ai_strengths TEXT')
    if 'ai_weaknesses' not in columns:
        cursor.execute('ALTER TABLE reports ADD COLUMN ai_weaknesses TEXT')
    if 'ai_suggestions' not in columns:
        cursor.execute('ALTER TABLE reports ADD COLUMN ai_suggestions TEXT')
    
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
        
        # Analyze assignment (rule-based checks)
        analysis = analyze_assignment(assignment_text)
        
        # Generate AI feedback
        # We use a try-except block here because AI feedback might fail
        # but we still want to save the assignment with basic analysis
        ai_feedback = None
        ai_error = None
        
        try:
            ai_feedback = generate_ai_feedback(assignment_text)
        except Exception as e:
            # Log the error but don't fail the entire request
            ai_error = str(e)
            print(f"AI feedback generation failed: {ai_error}")
        
        # Prepare AI feedback data for database storage
        # We store lists as JSON strings in the database
        ai_overall_eval = None
        ai_strengths_json = None
        ai_weaknesses_json = None
        ai_suggestions_json = None
        
        if ai_feedback:
            import json as json_lib
            ai_overall_eval = ai_feedback.get('overall_evaluation')
            ai_strengths_json = json_lib.dumps(ai_feedback.get('strengths', []))
            ai_weaknesses_json = json_lib.dumps(ai_feedback.get('weaknesses', []))
            ai_suggestions_json = json_lib.dumps(ai_feedback.get('suggestions', []))
        
        # Save report to database (including AI feedback)
        cursor.execute('''
            INSERT INTO reports (
                assignment_id, word_count, has_introduction, has_body, 
                has_conclusion, long_sentences_count, long_sentences, 
                overall_score, feedback, ai_overall_evaluation, 
                ai_strengths, ai_weaknesses, ai_suggestions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            assignment_id,
            analysis['word_count'],
            analysis['sections']['has_introduction'],
            analysis['sections']['has_body'],
            analysis['sections']['has_conclusion'],
            analysis['long_sentences_count'],
            '\n'.join(analysis['long_sentences']),
            analysis['overall_score'],
            analysis['feedback'],
            ai_overall_eval,
            ai_strengths_json,
            ai_weaknesses_json,
            ai_suggestions_json
        ))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Return success response with report and AI feedback
        return jsonify({
            'success': True,
            'assignment_id': assignment_id,
            'report_id': report_id,
            'report': analysis,
            'ai_feedback': ai_feedback,  # Will be None if AI failed
            'ai_error': ai_error  # Will be None if AI succeeded
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
        # Handle cases where AI feedback columns might not exist (for older records)
        import json as json_lib
        
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
        }
        
        # Add AI feedback fields if they exist
        # Check the length of the report tuple to see if AI fields are present
        if len(report) > 10:
            # Parse JSON strings back to lists
            ai_feedback_dict = {}
            if report[10]:  # ai_overall_evaluation
                ai_feedback_dict['overall_evaluation'] = report[10]
            if report[11]:  # ai_strengths
                try:
                    ai_feedback_dict['strengths'] = json_lib.loads(report[11])
                except:
                    ai_feedback_dict['strengths'] = []
            if report[12]:  # ai_weaknesses
                try:
                    ai_feedback_dict['weaknesses'] = json_lib.loads(report[12])
                except:
                    ai_feedback_dict['weaknesses'] = []
            if report[13]:  # ai_suggestions
                try:
                    ai_feedback_dict['suggestions'] = json_lib.loads(report[13])
                except:
                    ai_feedback_dict['suggestions'] = []
            
            if ai_feedback_dict:
                report_dict['ai_feedback'] = ai_feedback_dict
        
        report_dict['created_at'] = report[-1] if len(report) > 10 else report[10]
        
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

@app.route('/api/check', methods=['POST'])
def check_assignment():
    """
    API endpoint to check an assignment without saving to database.
    This is a lightweight endpoint that returns analysis results including AI feedback.
    
    Accepts POST request with JSON containing assignment_text.
    Returns analysis report with both rule-based checks and AI feedback.
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        assignment_text = data.get('assignment_text', '').strip()
        
        if not assignment_text:
            return jsonify({'error': 'Assignment text is required'}), 400
        
        # Perform rule-based analysis (word count, sections, long sentences)
        analysis = analyze_assignment(assignment_text)
        
        # Generate AI feedback
        # We use a try-except block here because AI feedback might fail
        # (e.g., API key issues, network problems) but we still want to return the basic analysis
        ai_feedback = None
        ai_error = None
        
        try:
            ai_feedback = generate_ai_feedback(assignment_text)
        except Exception as e:
            # Log the error but don't fail the entire request
            # This way, users still get the basic analysis even if AI is unavailable
            ai_error = str(e)
            print(f"AI feedback generation failed: {ai_error}")
        
        # Prepare the response
        response_data = {
            'success': True,
            'report': analysis,
            'ai_feedback': ai_feedback,  # Will be None if AI failed
            'ai_error': ai_error  # Will be None if AI succeeded
        }
        
        return jsonify(response_data), 200
        
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

