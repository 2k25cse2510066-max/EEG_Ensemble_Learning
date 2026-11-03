const sig = new Intl.NumberFormat('en-US', { maximumSignificantDigits: 5 })

// Compact, readable number: plain for ordinary magnitudes, scientific for extremes.
export function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '–'
  if (value === 0) return '0'
  const abs = Math.abs(value)
  if (abs >= 1e6 || abs < 1e-3) return value.toExponential(3).replace('e+', 'e')
  return sig.format(value)
}

export function formatPercent(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(value)) return '–'
  return `${Number(value).toFixed(digits)}%`
}
