import { projectData } from '../data/projectData.js'
import { FEATURES } from '../constants/features.js'
import { formatNumber } from './format.js'

const NUMBER_PATTERN = /^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/

// Returns a finite number, or null when the text is not a plain decimal.
export function parseNumber(text) {
  const trimmed = String(text ?? '').trim()
  if (!NUMBER_PATTERN.test(trimmed)) return null
  const value = Number(trimmed)
  return Number.isFinite(value) ? value : null
}

// Blocking validation: the backend needs 15 finite numbers.
export function validateField(text) {
  const trimmed = String(text ?? '').trim()
  if (trimmed === '') return 'Required'
  if (parseNumber(trimmed) === null) return 'Enter a plain number, e.g. 12.5 or 1.2e-3'
  return ''
}

export function validateAll(values) {
  const errors = {}
  for (const { key } of FEATURES) {
    const message = validateField(values[key])
    if (message) errors[key] = message
  }
  return errors
}

export function toPayload(values) {
  const payload = {}
  for (const { key } of FEATURES) payload[key] = parseNumber(values[key])
  return payload
}

// Per-field note when a value lies outside everything seen in the training data.
export function rangeNote(key, text) {
  const value = parseNumber(text)
  const stats = projectData.dataset.featureStats[key]
  if (value === null || !stats) return ''
  if (value < stats.min || value > stats.max) {
    return `Outside the training range (${formatNumber(stats.min)} to ${formatNumber(stats.max)})`
  }
  return ''
}

const near = (a, b, tolerance = 0.01) => Math.abs(a - b) <= tolerance * Math.max(1, Math.abs(a), Math.abs(b))

// Non-blocking advisories. Every rule here holds for all 500 training rows,
// so a violation means the inputs do not look like the data the model learned from.
export function consistencyAdvisories(values) {
  const v = {}
  for (const { key } of FEATURES) v[key] = parseNumber(values[key])
  const notes = []

  if (v.minimum !== null && v.maximum !== null) {
    if (v.minimum > v.maximum) {
      notes.push('Minimum is greater than maximum.')
    } else if (v.range !== null && !near(v.range, v.maximum - v.minimum)) {
      notes.push('Range differs from maximum − minimum. In the training data they are always equal.')
    }
  }
  if (v.mean !== null && v.minimum !== null && v.maximum !== null && v.minimum <= v.maximum) {
    if (v.mean < v.minimum || v.mean > v.maximum) notes.push('Mean lies outside the minimum–maximum interval.')
  }
  if (v.std !== null && v.std < 0) notes.push('Standard deviation is negative.')
  if (v.std !== null && v.variance !== null && v.std >= 0 && !near(v.variance, v.std * v.std)) {
    notes.push('Variance differs from std². In the training data they are always equal.')
  }

  const bands = ['delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'total_power']
  if (bands.some((k) => v[k] !== null && v[k] <= 0)) {
    notes.push('One or more power values are zero or negative. All training power values are positive.')
  } else if (bands.every((k) => v[k] !== null)) {
    const sum = bands.slice(0, 5).reduce((acc, k) => acc + v[k], 0)
    if (sum > v.total_power * 1.01) {
      notes.push('The five band powers add up to more than total power. In the training data they never do.')
    }
  }
  return notes
}
