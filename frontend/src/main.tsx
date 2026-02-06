/**
 * Main entry point for the React application
 * This file renders the App component into the DOM with React Router
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

// Get the root element from index.html
const rootElement = document.getElementById('root')

if (rootElement) {
  // Create a React root and render the App component wrapped in BrowserRouter
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </React.StrictMode>
  )
}
