// Simple horizontal ranking. `tone` is 'cyan' or 'violet'.
export default function RankedBars({ items, label }) {
  const max = Math.max(...items.map((i) => i.value))
  return (
    <ul className="rank-list" aria-label={label}>
      {items.map((item, index) => (
        <li className="rank-row" key={item.name} style={{ '--i': index }}>
          <span className="rank-name mono">{item.name}</span>
          <span className="rank-track" aria-hidden="true">
            <span className={`rank-fill rank-${item.tone}`} style={{ width: `${(item.value / max) * 100}%` }} />
          </span>
          <span className="rank-value">{item.display}</span>
        </li>
      ))}
    </ul>
  )
}
