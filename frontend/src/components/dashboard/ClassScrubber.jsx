import { CLASS_ORDER, classMeta } from '../../constants/classes.js'
import Icon from '../ui/Icon.jsx'

const stops = CLASS_ORDER.map((name, i) => `${classMeta(name).color} ${(i / (CLASS_ORDER.length - 1)) * 100}%`).join(', ')

// The timeline of the reference design, repurposed: a slider that steps through the five classes.
export default function ClassScrubber({ value, onChange, playing, onTogglePlay, counts }) {
  const index = CLASS_ORDER.indexOf(value)
  return (
    <div className="scrubber" style={{ '--stops': stops, '--idx': index }}>
      <button
        type="button"
        className="round-btn"
        aria-pressed={playing}
        aria-label={playing ? 'Pause the class tour' : 'Play a tour through the classes'}
        onClick={onTogglePlay}
      >
        <Icon name={playing ? 'pause' : 'play'} size={15} />
      </button>
      <div className="scrubber-body">
        <input
          type="range"
          min={0}
          max={CLASS_ORDER.length - 1}
          step={1}
          value={index}
          aria-label="Class shown on this dashboard"
          aria-valuetext={classMeta(value).label}
          onChange={(event) => onChange(CLASS_ORDER[Number(event.target.value)])}
        />
        <ol className="scrubber-labels">
          {CLASS_ORDER.map((name) => (
            <li key={name}>
              <button type="button" data-active={name === value} onClick={() => onChange(name)}>
                {classMeta(name).short}
                <small>{counts[name]} samples</small>
              </button>
            </li>
          ))}
        </ol>
      </div>
    </div>
  )
}
