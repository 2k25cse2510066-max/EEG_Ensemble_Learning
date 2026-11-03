// Purely decorative ambient line behind the page title. It is NOT EEG data.
const TILE = 600
const points = []
for (let x = 0; x <= TILE * 2; x += 6) {
  const y =
    40 +
    13 * Math.sin((2 * Math.PI * x) / 300) +
    8 * Math.sin((2 * Math.PI * x) / 120 + 1) +
    4 * Math.sin((2 * Math.PI * x) / 60)
  points.push(`${x === 0 ? 'M' : 'L'}${x} ${y.toFixed(1)}`)
}
const PATH = points.join(' ')

export default function HeroWave() {
  return (
    <div className="hero-wave" aria-hidden="true">
      <svg viewBox={`0 0 ${TILE} 80`} preserveAspectRatio="none" focusable="false">
        <defs>
          <linearGradient id="wave-grad" x1="0" x2="1">
            <stop offset="0" stopColor="#3ccbe0" />
            <stop offset="1" stopColor="#9d8cff" />
          </linearGradient>
        </defs>
        <g className="wave-a">
          <path d={PATH} fill="none" stroke="url(#wave-grad)" strokeWidth="1.6" vectorEffect="non-scaling-stroke" />
        </g>
        <g className="wave-b">
          <path d={PATH} fill="none" stroke="url(#wave-grad)" strokeWidth="1" vectorEffect="non-scaling-stroke" />
        </g>
      </svg>
    </div>
  )
}
