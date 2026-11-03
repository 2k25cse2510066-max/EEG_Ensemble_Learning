import { BANDS } from '../../constants/features.js'
import { classMeta } from '../../constants/classes.js'
import { formatPercent } from '../../utils/format.js'

const CX = 190
const CY = 160
const R = 112
const angle = (i) => -Math.PI / 2 + (i * 2 * Math.PI) / BANDS.length
const point = (i, radius) => [CX + radius * Math.cos(angle(i)), CY + radius * Math.sin(angle(i))]

// Radar of the same band-share data as the bar view. Overlaid polygons make the class profiles comparable.
export default function BandRadar({ signature, classOrder, active, onActive }) {
  const max = Math.max(...classOrder.flatMap((c) => BANDS.map((b) => signature[c][b.key])))
  const scale = Math.ceil(max * 10) / 10 // round the outer ring up to a tidy value
  const rings = [0.25, 0.5, 0.75, 1]
  const ordered = active ? [...classOrder.filter((c) => c !== active), active] : classOrder

  return (
    <svg className="radar" viewBox="0 0 380 330" role="img" aria-label="Radar chart of median band power share by class. The same data is available in the bar view.">
      {rings.map((ring) => (
        <polygon
          key={ring}
          className="radar-ring"
          points={BANDS.map((_, i) => point(i, R * ring).join(',')).join(' ')}
        />
      ))}
      {BANDS.map((b, i) => {
        const [x, y] = point(i, R)
        const [lx, ly] = point(i, R + 22)
        return (
          <g key={b.key}>
            <line className="radar-axis" x1={CX} y1={CY} x2={x} y2={y} />
            <text className="radar-label" x={lx} y={ly} textAnchor="middle" dominantBaseline="middle">
              {b.symbol} {b.label}
            </text>
          </g>
        )
      })}
      {rings.map((ring) => (
        <text key={ring} className="radar-tick" x={CX + 4} y={CY - R * ring - 2}>
          {Math.round(scale * ring * 100)}%
        </text>
      ))}

      {ordered.map((c) => {
        const meta = classMeta(c)
        const pts = BANDS.map((b, i) => point(i, R * (signature[c][b.key] / scale)))
        const isActive = active === c
        const dim = active && !isActive
        return (
          <g
            key={c}
            className="radar-class"
            data-active={isActive}
            data-dim={Boolean(dim)}
            onPointerEnter={() => onActive(c, true)}
            onPointerLeave={() => onActive(null, true)}
          >
            <polygon
              className="radar-poly"
              points={pts.map((p) => p.join(',')).join(' ')}
              fill={meta.color}
              stroke={meta.color}
            />
            {pts.map(([x, y], i) => (
              <circle key={BANDS[i].key} className="radar-dot" cx={x} cy={y} r={isActive ? 4 : 2.6} fill={meta.color}>
                <title>
                  {meta.label}, {BANDS[i].label}: {formatPercent(signature[c][BANDS[i].key] * 100, 1)} of total power
                </title>
              </circle>
            ))}
          </g>
        )
      })}
    </svg>
  )
}
