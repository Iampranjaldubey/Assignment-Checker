/**
 * Main App Component
 * Defines all routes and navigation for the application
 */

import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import AssignmentForm from './components/AssignmentForm'
import AssignmentsList from './components/AssignmentsList'
import ReportPage from './components/ReportPage'
import './App.css'

function App() {
  const navigate = useNavigate()

  /**
   * Handle successful assignment submission
   * Navigate to assignments list after submission
   */
  const handleSubmissionSuccess = () => {
    navigate('/assignments')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📝 Assignment Checker</h1>
        <p>Submit your assignment and get instant feedback!</p>
        <nav className="app-nav">
          <Link to="/" className="nav-link">Submit</Link>
          <Link to="/assignments" className="nav-link">History</Link>
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          {/* Home route - Assignment submission */}
          <Route
            path="/"
            element={<AssignmentForm onSubmissionSuccess={handleSubmissionSuccess} />}
          />

          {/* Assignments list route */}
          <Route path="/assignments" element={<AssignmentsList />} />

          {/* Report detail route */}
          <Route path="/report/:id" element={<ReportPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
