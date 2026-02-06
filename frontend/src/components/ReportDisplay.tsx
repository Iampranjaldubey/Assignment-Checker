/**
 * ReportDisplay Component
 * Reusable presentation component for displaying report data
 * Shows rule-based analysis and AI feedback
 */

import './ReportDisplay.css'
import type { Report } from '../types'

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

      {/* AI Feedback Card */}
      {report.ai_feedback && (
        <div className="report-section ai-feedback-section">
          <h3>🤖 AI Feedback</h3>
          <div className="ai-feedback-content">
            {/* Overall Evaluation */}
            <div className="ai-feedback-item">
              <h4 className="ai-feedback-title">Overall Evaluation</h4>
              <p className="ai-feedback-text">{report.ai_feedback.overall_evaluation}</p>
            </div>

            {/* Strengths */}
            {report.ai_feedback.strengths && report.ai_feedback.strengths.length > 0 && (
              <div className="ai-feedback-item">
                <h4 className="ai-feedback-title strengths-title">✅ Strengths</h4>
                <ul className="ai-feedback-list">
                  {report.ai_feedback.strengths.map((strength, index) => (
                    <li key={index} className="ai-feedback-list-item">
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Weaknesses */}
            {report.ai_feedback.weaknesses && report.ai_feedback.weaknesses.length > 0 && (
              <div className="ai-feedback-item">
                <h4 className="ai-feedback-title weaknesses-title">⚠️ Areas for Improvement</h4>
                <ul className="ai-feedback-list">
                  {report.ai_feedback.weaknesses.map((weakness, index) => (
                    <li key={index} className="ai-feedback-list-item">
                      {weakness}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Suggestions */}
            {report.ai_feedback.suggestions && report.ai_feedback.suggestions.length > 0 && (
              <div className="ai-feedback-item">
                <h4 className="ai-feedback-title suggestions-title">💡 Suggestions</h4>
                <ul className="ai-feedback-list">
                  {report.ai_feedback.suggestions.map((suggestion, index) => (
                    <li key={index} className="ai-feedback-list-item">
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ReportDisplay
