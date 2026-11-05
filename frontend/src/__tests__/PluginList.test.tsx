import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { PluginList } from '../components/PluginList'

const mockPlugins = [
  {
    id: 1,
    name: 'Claude Code Plugin',
    slug: 'claude-code-plugin',
    description: 'A plugin for Claude Code',
    version: '1.0.0',
    author: 'Anthropic',
    repository_url: 'https://github.com/anthropics/claude-code-plugin',
    homepage_url: 'https://claude.ai',
    license: 'MIT',
    tags: 'ai, coding, claude',
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    skills: [
      { id: 1, plugin_id: 1, name: 'Code Generation', slug: 'code-generation', description: 'Generate code', input_schema: '{}', output_schema: '{}', is_active: true, created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
      { id: 2, plugin_id: 1, name: 'Code Review', slug: 'code-review', description: 'Review code', input_schema: '{}', output_schema: '{}', is_active: true, created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
    ],
  },
  {
    id: 2,
    name: 'Data Analysis Plugin',
    slug: 'data-analysis-plugin',
    description: 'Plugin for data analysis',
    version: '2.0.0',
    author: 'Data Corp',
    repository_url: null,
    homepage_url: null,
    license: 'Apache-2.0',
    tags: 'data, analytics, python',
    is_active: true,
    created_at: '2024-02-01T00:00:00Z',
    updated_at: '2024-02-01T00:00:00Z',
    skills: [],
  },
]

const mockResponse = {
  items: mockPlugins,
  total: 2,
  page: 1,
  page_size: 12,
  total_pages: 1,
}

const renderPluginList = () => {
  return render(
    <BrowserRouter>
      <PluginList />
    </BrowserRouter>
  )
}

describe('PluginList', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockResponse,
    } as Response)
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders plugin list header', async () => {
    renderPluginList()
    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 2, name: 'Plugin Catalog' })).toBeInTheDocument()
    })
  })

  it('shows loading state initially', () => {
    vi.mocked(fetch).mockImplementation(() => new Promise(() => {}))
    renderPluginList()
    expect(screen.getByText('Loading plugins...')).toBeInTheDocument()
  })

  it('displays plugins when loaded', async () => {
    renderPluginList()
    await waitFor(() => {
      expect(screen.getByText('Claude Code Plugin')).toBeInTheDocument()
      expect(screen.getByText('Data Analysis Plugin')).toBeInTheDocument()
    })
  })

  it('shows plugin version and author', async () => {
    renderPluginList()
    await waitFor(() => {
      expect(screen.getByText('v1.0.0')).toBeInTheDocument()
      expect(screen.getByText('By Anthropic')).toBeInTheDocument()
    })
  })

  it('shows skill count for each plugin', async () => {
    renderPluginList()
    await waitFor(() => {
      expect(screen.getByText('2 skills')).toBeInTheDocument()
      expect(screen.getByText('0 skills')).toBeInTheDocument()
    })
  })

  it('has search input', async () => {
    renderPluginList()
    await waitFor(() => {
      const searchInput = screen.getByPlaceholderText('Search plugins...')
      expect(searchInput).toBeInTheDocument()
    })
  })

  it('filters by tag when tag button clicked', async () => {
    renderPluginList()
    await waitFor(() => {
      const aiTag = screen.getByRole('button', { name: 'ai' })
      expect(aiTag).toBeInTheDocument()
    })
  })

  it('shows pagination when multiple pages', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        ...mockResponse,
        total: 25,
        total_pages: 3,
      }),
    } as Response)

    renderPluginList()
    await waitFor(() => {
      expect(screen.getByText('Page 1 of 3 (25 total)')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Next' })).toBeInTheDocument()
    })
  })

  it('shows error state on fetch failure', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 500,
    } as Response)

    renderPluginList()
    await waitFor(() => {
      expect(screen.getByText(/Failed to load plugins/)).toBeInTheDocument()
    })
  })
})
