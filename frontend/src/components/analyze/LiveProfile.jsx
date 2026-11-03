import { useMemo, useState } from 'react'
import { BANDS, FEATURES } from '../../constants/features.js'
import { CLASS_ORDER, classMeta } from '../../constants/classes.js'
import { projectData } from '../../data/projectData.js'
import { parseNumber } from '../../utils/validation.js'

const EPS = 1e-10

// Live preview of band power ÷ total power (the definition behind the *_ratio features),
// updated as the user types. Optional class medians are shown as reference ticks.
// This is a browser-side preview, not a model prediction.
export default function LiveProfile({ values }) {
  const [compare, setCompare] = useState(null)

  const shares = useMemo(() => {
    const total = parseNumber(values.total_power)
    const powers = BANDS.map((b) => parseNumber(values[`${b.key}_power`]))
    if (total === null || total <= 0 || powers.some((p) => p === null || p < 0)) return null
    return powers.map((p) => p / (total + EPS))
  }, [values])

  const reference = compare ? projectData.dataset.bandSignature[compare] : null
  const scale = Math.max(0.6, ...(shares ?? []), ...(reference ? Object.values(reference) : []))
  const bandFeatures = FEATURES.filter((f) => f.group === 'power').length

  return (
    <section className="live" aria-labelledby="live-title">
      <div className="live-head">
        <div>
          <h3 id="live-title">Live band profile</h3>
          <p>
            Each band's share of total power for the values you typed. A preview computed in your browser, not a
            prediction.
          </p>
        </div>
        <div className="chips" role="group" aria-label="Compare with a class median">
          <button type="button" className="chip chip-sm" aria-pressed={compare === null} onClick={() => setCompare(null)}>
            No comparison
          </button>
          {CLASS_ORDER.map((c) => (
            <button
              key={c}
              type="button"
              className="chip chip-sm"
              aria-pressed={compare === c}
              onClick={() => setCompare(compare === c ? null : c)}
            >
              <span className="class-swatch" style={{ background: classMeta(c).color }} aria-hidden="true" />
              {classMeta(c).short}
            </button>
          ))}
        </div>
      </div>

      {shares ? (
        <ul className="live-bars" aria-label="Band share of total power">
          {BANDS.map((b, i) => (
            <li key={b.key}>
              <span className="live-name">
                <span className="live-symbol">{b.symbol}</span> {b.label}
              </span>
              <span className="live-track">
                <span className="live-fill" style={{ width: `${Math.min(100, (shares[i] / scale) * 100)}%` }} />
                {reference && (
                  <span
                    className="live-ref"
                    style={{ left: `${(reference[b.key] / scale) * 100}%`, background: classMeta(compare).color }}
                    title={`${classMeta(compare).label} median: ${(reference[b.key] * 100).toFixed(1)}%`}
                  />
                )}
              </span>
              <span className="live-value">{(shares[i] * 100).toFixed(1)}%</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="live-empty">
          Enter the {bandFeatures - 1} band powers and total power (positive numbers) to see their relative shares.
        </p>
      )}
      {shares && reference && (
        <p className="live-foot">
          Marks show the {classMeta(compare).label} median from the training data.
        </p>
      )}
    </section>
  )
}
