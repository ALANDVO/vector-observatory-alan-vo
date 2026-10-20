import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

interface HealthStatus {
  status: string
  service: string
  version: string
}

interface DbHealthStatus {
  status: string
  database: string
  error?: string
}

export function Dashboard() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [dbHealth, setDbHealth] = useState<DbHealthStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchHealth() {
      try {
        setLoading(true)
        const [healthRes, dbHealthRes] = await Promise.all([
          fetch('/api/v1/health'),
          fetch('/api/v1/health/db'),
        ])

        if (!healthRes.ok) throw new Error('Health check failed')
        if (!dbHealthRes.ok) throw new Error('DB health check failed')

        setHealth(await healthRes.json())
        setDbHealth(await dbHealthRes.json())
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchHealth()
  }, [])

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">Failed to load dashboard: {error}</div>
      </div>
    )
  }

  return (
    <div className="grid grid-2">
      <div className="card">
        <h2>Service Health</h2>
        {health && (
          <div>
            <p>
              <strong>Status:</strong>{' '}
              <span className={`status-badge ${health.status === 'healthy' ? 'status-healthy' : 'status-unhealthy'}`}>
                {health.status}
              </span>
            </p>
            <p><strong>Service:</strong> {health.service}</p>
            <p><strong>Version:</strong> {health.version}</p>
          </div>
        )}
      </div>

      <div className="card">
        <h2>Database Health</h2>
        {dbHealth && (
          <div>
            <p>
              <strong>Status:</strong>{' '}
              <span className={`status-badge ${dbHealth.status === 'healthy' ? 'status-healthy' : 'status-unhealthy'}`}>
                {dbHealth.status}
              </span>
            </p>
            <p><strong>Database:</strong> {dbHealth.database}</p>
            {dbHealth.error && <p className="error">Error: {dbHealth.error}</p>}
          </div>
        )}
      </div>

      <div className="card">
        <h2>Quick Actions</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <Link to="/health" className="btn btn-primary">Detailed Health</Link>
          <button className="btn btn-secondary" disabled>Browse Plugins (Coming Soon)</button>
          <button className="btn btn-secondary" disabled>Search Skills (Coming Soon)</button>
        </div>
      </div>

      <div className="card">
        <h2>About Vector Observatory</h2>
        <p>
          Vector Observatory is an AI/ML plugin observatory for knowledge workers using
          Claude Cowork. It catalogs plugins and skills from the
          <a href="https://github.com/anthropics/knowledge-work-plugins" target="_blank" rel="noopener noreferrer">
            knowledge-work-plugins
          </a>
          repository, providing search, quality analysis, and issue tracking.
        </p>
        <p>
          Current focus: building a substantive domain engine for plugin discovery,
          content quality evaluation, and GitHub issue triage workflows.
        </p>
      </div>
    </div>
  )
}