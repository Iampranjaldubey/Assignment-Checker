/**
 * ReportPage Component
 * Fetches and displays a detailed report for a specific assignment
 */

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReportDisplay from './ReportDisplay'
import type { Report } from '../types'
import './ReportPage.css'

function ReportPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  /**
   * Fetch report from backend API
   */
  useEffect(() => {
    const fetchReport = async () => {
      if (!id) {
        setError('Invalid assignment ID')
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        const response = await fetch(`/api/report/${id}`)

        if (!response.ok) {
          const data = await response.json()
          throw new Error(data.error || 'Failed to fetch report')
        }

        const data = await response.json()

        // Transform API response to Report type
        const reportData: Report = {
          word_count: data.word_count,
          sections: {
            has_introduction: data.has_introduction,
            has_body: data.has_body,
            has_conclusion: data.has_conclusion,
          },
          long_sentences_count: data.long_sentences_count,
          long_sentences: data.long_sentences || [],
          overall_score: data.overall_score,
          feedback: data.feedback,
          ai_feedback: data.ai_feedback || null,
        }

        setReport(reportData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unexpected error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchReport()
  }, [id])

  if (loading) {
    return (
      <div className="report-page">
        <div className="loading-message">
          <p>⏳ Loading report...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="report-page">
        <div className="error-message">
          <p>❌ Error: {error}</p>
          <button onClick={() => navigate('/assignments')} className="back-button">
            ← Back to History
          </button>
        </div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="report-page">
        <div className="error-message">
          <p>Report not found</p>
          <button onClick={() => navigate('/assignments')} className="back-button">
            ← Back to History
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="report-page">
      <button onClick={() => navigate('/assignments')} className="back-button">
        ← Back to History
      </button>
      <ReportDisplay report={report} />
    </div>
  )
}

export default ReportPage
