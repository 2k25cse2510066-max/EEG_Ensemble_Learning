import { ENDPOINTS } from '../config.js'

export class ApiError extends Error {
  constructor(kind, message, extra = {}) {
    super(message)
    this.name = 'ApiError'
    this.kind = kind // 'network' | 'timeout' | 'validation' | 'server' | 'invalid-response'
    this.status = extra.status ?? null
    this.missing = extra.missing ?? []
  }
}

async function readJson(response) {
  try {
    return await response.json()
  } catch {
    return null
  }
}

// GET / returns {status, message} when the Flask app is up.
export async function checkHealth() {
  try {
    const response = await fetch(ENDPOINTS.health, { signal: AbortSignal.timeout(4000) })
    const data = await readJson(response)
    if (!response.ok || data?.status !== 'running') {
      throw new ApiError('server', 'The server responded, but not with the expected health message.', {
        status: response.status,
      })
    }
    return data
  } catch (error) {
    if (error instanceof ApiError) throw error
    if (error?.name === 'TimeoutError') throw new ApiError('timeout', 'The backend did not answer in time.')
    throw new ApiError('network', 'The backend could not be reached.')
  }
}

// POST /api/predict with the 15 original features as numbers.
export async function predict(payload) {
  const started = performance.now()
  let response
  try {
    response = await fetch(ENDPOINTS.predict, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(20000),
    })
  } catch (error) {
    if (error?.name === 'TimeoutError') throw new ApiError('timeout', 'The backend took too long to respond.')
    throw new ApiError('network', 'The backend could not be reached.')
  }

  const data = await readJson(response)

  if (!response.ok) {
    const message = typeof data?.error === 'string' ? data.error : `The backend returned HTTP ${response.status}.`
    throw new ApiError(response.status === 400 ? 'validation' : 'server', message, {
      status: response.status,
      missing: Array.isArray(data?.missing) ? data.missing : [],
    })
  }

  if (!data || data.success !== true || typeof data.prediction !== 'string') {
    throw new ApiError('invalid-response', 'The backend response did not contain a prediction.')
  }

  // Probabilities are only used if the backend actually returned them.
  const raw = data.class_probabilities
  const classProbabilities =
    raw && typeof raw === 'object' && Object.values(raw).every((p) => typeof p === 'number') && Object.keys(raw).length > 0
      ? raw
      : null

  return {
    prediction: data.prediction,
    probability: typeof data.probability === 'number' ? data.probability : null,
    classProbabilities,
    raw: data,
    elapsedMs: Math.round(performance.now() - started),
  }
}
