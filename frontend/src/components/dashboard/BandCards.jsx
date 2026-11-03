import { BANDS } from '../../constants/features.js'
import { projectData } from '../../data/projectData.js'
import { formatNumber, formatPercent } from '../../utils/format.js'
import WaveCanvas from './WaveCanvas.jsx'

const NOTE = 'Band edges are not documented in this project, so no frequencies in Hz are shown.'

// Five compact cards, one per band, for the selected class.
export default function BandCards({ shares, relative }) {
  const ranked = [...BANDS].sort((a, b) => shares[b.key] - shares[a.key]).map((b) => b.key)
  const stats = projectData.dataset.featureStats

  return (
    <ul className="band-cards" aria-label="Band details for the selected class">
      {BANDS.map((b) => {
        const rank = ranked.indexOf(b.key) + 1
        const range = stats[`${b.key}_power`]
        return (
          <li key={b.key} className="band-card" data-rank={rank}>
            <header>
              <h3>{b.label}</h3>
              <span className="tag">{rank === 1 ? 'Strongest' : `Rank ${rank}`}</span>
              <span className="info" tabIndex={0} role="img" aria-label={NOTE} title={NOTE}>
                i
              </span>
            </header>
            <div className="band-card-main">
              <span className="symbol-tile" aria-hidden="true">{b.symbol}</span>
              <div>
                <div className="band-card-value">{formatPercent(shares[b.key] * 100, shares[b.key] < 0.1 ? 2 : 1)}</div>
                <div className="band-card-range">
                  Power range {formatNumber(range.min)} to {formatNumber(range.max)}
                </div>
              </div>
            </div>
            <WaveCanvas band={b.key} amp={relative[b.key]} height={40} glow={8} />
          </li>
        )
      })}
    </ul>
  )
}
