/**
 * ReportDisplay Component
 * This component displays the analysis report for a submitted assignment
 * It shows word count, section checks, long sentences, overall score, and feedback
 */

import React from 'react'
import './ReportDisplay.css'

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
}

// Props interface for the component
interface ReportDisplayProps {
  report: Report
}

function ReportDisplay({ report }: ReportDisplayProps) {
  /**
   * Get a color class based on the score
   * Green for good scores, yellow for medium, red for low
   */
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'score-excellent'
    if (score >= 60) return 'score-good'
    if (score >= 40) return 'score-fair'
    return 'score-poor'
  }

  return (
    <div className="report-display">
      <h2>📊 Assignment Report</h2>

      {/* Overall Score */}
      <div className="score-section">
        <div className={`score-circle ${getScoreColor(report.overall_score)}`}>
          <div className="score-value">{report.overall_score}</div>
          <div className="score-label">/ 100</div>
        </div>
        <p className="score-description">
          {report.overall_score >= 80
            ? 'Excellent work! 🎉'
            : report.overall_score >= 60
            ? 'Good job! Keep improving! 👍'
            : report.overall_score >= 40
            ? 'Not bad, but there\'s room for improvement 📝'
            : 'Needs significant improvement. Review the feedback below. 🔍'}
        </p>
      </div>

      {/* Word Count */}
      <div className="report-section">
        <h3>📝 Word Count</h3>
        <p className="stat-value">{report.word_count} words</p>
        <p className="stat-note">
          {report.word_count >= 200
            ? '✅ Meets the recommended minimum of 200 words'
            : `⚠️ Below the recommended minimum of 200 words (${200 - report.word_count} words short)`}
        </p>
      </div>

      {/* Section Checks */}
      <div className="report-section">
        <h3>📑 Required Sections</h3>
        <div className="sections-list">
          <div className="section-item">
            <span className={report.sections.has_introduction ? 'check-pass' : 'check-fail'}>
              {report.sections.has_introduction ? '✅' : '❌'}
            </span>
            <span>Introduction</span>
          </div>
          <div className="section-item">
            <span className={report.sections.has_body ? 'check-pass' : 'check-fail'}>
              {report.sections.has_body ? '✅' : '❌'}
            </span>
            <span>Body</span>
          </div>
          <div className="section-item">
            <span className={report.sections.has_conclusion ? 'check-pass' : 'check-fail'}>
              {report.sections.has_conclusion ? '✅' : '❌'}
            </span>
            <span>Conclusion</span>
          </div>
        </div>
      </div>

      {/* Long Sentences */}
      <div className="report-section">
        <h3>📏 Sentence Length</h3>
        <p className="stat-value">
          {report.long_sentences_count === 0
            ? '✅ All sentences are within the recommended length (≤20 words)'
            : `⚠️ Found ${report.long_sentences_count} sentence(s) with more than 20 words`}
        </p>
        {report.long_sentences.length > 0 && (
          <div className="long-sentences">
            <p className="long-sentences-title">Long sentences to review:</p>
            <ul>
              {report.long_sentences.map((sentence, index) => (
                <li key={index} className="long-sentence-item">
                  "{sentence.substring(0, 100)}
                  {sentence.length > 100 ? '...' : ''}"
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Detailed Feedback */}
      <div className="report-section feedback-section">
        <h3>💬 Detailed Feedback</h3>
        <div className="feedback-content">
          {report.feedback.split('\n').map((line, index) => (
            <p key={index} className="feedback-line">
              {line}
            </p>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ReportDisplay

