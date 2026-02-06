/**
 * Shared TypeScript type definitions for the Assignment Checker application
 */

export interface AIFeedback {
  overall_evaluation: string
  strengths: string[]
  weaknesses: string[]
  suggestions: string[]
}

export interface Report {
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
  ai_feedback?: AIFeedback | null
}

export interface Assignment {
  id: number
  student_name: string
  word_count: number
  created_at: string
  overall_score: number | null
}

export interface ReportResponse {
  id: number
  assignment_id: number
  word_count: number
  has_introduction: boolean
  has_body: boolean
  has_conclusion: boolean
  long_sentences_count: number
  long_sentences: string[]
  overall_score: number
  feedback: string
  ai_feedback?: AIFeedback | null
  created_at: string
}
