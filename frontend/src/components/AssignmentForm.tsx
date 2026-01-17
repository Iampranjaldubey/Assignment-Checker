/**
 * AssignmentForm Component
 * This component handles the assignment submission form
 * It collects student name and assignment text, then sends it to the backend API
 */

import React, { useState } from 'react'
import './AssignmentForm.css'

// Type definition for AI feedback structure
interface AIFeedback {
  overall_evaluation: string
  strengths: string[]
  weaknesses: string[]
  suggestions: string[]
}

// Type definition for the report structure
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
  ai_feedback?: AIFeedback | null  // Optional: AI feedback might not always be available
}

// Props interface for the component
interface AssignmentFormProps {
  onSubmission: (report: Report) => void
  onError: (error: string) => void
  onLoading: (loading: boolean) => void
}

function AssignmentForm({ onSubmission, onError, onLoading }: AssignmentFormProps) {
  // State for form inputs
  const [studentName, setStudentName] = useState('')
  const [assignmentText, setAssignmentText] = useState('')

  /**
   * Handle form submission
   * Sends the assignment data to the backend API
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault() // Prevent page refresh

    // Validate inputs
    if (!studentName.trim()) {
      onError('Please enter your name')
      return
    }

    if (!assignmentText.trim()) {
      onError('Please enter your assignment text')
      return
    }

    // Set loading state
    onLoading(true)
    onError('')

    try {
      // Send POST request to backend API
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_name: studentName,
          assignment_text: assignmentText,
        }),
      })

      // Parse the response
      const data = await response.json()

      if (!response.ok) {
        // Handle API errors
        throw new Error(data.error || 'Failed to submit assignment')
      }

      // Success! Prepare the report with AI feedback if available
      // The backend returns: { success: true, report: {...}, ai_feedback: {...} }
      const reportWithAI = {
        ...data.report,
        ai_feedback: data.ai_feedback || null  // Include AI feedback if present
      }

      // Pass the report (with AI feedback) to parent component
      onSubmission(reportWithAI)
      
      // Reset form
      setStudentName('')
      setAssignmentText('')
    } catch (err) {
      // Handle network or other errors
      onError(err instanceof Error ? err.message : 'An unexpected error occurred')
    } finally {
      // Always turn off loading state
      onLoading(false)
    }
  }

  return (
    <div className="assignment-form-container">
      <form onSubmit={handleSubmit} className="assignment-form">
        <h2>Submit Your Assignment</h2>

        {/* Student Name Input */}
        <div className="form-group">
          <label htmlFor="studentName">Your Name:</label>
          <input
            type="text"
            id="studentName"
            value={studentName}
            onChange={(e) => setStudentName(e.target.value)}
            placeholder="Enter your name"
            className="form-input"
          />
        </div>

        {/* Assignment Text Textarea */}
        <div className="form-group">
          <label htmlFor="assignmentText">Assignment Text:</label>
          <textarea
            id="assignmentText"
            value={assignmentText}
            onChange={(e) => setAssignmentText(e.target.value)}
            placeholder="Paste or type your assignment here..."
            className="form-textarea"
            rows={15}
          />
          <small className="form-hint">
            💡 Tip: Make sure to include Introduction, Body, and Conclusion sections
          </small>
        </div>

        {/* Submit Button */}
        <button type="submit" className="submit-button">
          📤 Submit Assignment
        </button>
      </form>
    </div>
  )
}

export default AssignmentForm

