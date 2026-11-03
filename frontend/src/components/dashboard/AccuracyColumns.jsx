import { useState } from 'react'
import { projectData } from '../../data/projectData.js'
import { DEPLOYED_LABEL, labelDeployed } from '../../utils/models.js'
import Icon from '../ui/Icon.jsx'

const COLORS = ['#ff4d6d', '#d9b13f', '#3cc4e0', '#7be04c', '#7aa7ff', '#9b8cff', '#ff9a56', '#5fe0b4']
const MIN = 60
const MAX = 100
const pct = (v) => ((Math.min(MAX, Math.max(MIN, v)) - MIN) / (MAX - MIN)) * 100

const SETS = {
  approaches: { label: 'Approaches', items: labelDeployed(projectData.evaluation.cvModels), best: DEPLOYED_LABEL },
  algorithms: { label: 'Algorithms', items: projectData.evaluation.benchmark, best: 'ExtraTrees' },
}

// Column chart of cross-validated accuracy, in the style of the "Time spend" panel.
export default function AccuracyColumns() {
  const [setKey, setSetKey] = useState('approaches')
  const [hover, setHover] = useState(null)
  const { items, best } = SETS[setKey]
  const bestItem = items.find((i) => i.model === best)
  const shown = items.slice(0, 6)

  return (
    <section className="panel acc-panel" aria-labelledby="acc-title">
      <header className="panel-head">
        <div>
          <h2 id="acc-title">Model accuracy</h2>
          <p className="panel-desc">Cross-validated, axis from {MIN}%</p>
        </div>
        <div className="panel-actions">
          <label className="menu-select">
            <span className="sr-only">Compare</span>
            <select
              value={setKey}
              onChange={(event) => {
                setSetKey(event.target.value)
                setHover(null)
              }}
            >
              {Object.entries(SETS).map(([key, set]) => (
                <option key={key} value={key}>
                  {set.label}
                </option>
              ))}
            </select>
            <Icon name="chevron" size={14} />
          </label>
          <span className="pill">Deployed: {bestItem.mean.toFixed(1)}%</span>
        </div>
      </header>

      <div className="cols" key={setKey}>
        <table className="sr-only">
          <caption>Cross-validated accuracy by {SETS[setKey].label.toLowerCase()}</caption>
          <tbody>
            {shown.map((i) => (
              <tr key={i.model}>
                <th scope="row">{i.model}</th>
                <td>
                  {i.mean.toFixed(1)}% plus or minus {i.std.toFixed(1)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="cols-plot" aria-hidden="true">
          {[60, 80, 100].map((t) => (
            <span key={t} className="cols-grid" style={{ bottom: `${pct(t)}%` }}>
              {t}
            </span>
          ))}
          {shown.map((item, index) => (
            <div
              key={item.model}
              className="col"
              data-best={item.model === best}
              data-dim={hover !== null && hover !== item.model}
              style={{
                '--c': COLORS[index % COLORS.length],
                '--h': `${pct(item.mean)}%`,
                '--lo': `${pct(item.mean - item.std)}%`,
                '--hi': `${pct(item.mean + item.std)}%`,
                '--i': index,
              }}
              onPointerEnter={() => setHover(item.model)}
              onPointerLeave={() => setHover(null)}
            >
              <span className="col-value">{item.mean.toFixed(1)}</span>
              <span className="col-bar" />
              <span className="col-whisker" />
            </div>
          ))}
        </div>
      </div>

      <ul className="legend" aria-hidden="true">
        {shown.map((item, index) => (
          <li key={item.model} data-dim={hover !== null && hover !== item.model} onPointerEnter={() => setHover(item.model)} onPointerLeave={() => setHover(null)}>
            <i style={{ background: COLORS[index % COLORS.length] }} />
            {item.model}
          </li>
        ))}
      </ul>
    </section>
  )
}
