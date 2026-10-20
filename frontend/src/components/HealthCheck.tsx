import { useState, useEffect } from 'react'

interface HealthDetail {
  status: string
  service: string
  version: string
  timestamp: string
  uptime_seconds: number
  dependencies: {
    database: { status: string; latency_ms: number }
    keycloak: { status: string; latency_ms: number }
  }
}

export function HealthCheck() {
  const [health, setHealth] = useState<HealthDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchHealth() {
      try {
        setLoading(true)
        const res = await fetch('/api/v1/health/detail')
        if (!res.ok) throw new Error('Detailed health check failed')
        setHealth(await res.json())
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
    return <div className="loading">Loading detailed health...</div>
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">Failed to load health details: {error}</div>
      </div>
    )
  }

  if (!health) {
    return <div className="card">No health data available</div>
  }

  return (
    <div className="card">
      <h2>Detailed Health Check</h2>
      <div className="grid grid-2" style={{ marginBottom: '1.5rem' }}>
        <div>
          <p><strong>Service:</strong> {health.service}</p>
          <p><strong>Version:</strong> {health.version}</p>
          <p><strong>Uptime:</strong> {Math.floor(health.uptime_seconds / 60)} minutes</p>
        </div>
        <div>
          <p>
            <strong>Overall Status:</strong>{' '}
            <span className={`status-badge ${health.status === 'healthy' ? 'status-healthy' : 'status-unhealthy'}`}>
              {health.status}
            </span>
          </p>
          <p><strong>Timestamp:</strong> {health.timestamp}</p>
        </div>
      </div>

      <h3>Dependencies</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ textAlign: 'left', borderBottom: '2px solid #e8eef5' }}>
            <th style={{ padding: '0.75rem' }}>Dependency</th>
            <th style={{ padding: '0.75rem' }}>Status</th>
            <th style={{ padding: '0.75rem' }}>Latency</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(health.dependencies).map(([name, dep]) => (
            <tr key={name} style={{ borderBottom: '1px solid #e8eef5' }}>
              <td style={{ padding: '0.75rem' }}>{name}</td>
              <td style={{ padding: '0.75rem' }}>
                <span className={`status-badge ${dep.status === 'healthy' ? 'status-healthy' : 'status-unhealthy'}`}>
                  {dep.status}
                </span>
              </td>
              <td style={{ padding: '0.75rem' }}>{dep.latency_ms} ms</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}