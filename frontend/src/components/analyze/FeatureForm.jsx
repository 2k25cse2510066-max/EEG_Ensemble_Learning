import { FEATURE_GROUPS, FEATURES } from '../../constants/features.js'
import { CLASS_ORDER } from '../../constants/classes.js'
import { rangeNote } from '../../utils/validation.js'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import ClassTag from '../ui/ClassTag.jsx'
import FeatureField from './FeatureField.jsx'
import LiveProfile from './LiveProfile.jsx'

export default function FeatureForm({
  values,
  errors,
  visibleErrors,
  advisories,
  loadedExample,
  loading,
  onChange,
  onBlur,
  onSubmit,
  onReset,
  onLoadExample,
}) {
  const invalidCount = Object.keys(errors).length
  const filled = FEATURES.filter((f) => String(values[f.key]).trim() !== '').length

  return (
    <form className="panel form" onSubmit={onSubmit} noValidate aria-labelledby="form-title">
      <header className="panel-head">
        <div>
          <h2 id="form-title">Input features</h2>
          <p className="panel-desc">
            The 15 extracted EEG features the model expects. The 14 derived features are computed by the backend.
          </p>
        </div>
        <span className="progress-pill" aria-live="polite">
          {filled} of {FEATURES.length} filled
        </span>
      </header>

      <div className="examples" role="group" aria-label="Load a training example">
        <div className="examples-title">Start from a real training row</div>
        <div className="examples-list">
          {CLASS_ORDER.map((name) => (
            <button
              key={name}
              type="button"
              className="chip"
              data-active={loadedExample === name}
              aria-pressed={loadedExample === name}
              onClick={() => onLoadExample(name)}
            >
              <ClassTag name={name} short />
            </button>
          ))}
        </div>
        {loadedExample ? (
          <p className="examples-note">
            Loaded the training row closest to the median of <strong>{loadedExample.replaceAll('_', ' ')}</strong>. The
            deployed model was trained on all 500 rows, including this one, so its probabilities here are not a test
            of accuracy.
          </p>
        ) : (
          <p className="examples-note">Each button fills the form with one real row from the dataset.</p>
        )}
      </div>

      {FEATURE_GROUPS.map((group) => (
        <fieldset className="fieldset" key={group.id}>
          <legend>
            {group.title}
            <span>{group.hint}</span>
          </legend>
          <div className="field-grid">
            {FEATURES.filter((f) => f.group === group.id).map((feature) => (
              <FeatureField
                key={feature.key}
                feature={feature}
                value={values[feature.key]}
                error={visibleErrors[feature.key]}
                note={rangeNote(feature.key, values[feature.key])}
                onChange={onChange}
                onBlur={onBlur}
              />
            ))}
          </div>
        </fieldset>
      ))}

      <LiveProfile values={values} />

      {advisories.length > 0 && (
        <Alert tone="warn" title="These values look unlike the training data">
          <ul className="advisory-list">
            {advisories.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
          <p className="advisory-foot">You can still run the classifier, but treat the result with extra caution.</p>
        </Alert>
      )}

      {Object.keys(visibleErrors).length > 0 && invalidCount > 0 && (
        <Alert tone="danger" title={`${invalidCount} ${invalidCount === 1 ? 'field needs' : 'fields need'} attention`}>
          Every one of the 15 features must be a number before the model can run.
        </Alert>
      )}

      <div className="form-actions">
        <Button type="submit" variant="primary" icon="play" loading={loading}>
          {loading ? 'Classifying…' : 'Run classifier'}
        </Button>
        <Button icon="reset" onClick={onReset} disabled={loading}>
          Clear form
        </Button>
      </div>
    </form>
  )
}
