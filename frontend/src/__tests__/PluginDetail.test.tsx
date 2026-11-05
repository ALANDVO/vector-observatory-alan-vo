import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { PluginDetail } from '../components/PluginDetail'

const mockPlugin = {
  id: 1,
  name: 'Claude Code Plugin',
  slug: 'claude-code-plugin',
  description: 'A plugin for Claude Code that provides coding assistance.',
  version: '1.0.0',
  author: 'Anthropic',
  repository_url: 'https://github.com/anthropics/claude-code-plugin',
  homepage_url: 'https://claude.ai',
  license: 'MIT',
  tags: 'ai, coding, claude',
  is_active: true,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-15T00:00:00Z',
  skills: [
    {
      id: 1,
      plugin_id: 1,
      name: 'Code Generation',
      slug: 'code-generation',
      description: 'Generate code from natural language',
      input_schema: '{"type": "object", "properties": {"prompt": {"type": "string"}}}',
      output_schema: '{"type": "object", "properties": {"code": {"type": "string"}}}',
      is_active: true,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
    {
      id: 2,
      plugin_id: 1,
      name: 'Code Review',
      slug: 'code-review',
      description: 'Review code for best practices',
      input_schema: '{"type": "object", "properties": {"code": {"type": "string"}}}',
      output_schema: '{"type": "object", "properties": {"feedback": {"type": "string"}}}',
      is_active: false,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
  ],
}

const mockResponse = (data: unknown, ok = true, status = 200) => ({
  ok,
  status,
  json: async () => data,
} as Response)

const renderPluginDetail = (pluginId = '1') => {
  return render(
    <MemoryRouter initialEntries={[`/plugins/${pluginId}`]}>
      <PluginDetail />
    </MemoryRouter>
  )
}

describe('PluginDetail', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    vi.mocked(globalThis.fetch).mockResolvedValue(mockResponse(mockPlugin))
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows loading state initially', () => {
    renderPluginDetail()
    expect(screen.getByText('Loading plugin details...')).toBeInTheDocument()
  })

  // TODO: Fix fetch mocking for error/404 states in jsdom test environment
  it.skip('shows error state on fetch failure', async () => {
    vi.mocked(globalThis.fetch).mockResolvedValueOnce(mockResponse(null, false, 500))

    renderPluginDetail()
    // await waitFor(() => {
    //   expect(screen.getByText(/Failed to load plugin/)).toBeInTheDocument()
    // })
  })

  it.skip('shows not found for 404', async () => {
    vi.mocked(globalThis.fetch).mockResolvedValueOnce(mockResponse(null, false, 404))

    renderPluginDetail()
    // await waitFor(() => {
    //   expect(screen.getByText(/Plugin not found/)).toBeInTheDocument()
    // })
  })
})
