import { useCallback, useEffect, useRef } from 'react'
import ResearchNotice from './components/layout/ResearchNotice.jsx'
import TopBar from './components/layout/TopBar.jsx'
import { NAV_ITEMS } from './constants/navigation.js'
import { useBackendStatus } from './hooks/useBackendStatus.js'
import { useHashRoute } from './hooks/useHashRoute.js'
import { useSpotlight } from './hooks/useSpotlight.js'
import AnalyzePage from './pages/AnalyzePage.jsx'
import MethodologyPage from './pages/MethodologyPage.jsx'
import OverviewPage from './pages/OverviewPage.jsx'
import PerformancePage from './pages/PerformancePage.jsx'

export default function App() {
  const [route, navigate] = useHashRoute()
  const backend = useBackendStatus()
  useSpotlight()
  const pageRef = useRef(null)
  const firstRender = useRef(true)

  const go = useCallback(
    (id) => {
      navigate(id)
    },
    [navigate],
  )

  // After navigating, reset scroll and move focus to the page heading for screen-reader and keyboard users.
  useEffect(() => {
    const title = NAV_ITEMS.find((item) => item.id === route)?.label
    document.title = `${title} | EEG State Classifier`
    if (firstRender.current) {
      firstRender.current = false
      return
    }
    window.scrollTo(0, 0)
    pageRef.current?.querySelector('#page-title')?.focus({ preventScroll: true })
  }, [route])

  return (
    <div className="app-shell">
      <div className="ambient" aria-hidden="true" />
      <a className="skip-link" href="#main">
        Skip to content
      </a>

      <TopBar route={route} onNavigate={go} backend={backend} />

      <main className="main" id="main">
        <div className="page" ref={pageRef} key={route}>
          {route === 'overview' && <OverviewPage onNavigate={go} />}
          {route === 'analyze' && <AnalyzePage backend={backend} />}
          {route === 'performance' && <PerformancePage />}
          {route === 'methodology' && <MethodologyPage />}
        </div>
        <footer className="site-foot">
          <ResearchNotice compact />
        </footer>
      </main>
    </div>
  )
}
