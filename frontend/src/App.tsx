import { Routes, Route } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { HealthCheck } from './components/HealthCheck'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Vector Observatory</h1>
        <p className="subtitle">AI/ML Plugin Observatory for Knowledge Workers</p>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/health" element={<HealthCheck />} />
        </Routes>
      </main>
      <footer className="app-footer">
        <p>Vector Observatory \u2014 Alan Vo {String.fromCharCode(60)}alanvo@gmail.com{String.fromCharCode(62)}</p>
      </footer>
    </div>
  )
}

export default App
