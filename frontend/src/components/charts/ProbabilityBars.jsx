import { classMeta } from '../../constants/classes.js'

// Per-class probabilities exactly as returned by the backend (already in percent).
export default function ProbabilityBars({ probabilities, predicted }) {
  const rows = Object.entries(probabilities).sort((a, b) => b[1] - a[1])

  return (
    <ul className="prob-list" aria-label="Class probabilities returned by the model">
      {rows.map(([name, value], index) => {
        const meta = classMeta(name)
        const isTop = name === predicted
        return (
          <li key={name} className="prob-row" data-top={isTop} style={{ '--i': index }}>
            <span className="prob-name">
              <span className="class-swatch" style={{ background: meta.color }} aria-hidden="true" />
              {meta.label}
              {isTop && <span className="sr-only"> (predicted class)</span>}
            </span>
            <span className="prob-track" aria-hidden="true">
              <span
                className="prob-fill"
                style={{ width: `${Math.max(0, Math.min(100, value))}%`, background: meta.color }}
              />
            </span>
            <span className="prob-value">{value.toFixed(2)}%</span>
          </li>
        )
      })}
    </ul>
  )
}
