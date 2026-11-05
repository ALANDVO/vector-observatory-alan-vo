import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

interface Plugin {
  id: number
  name: string
  slug: string
  description: string | null
  version: string | null
  author: string | null
  repository_url: string | null
  homepage_url: string | null
  license: string | null
  tags: string | null
  is_active: boolean
  created_at: string
  updated_at: string
  skills: Skill[]
}

interface Skill {
  id: number
  plugin_id: number
  name: string
  slug: string
  description: string | null
  input_schema: string | null
  output_schema: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

const API_BASE = '/api/v1'

export function PluginDetail() {
  const { pluginId } = useParams<{ pluginId: string }>()
  const [plugin, setPlugin] = useState<Plugin | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!pluginId) return

    async function fetchPlugin() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(`${API_BASE}/plugins/${pluginId}`)
        if (!response.ok) {
          if (response.status === 404) throw new Error('Plugin not found')
          throw new Error('Failed to fetch plugin')
        }
        const data: Plugin = await response.json()
        setPlugin(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchPlugin()
  }, [pluginId])

  if (loading) {
    return <div className="loading">Loading plugin details...</div>
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">Failed to load plugin: {error}</div>
        <Link to="/plugins" className="back-link">← Back to catalog</Link>
      </div>
    )
  }

  if (!plugin) {
    return (
      <div className="card">
        <div className="error">Plugin not found</div>
        <Link to="/plugins" className="back-link">← Back to catalog</Link>
      </div>
    )
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  return (
    <div className="plugin-detail">
      <Link to="/plugins" className="back-link">← Back to catalog</Link>

      <div className="plugin-header">
        <div className="plugin-title-section">
          <h1 className="plugin-name">{plugin.name}</h1>
          {plugin.version && <span className="plugin-version">v{plugin.version}</span>}
          <span className={`plugin-status ${plugin.is_active ? 'active' : 'inactive'}`}>
            {plugin.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>

        <div className="plugin-links">
          {plugin.homepage_url && (
            <a href={plugin.homepage_url} target="_blank" rel="noopener noreferrer" className="external-link">
              Homepage
            </a>
          )}
          {plugin.repository_url && (
            <a href={plugin.repository_url} target="_blank" rel="noopener noreferrer" className="external-link">
              Repository
            </a>
          )}
        </div>
      </div>

      {plugin.description && (
        <div className="plugin-description">
          <h2>Description</h2>
          <p>{plugin.description}</p>
        </div>
      )}

      <div className="plugin-meta-grid">
        {plugin.author && (
          <div className="meta-item">
            <span className="meta-label">Author</span>
            <span className="meta-value">{plugin.author}</span>
          </div>
        )}
        {plugin.license && (
          <div className="meta-item">
            <span className="meta-label">License</span>
            <span className="meta-value">{plugin.license}</span>
          </div>
        )}
        <div className="meta-item">
          <span className="meta-label">Created</span>
          <span className="meta-value">{formatDate(plugin.created_at)}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Updated</span>
          <span className="meta-value">{formatDate(plugin.updated_at)}</span>
        </div>
      </div>

      {plugin.tags && (
        <div className="plugin-tags-section">
          <h2>Tags</h2>
          <div className="tags-cloud">
            {plugin.tags.split(',').map(tag => (
              <span key={tag.trim()} className="tag">{tag.trim()}</span>
            ))}
          </div>
        </div>
      )}

      <div className="plugin-skills">
        <h2>Skills ({plugin.skills.length})</h2>

        {plugin.skills.length === 0 ? (
          <p className="no-skills">This plugin provides no skills yet.</p>
        ) : (
          <div className="skills-grid">
            {plugin.skills.map(skill => (
              <div key={skill.id} className="skill-card">
                <div className="skill-header">
                  <h3 className="skill-name">{skill.name}</h3>
                  <span className={`skill-status ${skill.is_active ? 'active' : 'inactive'}`}>
                    {skill.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                {skill.description && (
                  <p className="skill-description">{skill.description}</p>
                )}
                <div className="skill-schemas">
                  {skill.input_schema && (
                    <details className="schema-detail">
                      <summary>Input Schema</summary>
                      <pre className="schema-pre">{skill.input_schema}</pre>
                    </details>
                  )}
                  {skill.output_schema && (
                    <details className="schema-detail">
                      <summary>Output Schema</summary>
                      <pre className="schema-pre">{skill.output_schema}</pre>
                    </details>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
