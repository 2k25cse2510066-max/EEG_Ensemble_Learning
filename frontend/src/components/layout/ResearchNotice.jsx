import Icon from '../ui/Icon.jsx'

export default function ResearchNotice({ compact = false }) {
  if (compact) {
    return (
      <p className="notice-compact">
        Research prototype working on pre-computed EEG features. It is not clinically validated and must not be
        used for diagnosis or treatment decisions.
      </p>
    )
  }
  return (
    <aside className="notice" aria-label="Research use only">
      <Icon name="shield" size={20} className="notice-icon" />
      <div>
        <strong>Research prototype, not a diagnostic tool.</strong>
        <p>
          This system classifies feature-level summaries of EEG segments with a model trained on 500 labelled
          samples. It has not been clinically validated, and it does not read raw EEG. Its output must not be used
          to diagnose, monitor, or treat any medical condition.
        </p>
      </div>
    </aside>
  )
}
