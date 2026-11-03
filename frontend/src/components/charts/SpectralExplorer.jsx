import { useState } from 'react'
import { BANDS } from '../../constants/features.js'
import { classMeta } from '../../constants/classes.js'
import { formatPercent } from '../../utils/format.js'
import BandRadar from './BandRadar.jsx'
import BandSignature from './BandSignature.jsx'

// Interactive container: switch view, hover to preview a class, click a chip to pin it.
export default function SpectralExplorer({ signature, classOrder }) {
  const [view, setView] = useState('bars')
  const [pinned, setPinned] = useState(null)
  const [hovered, setHovered] = useState(null)
  const active = hovered ?? pinned

  const setActive = (name, transient) => (transient ? setHovered(name) : setPinned((p) => (p === name ? null : name)))

  let readout = 'Hover a class to preview it, or select one to pin it.'
  if (active) {
    const [topBand, topShare] = BANDS.map((b) => [b, signature[active][b.key]]).sort((a, b) => b[1] - a[1])[0]
    readout = `${classMeta(active).label}: ${topBand.label.toLowerCase()} holds the largest share, ${formatPercent(topShare * 100, 1)} of total power.`
  }

  return (
    <div className="explorer">
      <div className="explorer-bar">
        <div className="chips" role="group" aria-label="Focus a class">
          {classOrder.map((c) => (
            <button
              key={c}
              type="button"
              className="chip chip-sm"
              aria-pressed={pinned === c}
              data-active={active === c}
              onClick={() => setActive(c, false)}
              onPointerEnter={() => setHovered(c)}
              onPointerLeave={() => setHovered(null)}
              onFocus={() => setHovered(c)}
              onBlur={() => setHovered(null)}
            >
              <span className="class-swatch" style={{ background: classMeta(c).color }} aria-hidden="true" />
              {classMeta(c).short}
            </button>
          ))}
        </div>
        <div className="segmented" role="group" aria-label="Chart type">
          {['bars', 'radar'].map((v) => (
            <button key={v} type="button" aria-pressed={view === v} onClick={() => setView(v)}>
              {v === 'bars' ? 'Bars' : 'Radar'}
            </button>
          ))}
        </div>
      </div>

      <div className="explorer-stage" key={view}>
        {view === 'bars' ? (
          <BandSignature signature={signature} classOrder={classOrder} active={active} onActive={setActive} />
        ) : (
          <BandRadar signature={signature} classOrder={classOrder} active={active} onActive={setActive} />
        )}
      </div>
      <p className="explorer-readout" aria-live="polite">
        {readout}
      </p>
    </div>
  )
}
