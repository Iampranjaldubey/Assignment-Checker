/**
 * AssignmentsList Component
 * Displays a table of all submitted assignments
 * Clicking a row navigates to the detailed report
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import type { Assignment } from '../types'
import './AssignmentsList.css'

function AssignmentsList() {
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  /**
   * Fetch assignments from backend API
   */
  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/assignments')

        if (!response.ok) {
          throw new Error('Failed to fetch assignments')
        }

        const data = await response.json()
        setAssignments(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unexpected error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchAssignments()
  }, [])

  /**
   * Handle row click - navigate to report detail page
   */
  const handleRowClick = (assignmentId: number) => {
    navigate(`/report/${assignmentId}`)
  }

  /**
   * Format date string for display
   */
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  if (loading) {
    return (
      <div className="assignments-container">
        <h2>📋 Assignment History</h2>
        <div className="loading-message">
          <p>⏳ Loading assignments...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="assignments-container">
        <h2>📋 Assignment History</h2>
        <div className="error-message">
          <p>❌ Error: {error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="assignments-container">
      <h2>📋 Assignment History</h2>

      {assignments.length === 0 ? (
        <div className="empty-state">
          <p>No assignments submitted yet.</p>
          <p>Submit your first assignment to see it here!</p>
        </div>
      ) : (
        <div className="table-wrapper">
          <table className="assignments-table">
            <thead>
              <tr>
                <th>Student Name</th>
                <th>Word Count</th>
                <th>Score</th>
                <th>Submitted</th>
              </tr>
            </thead>
            <tbody>
              {assignments.map((assignment) => (
                <tr
                  key={assignment.id}
                  onClick={() => handleRowClick(assignment.id)}
                  className="table-row"
                >
                  <td>{assignment.student_name}</td>
                  <td>{assignment.word_count}</td>
                  <td>
                    {assignment.overall_score !== null ? (
                      <span className={`score-badge score-${getScoreClass(assignment.overall_score)}`}>
                        {assignment.overall_score}/100
                      </span>
                    ) : (
                      <span className="score-badge score-none">N/A</span>
                    )}
                  </td>
                  <td>{formatDate(assignment.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

/**
 * Get CSS class for score badge based on score value
 */
function getScoreClass(score: number): string {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  return 'poor'
}

export default AssignmentsList
