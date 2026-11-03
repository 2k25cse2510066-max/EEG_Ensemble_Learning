import { BANDS } from '../../constants/features.js'
import { classMeta } from '../../constants/classes.js'
import { formatPercent } from '../../utils/format.js'
import WaveCanvas from './WaveCanvas.jsx'
import ClassSelect from './ClassSelect.jsx'

// Rows of animated waves, one per band, with the real median share of total power at the right.
export default function BandPanel({ classKey, onClassChange, signature, relative }) {
  const shares = signature[classKey]
  const top = BANDS.reduce((best, b) => (shares[b.key] > shares[best.key] ? b : best), BANDS[0])

  return (
    <section className="panel band-panel" aria-labelledby="band-panel-title">
      <header className="panel-head">
        <div>
          <h2 id="band-panel-title">Band power</h2>
          <p className="panel-desc">Median share of total power</p>
        </div>
        <div className="panel-actions">
          <ClassSelect value={classKey} onChange={onClassChange} />
          <span className="pill" title={`${classMeta(classKey).label}: ${top.label} holds the largest share`}>
            Peak: {top.label} {formatPercent(shares[top.key] * 100, 1)}
          </span>
        </div>
      </header>

      <ul className="wave-rows" aria-label={`Band power share for ${classMeta(classKey).label}`}>
        {[...BANDS].reverse().map((b) => (
          <li key={b.key} className="wave-row">
            <span className="wave-name">
              <span className="wave-symbol" aria-hidden="true">{b.symbol}</span>
              {b.label}
            </span>
            <WaveCanvas band={b.key} amp={relative[classKey][b.key]} height={34} glow={9} />
            <span className="wave-value">{formatPercent(shares[b.key] * 100, shares[b.key] < 0.1 ? 2 : 1)}</span>
          </li>
        ))}
      </ul>
      <p className="panel-foot">
        Values are measured. Wave height compares classes within a band; wave shape is illustrative.
      </p>
    </section>
  )
}
