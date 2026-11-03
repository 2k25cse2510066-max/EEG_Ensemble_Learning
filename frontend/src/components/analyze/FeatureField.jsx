import { projectData } from '../../data/projectData.js'
import { formatNumber } from '../../utils/format.js'
import Icon from '../ui/Icon.jsx'

export default function FeatureField({ feature, value, error, note, onChange, onBlur }) {
  const inputId = `field-${feature.key}`
  const helpId = `${inputId}-help`
  const stats = projectData.dataset.featureStats[feature.key]

  return (
    <div className="field" data-invalid={Boolean(error)}>
      <label htmlFor={inputId} className="field-label">
        <span>{feature.label}</span>
        <code>{feature.key}</code>
      </label>
      <input
        id={inputId}
        name={feature.key}
        type="text"
        inputMode="decimal"
        autoComplete="off"
        spellCheck={false}
        value={value}
        placeholder={formatNumber(stats.median)}
        aria-invalid={Boolean(error)}
        aria-describedby={helpId}
        onChange={(event) => onChange(feature.key, event.target.value)}
        onBlur={() => onBlur(feature.key)}
      />
      <p id={helpId} className="field-help" data-tone={error ? 'danger' : note ? 'warn' : 'neutral'}>
        {error ? (
          <>
            <Icon name="alert" size={13} /> {error}
          </>
        ) : note ? (
          <>
            <Icon name="alert" size={13} /> {note}
          </>
        ) : (
          <>
            {feature.description}. Training range {formatNumber(stats.min)} to {formatNumber(stats.max)}.
          </>
        )}
      </p>
    </div>
  )
}
