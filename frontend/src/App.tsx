/**
 * Main App Component
 * This is the root component that manages the overall application state
 * and renders the assignment submission form and report display
 */

import React, { useState } from 'react'
import AssignmentForm from './components/AssignmentForm'
import ReportDisplay from './components/ReportDisplay'
import './App.css'

// Type definition for the report data structure
interface Report {
  word_count: number
  sections: {
    has_introduction: boolean
    has_body: boolean
    has_conclusion: boolean
  }
  long_sentences_count: number
  long_sentences: string[]
  overall_score: number
  feedback: string
}

function App() {
  // State to store the report after submission
  const [report, setReport] = useState<Report | null>(null)
  // State to track loading status
  const [loading, setLoading] = useState(false)
  // State to store any error messages
  const [error, setError] = useState<string | null>(null)

  /**
   * Callback function called when an assignment is submitted
   * This receives the report data from the AssignmentForm component
   */
  const handleSubmission = (reportData: Report) => {
    setReport(reportData)
    setError(null)
  }

  /**
   * Callback function called when an error occurs during submission
   */
  const handleError = (errorMessage: string) => {
    setError(errorMessage)
    setReport(null)
  }

  /**
   * Callback function to update loading state
   */
  const handleLoading = (isLoading: boolean) => {
    setLoading(isLoading)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📝 Assignment Checker</h1>
        <p>Submit your assignment and get instant feedback!</p>
      </header>

      <main className="app-main">
        {/* Assignment submission form */}
        <AssignmentForm
          onSubmission={handleSubmission}
          onError={handleError}
          onLoading={handleLoading}
        />

        {/* Display error message if submission failed */}
        {error && (
          <div className="error-message">
            <p>❌ Error: {error}</p>
          </div>
        )}

        {/* Display loading indicator */}
        {loading && (
          <div className="loading">
            <p>⏳ Analyzing your assignment...</p>
          </div>
        )}

        {/* Display report if available */}
        {report && <ReportDisplay report={report} />}
      </main>
    </div>
  )
}

export default App

