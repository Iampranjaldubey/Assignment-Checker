# 📝 Assignment Checker

A full-stack web application that helps students check their assignments for common issues like word count, missing sections, and long sentences.

## 🎯 Features

- **Word Count Check**: Verifies if the assignment meets the minimum word requirement (200 words)
- **Section Detection**: Checks for Introduction, Body, and Conclusion sections
- **Sentence Length Analysis**: Identifies sentences longer than 20 words
- **Comprehensive Report**: Provides detailed feedback with an overall score
- **Modern UI**: Beautiful, responsive design with smooth animations

## 🛠️ Tech Stack

### Backend
- **Python 3.x**: Programming language
- **Flask**: Web framework for building the API
- **SQLite**: Lightweight database for storing submissions and reports
- **Flask-CORS**: Enables cross-origin requests

### Frontend
- **React**: UI library for building interactive components
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and development server
- **CSS3**: Modern styling with gradients and animations

## 📁 Project Structure

```
Assignment-Checker/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── assignments.db      # SQLite database (created automatically)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AssignmentForm.tsx    # Form for submitting assignments
│   │   │   ├── AssignmentForm.css
│   │   │   ├── ReportDisplay.tsx     # Component to display reports
│   │   │   └── ReportDisplay.css
│   │   ├── App.tsx         # Main app component
│   │   ├── App.css
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts      # Vite configuration
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **npm**: Comes with Node.js

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server:**
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will start on `http://localhost:3000`

## 📖 How It Works

### Backend (`app.py`)

The Flask backend provides three main API endpoints:

1. **POST `/api/submit`**: Submits an assignment
   - Accepts: `student_name` and `assignment_text`
   - Returns: Analysis report with scores and feedback

2. **GET `/api/report/<assignment_id>`**: Retrieves a specific report

3. **GET `/api/assignments`**: Lists all submitted assignments

#### Key Functions:

- **`count_words(text)`**: Counts words by splitting on whitespace
- **`check_sections(text)`**: Detects Introduction, Body, and Conclusion sections using keyword matching
- **`find_long_sentences(text, max_words=20)`**: Identifies sentences exceeding the word limit
- **`analyze_assignment(text)`**: Combines all checks and generates a comprehensive report

#### Scoring System:

- Base score: 100 points
- Missing Introduction: -20 points
- Missing Body: -20 points
- Missing Conclusion: -20 points
- Long sentences: -2 points each (max -20 points)
- Low word count: -1 point per 10 words below 200 (max -20 points)

### Frontend Components

1. **`App.tsx`**: Root component that manages application state
   - Handles report data, loading states, and errors
   - Renders the form and report display

2. **`AssignmentForm.tsx`**: Submission form component
   - Collects student name and assignment text
   - Sends POST request to `/api/submit`
   - Handles form validation and error states

3. **`ReportDisplay.tsx`**: Report visualization component
   - Displays overall score with color-coded indicators
   - Shows word count, section checks, and long sentences
   - Renders detailed feedback

## 🎨 UI Features

- **Gradient Background**: Beautiful purple gradient
- **Glassmorphism**: Semi-transparent cards with backdrop blur
- **Smooth Animations**: Slide-in animations for reports
- **Color-Coded Scores**: Visual indicators for performance
- **Responsive Design**: Works on desktop, tablet, and mobile

## 📝 Example Usage

1. Open the app in your browser (`http://localhost:3000`)
2. Enter your name
3. Paste or type your assignment text
4. Click "Submit Assignment"
5. View your detailed report with:
   - Overall score (0-100)
   - Word count analysis
   - Section detection results
   - Long sentences list
   - Personalized feedback

## 🔧 Configuration

### Backend Port
Change the port in `backend/app.py`:
```python
app.run(debug=True, port=5000)  # Change 5000 to your preferred port
```

### Frontend Port
Change the port in `frontend/vite.config.ts`:
```typescript
server: {
  port: 3000,  // Change 3000 to your preferred port
}
```

### Word Limits
Adjust limits in `backend/app.py`:
- Minimum word count: Line 95 (`if word_count < 200`)
- Maximum sentence length: Line 60 (`max_words=20`)

## 🐛 Troubleshooting

### Backend Issues

- **Port already in use**: Change the port in `app.py` or stop the process using port 5000
- **Database errors**: Delete `assignments.db` and restart the server (it will recreate)
- **CORS errors**: Ensure `flask-cors` is installed

### Frontend Issues

- **Cannot connect to backend**: Check that the backend is running on port 5000
- **Build errors**: Delete `node_modules` and run `npm install` again
- **Type errors**: Ensure all TypeScript dependencies are installed

## 📚 Learning Resources

### For Beginners

- **Flask**: [Flask Documentation](https://flask.palletsprojects.com/)
- **React**: [React Documentation](https://react.dev/)
- **SQLite**: [SQLite Tutorial](https://www.sqlitetutorial.net/)
- **TypeScript**: [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests!

## 📄 License

This project is open source and available for educational purposes.

---

**Happy Coding! 🚀**

