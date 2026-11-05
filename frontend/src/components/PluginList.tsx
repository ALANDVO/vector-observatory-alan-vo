import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'

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

interface PaginatedResponse {
  items: Plugin[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

const API_BASE = '/api/v1'

export function PluginList() {
  const [plugins, setPlugins] = useState<Plugin[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [tagFilter, setTagFilter] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(12)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [allTags, setAllTags] = useState<string[]>([])

  const fetchPlugins = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: pageSize.toString(),
      })
      if (search) params.append('search', search)
      if (tagFilter) params.append('tag', tagFilter)

      const response = await fetch(`${API_BASE}/plugins?${params}`)
      if (!response.ok) throw new Error('Failed to fetch plugins')
      const data: PaginatedResponse = await response.json()
      setPlugins(data.items)
      setTotal(data.total)
      setTotalPages(data.total_pages)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, search, tagFilter])

  const fetchTags = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/plugins?page_size=100`)
      if (!response.ok) return
      const data: PaginatedResponse = await response.json()
      const tagsSet = new Set<string>()
      data.items.forEach(plugin => {
        if (plugin.tags) {
          plugin.tags.split(',').forEach(tag => tagsSet.add(tag.trim()))
        }
      })
      setAllTags(Array.from(tagsSet).sort())
    } catch {
      // Ignore tag fetch errors
    }
  }, [])

  useEffect(() => {
    fetchPlugins()
    fetchTags()
  }, [fetchPlugins, fetchTags])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setPage(1)
    fetchPlugins()
  }

  const handleTagClick = (tag: string) => {
    setTagFilter(tagFilter === tag ? '' : tag)
    setPage(1)
  }

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setPage(newPage)
    }
  }

  if (loading && plugins.length === 0) {
    return <div className="loading">Loading plugins...</div>
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">Failed to load plugins: {error}</div>
        <button onClick={fetchPlugins} className="retry-btn">Retry</button>
      </div>
    )
  }

  return (
    <div className="plugin-list">
      <div className="plugin-list-header">
        <h2>Plugin Catalog</h2>
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="search"
            placeholder="Search plugins..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn">Search</button>
          {search && (
            <button type="button" onClick={() => { setSearch(''); setPage(1); fetchPlugins(); }} className="clear-btn">Clear</button>
          )}
        </form>
      </div>

      {allTags.length > 0 && (
        <div className="tag-filters">
          <span className="tag-label">Filter by tag:</span>
          <div className="tag-cloud">
            {allTags.map(tag => (
              <button
                key={tag}
                onClick={() => handleTagClick(tag)}
                className={`tag-btn ${tagFilter === tag ? 'active' : ''}`}
              >
                {tag}
              </button>
            ))}
            {tagFilter && (
              <button onClick={() => { setTagFilter(''); setPage(1); fetchPlugins(); }} className="tag-btn clear-tag">
                Clear filter
              </button>
            )}
          </div>
        </div>
      )}

      <div className="plugins-grid">
        {plugins.map(plugin => (
          <Link key={plugin.id} to={`/plugins/${plugin.id}`} className="plugin-card">
            <div className="plugin-card-header">
              <h3 className="plugin-name">{plugin.name}</h3>
              {plugin.version && <span className="plugin-version">v{plugin.version}</span>}
            </div>
            <p className="plugin-description">{plugin.description || 'No description available'}</p>
            <div className="plugin-meta">
              {plugin.author && <span className="plugin-author">By {plugin.author}</span>}
              {plugin.tags && (
                <div className="plugin-tags">
                  {plugin.tags.split(',').slice(0, 3).map(tag => (
                    <span key={tag.trim()} className="tag">{tag.trim()}</span>
                  ))}
                  {plugin.tags.split(',').length > 3 && (
                    <span className="tag more">+{plugin.tags.split(',').length - 3} more</span>
                  )}
                </div>
              )}
            </div>
            <div className="plugin-skills-preview">
              <span className="skill-count">{plugin.skills.length} skill{plugin.skills.length !== 1 ? 's' : ''}</span>
            </div>
          </Link>
        ))}
      </div>

      {plugins.length === 0 && (
        <div className="no-results">No plugins found matching your criteria.</div>
      )}

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => handlePageChange(page - 1)}
            disabled={page === 1}
            className="page-btn"
          >
            Previous
          </button>
          <span className="page-info">
            Page {page} of {totalPages} ({total} total)
          </span>
          <button
            onClick={() => handlePageChange(page + 1)}
            disabled={page === totalPages}
            className="page-btn"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}
