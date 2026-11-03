// Mean accuracy with a ±1 standard deviation whisker. The axis starts at 60%
// so that the whiskers are legible; this is stated in the axis caption.
const MIN = 60
const MAX = 100
const pos = (v) => `${((Math.min(MAX, Math.max(MIN, v)) - MIN) / (MAX - MIN)) * 100}%`
const TICKS = [60, 70, 80, 90, 100]

export default function AccuracyBars({ items, highlight, caption }) {
  return (
    <div className="acc">
      <ul className="acc-list" aria-label={caption}>
        {items.map((item, index) => (
          <li className="acc-row" key={item.model} data-highlight={item.model === highlight} style={{ '--i': index }}>
            <span className="acc-name">{item.model}</span>
            <span className="acc-track" aria-hidden="true">
              <span className="acc-fill" style={{ width: pos(item.mean) }} />
              <span
                className="acc-whisker"
                style={{ left: pos(item.mean - item.std), width: `calc(${pos(item.mean + item.std)} - ${pos(item.mean - item.std)})` }}
              />
            </span>
            <span className="acc-value">
              {item.mean.toFixed(1)}
              <span className="acc-std"> ±{item.std.toFixed(1)}</span>
            </span>
          </li>
        ))}
      </ul>
      <div className="acc-axis" aria-hidden="true">
        <span />
        <span className="acc-ticks">
          {TICKS.map((t) => (
            <span key={t} style={{ left: pos(t) }}>
              {t}
            </span>
          ))}
        </span>
        <span />
      </div>
      <p className="chart-note">Accuracy in percent. The axis starts at 60%. Whiskers show ±1 standard deviation across folds.</p>
    </div>
  )
}
