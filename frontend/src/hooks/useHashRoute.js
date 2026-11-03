import { useCallback, useEffect, useState } from 'react'

const ROUTES = ['overview', 'analyze', 'performance', 'methodology']

function readRoute() {
  const id = window.location.hash.replace(/^#\/?/, '')
  return ROUTES.includes(id) ? id : 'overview'
}

// Minimal hash router: keeps refresh and the browser back button working.
export function useHashRoute() {
  const [route, setRoute] = useState(readRoute)

  useEffect(() => {
    const onChange = () => setRoute(readRoute())
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])

  const navigate = useCallback((id) => {
    window.location.hash = `/${id}`
  }, [])

  return [route, navigate]
}
