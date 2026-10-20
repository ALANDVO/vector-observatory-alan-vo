import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'

const renderApp = () => {
  return render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  )
}

describe('App', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({
        status: 'healthy',
        service: 'Vector Observatory',
        version: '1.0.0',
      }),
    } as Response)
  })

  it('renders header with correct title', () => {
    renderApp()
    expect(screen.getByRole('heading', { level: 1, name: 'Vector Observatory' })).toBeInTheDocument()
  })

  it('renders subtitle', () => {
    renderApp()
    expect(screen.getByText('AI/ML Plugin Observatory for Knowledge Workers')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    vi.mocked(fetch).mockImplementation(() => new Promise(() => {}))
    renderApp()
    expect(screen.getByText('Loading dashboard...')).toBeInTheDocument()
  })

  it('displays health status when loaded', async () => {
    renderApp()
    await waitFor(() => {
      const statusBadges = screen.getAllByText('healthy')
      expect(statusBadges.length).toBeGreaterThanOrEqual(1)
      expect(statusBadges[0]).toBeInTheDocument()
    })
  })

  it('displays service name and version', async () => {
    renderApp()
    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 1, name: 'Vector Observatory' })).toBeInTheDocument()
      expect(screen.getByText('1.0.0')).toBeInTheDocument()
    })
  })
})