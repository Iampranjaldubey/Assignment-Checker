/**
 * AssignmentForm Component
 * Handles assignment submission form
 * Navigates to assignments list on successful submission
 */

import { useState } from 'react'
import './AssignmentForm.css'

interface AssignmentFormProps {
  onSubmissionSuccess: () => void
}

function AssignmentForm({ onSubmissionSuccess }: AssignmentFormProps) {
  const [studentName, setStudentName] = useState('')
  const [assignmentText, setAssignmentText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /**
   * Handle form submission
   * Sends assignment data to backend API
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate inputs
    if (!studentName.trim()) {
      setError('Please enter your name')
      return
    }

    if (!assignmentText.trim()) {
      setError('Please enter your assignment text')
      return
    }

    setLoading(true)
    setError(null)

    try {
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

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to submit assignment')
      }

      // Success - reset form and navigate
      setStudentName('')
      setAssignmentText('')
      onSubmissionSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="assignment-form-container">
      <form onSubmit={handleSubmit} className="assignment-form">
        <h2>Submit Your Assignment</h2>

        {/* Error message */}
        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

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
            disabled={loading}
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
            disabled={loading}
          />
          <small className="form-hint">
            💡 Tip: Make sure to include Introduction, Body, and Conclusion sections
          </small>
        </div>

        {/* Submit Button */}
        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? '⏳ Submitting...' : '📤 Submit Assignment'}
        </button>
      </form>
    </div>
  )
}

export default AssignmentForm
