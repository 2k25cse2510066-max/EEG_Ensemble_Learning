import { BANDS } from '../../constants/features.js'
import { classMeta } from '../../constants/classes.js'
import { formatPercent } from '../../utils/format.js'

// Small multiples: one row per class, one bar per EEG band.
// Values are the median share of total power per band across that class's training rows.
export default function BandSignature({ signature, classOrder, active = null, onActive = () => {} }) {
  const max = Math.max(...classOrder.flatMap((c) => BANDS.map((b) => signature[c][b.key])))

  return (
    <div className="signature">
      <table className="sr-only">
        <caption>Median share of total power by band and class</caption>
        <thead>
          <tr>
            <th scope="col">Class</th>
            {BANDS.map((b) => (
              <th scope="col" key={b.key}>
                {b.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {classOrder.map((c) => (
            <tr key={c}>
              <th scope="row">{classMeta(c).label}</th>
              {BANDS.map((b) => (
                <td key={b.key}>{formatPercent(signature[c][b.key] * 100, 1)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="sig-grid" aria-hidden="true">
        <div />
        {BANDS.map((b) => (
          <div className="sig-band" key={b.key}>
            <span className="sig-symbol">{b.symbol}</span>
            {b.label}
          </div>
        ))}
        {classOrder.map((c, rowIndex) => {
          const meta = classMeta(c)
          const dim = active && active !== c
          return (
            <div
              className="sig-row"
              key={c}
              data-dim={Boolean(dim)}
              data-active={active === c}
              onMouseOver={() => onActive(c, true)}
              onMouseOut={() => onActive(null, true)}
            >
              <div className="sig-class">
                <span className="class-swatch" style={{ background: meta.color }} />
                {meta.label}
              </div>
              {BANDS.map((b, colIndex) => {
                const value = signature[c][b.key]
                return (
                  <div className="sig-cell" key={b.key} style={{ '--i': rowIndex + colIndex }}>
                    <span className="sig-val">{(value * 100).toFixed(value < 0.1 ? 1 : 0)}%</span>
                    <span
                      className="sig-bar"
                      style={{ height: `${Math.max(3, (value / max) * 44)}px`, background: meta.color }}
                    />
                  </div>
                )
              })}
            </div>
          )
        })}
      </div>
    </div>
  )
}
