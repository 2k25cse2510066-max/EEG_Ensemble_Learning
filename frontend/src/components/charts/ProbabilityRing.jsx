const R = 46
const C = 2 * Math.PI * R

// Animated ring for the top-class probability (percent, 0 to 100).
export default function ProbabilityRing({ value, color }) {
  const clamped = Math.max(0, Math.min(100, value))
  return (
    <div className="ring" style={{ '--ring-color': color }}>
      <svg viewBox="0 0 110 110" aria-hidden="true" focusable="false">
        <circle className="ring-track" cx="55" cy="55" r={R} />
        <circle
          className="ring-value-arc"
          cx="55"
          cy="55"
          r={R}
          strokeDasharray={C}
          style={{ '--ring-full': C, '--ring-offset': C * (1 - clamped / 100) }}
        />
      </svg>
      <div className="ring-text">
        <span className="ring-value">{clamped.toFixed(2)}%</span>
        <span className="ring-caption">top class</span>
      </div>
    </div>
  )
}
