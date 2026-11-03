export default function Stat({ label, value, suffix, caption, tone = 'cyan', index = 0 }) {
  return (
    <div className={`stat stat-${tone}`} style={{ '--i': index }}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">
        {value}
        {suffix && <span className="stat-suffix">{suffix}</span>}
      </div>
      {caption && <div className="stat-caption">{caption}</div>}
    </div>
  )
}
