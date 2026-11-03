import { useCallback, useEffect, useRef, useState } from 'react'
import { checkHealth } from '../services/api.js'

const POLL_MS = 30000

// Tracks whether the Flask backend answers GET /.
export function useBackendStatus() {
  const [status, setStatus] = useState({ state: 'checking', message: 'Checking backend…', checkedAt: null })
  const requestId = useRef(0)

  const check = useCallback(async () => {
    const id = ++requestId.current
    setStatus((prev) => ({ ...prev, state: 'checking', message: 'Checking backend…' }))
    try {
      const data = await checkHealth()
      if (id === requestId.current) {
        setStatus({ state: 'online', message: data.message || 'Backend is running', checkedAt: new Date() })
      }
    } catch (error) {
      if (id === requestId.current) {
        setStatus({ state: 'offline', message: error.message, checkedAt: new Date() })
      }
    }
  }, [])

  useEffect(() => {
    const first = setTimeout(check, 0)
    const timer = setInterval(check, POLL_MS)
    return () => {
      clearTimeout(first)
      clearInterval(timer)
      requestId.current += 1
    }
  }, [check])

  return { ...status, recheck: check }
}
