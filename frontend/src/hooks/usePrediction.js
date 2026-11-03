import { useCallback, useRef, useState } from 'react'
import { ApiError, predict } from '../services/api.js'

// idle -> loading -> success | error. Stale responses are ignored.
export function usePrediction() {
  const [state, setState] = useState({ status: 'idle', result: null, error: null })
  const requestId = useRef(0)

  const run = useCallback(async (payload) => {
    const id = ++requestId.current
    setState({ status: 'loading', result: null, error: null })
    try {
      const result = await predict(payload)
      if (id === requestId.current) setState({ status: 'success', result, error: null })
    } catch (error) {
      if (id !== requestId.current) return
      const apiError = error instanceof ApiError ? error : new ApiError('server', 'Something unexpected went wrong.')
      setState({ status: 'error', result: null, error: apiError })
    }
  }, [])

  const reset = useCallback(() => {
    requestId.current += 1
    setState({ status: 'idle', result: null, error: null })
  }, [])

  return { ...state, run, reset }
}
