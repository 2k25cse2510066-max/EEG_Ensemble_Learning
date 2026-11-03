import { useEffect, useMemo, useRef, useState } from 'react'
import FeatureForm from '../components/analyze/FeatureForm.jsx'
import ResultPanel from '../components/analyze/ResultPanel.jsx'
import ResearchNotice from '../components/layout/ResearchNotice.jsx'
import Alert from '../components/ui/Alert.jsx'
import Button from '../components/ui/Button.jsx'
import { FEATURES } from '../constants/features.js'
import { API_BASE_URL } from '../config.js'
import { projectData } from '../data/projectData.js'
import { usePrediction } from '../hooks/usePrediction.js'
import { consistencyAdvisories, toPayload, validateAll } from '../utils/validation.js'

const emptyValues = () => Object.fromEntries(FEATURES.map((f) => [f.key, '']))

export default function AnalyzePage({ backend }) {
  const [values, setValues] = useState(emptyValues)
  const [touched, setTouched] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [loadedExample, setLoadedExample] = useState(null)
  const [lastRun, setLastRun] = useState(null)
  const prediction = usePrediction()
  const resultRef = useRef(null)

  const errors = useMemo(() => validateAll(values), [values])
  const advisories = useMemo(() => consistencyAdvisories(values), [values])
  const visibleErrors = useMemo(
    () => Object.fromEntries(Object.entries(errors).filter(([key]) => submitted || touched[key])),
    [errors, submitted, touched],
  )
  const stale = prediction.status === 'success' && lastRun !== JSON.stringify(values)

  // On stacked layouts, bring the result into view once it starts loading.
  useEffect(() => {
    if (prediction.status === 'idle') return
    if (window.matchMedia('(max-width: 1180px)').matches) {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
      resultRef.current?.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' })
    }
  }, [prediction.status])

  const handleChange = (key, value) => {
    setValues((prev) => ({ ...prev, [key]: value }))
    setLoadedExample(null)
  }
  const handleBlur = (key) => setTouched((prev) => ({ ...prev, [key]: true }))

  const run = () => {
    setLastRun(JSON.stringify(values))
    prediction.run(toPayload(values))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    setSubmitted(true)
    const firstInvalid = FEATURES.find((f) => errors[f.key])
    if (firstInvalid) {
      document.getElementById(`field-${firstInvalid.key}`)?.focus()
      return
    }
    run()
  }

  const handleReset = () => {
    setValues(emptyValues())
    setTouched({})
    setSubmitted(false)
    setLoadedExample(null)
    setLastRun(null)
    prediction.reset()
  }

  const handleLoadExample = (name) => {
    const example = projectData.dataset.examples[name]
    setValues(Object.fromEntries(FEATURES.map((f) => [f.key, String(Number(example[f.key].toPrecision(8)))])))
    setTouched({})
    setSubmitted(false)
    setLoadedExample(name)
    setLastRun(null)
    prediction.reset()
  }

  const retry = () => {
    if (Object.keys(errors).length === 0) run()
  }

  return (
    <>
      <header className="page-header">
        <div>
          <h1 id="page-title" tabIndex={-1}>
            Analyze a sample
          </h1>
          <p>
            Enter the 15 feature-level values for one EEG segment. The Flask backend adds 14 derived features and the
            trained Extra Trees model returns a class with its probabilities.
          </p>
        </div>
      </header>

      {backend.state === 'offline' && (
        <Alert
          tone="warn"
          title="The backend is not reachable"
          action={
            <Button size="sm" icon="refresh" onClick={backend.recheck}>
              Check again
            </Button>
          }
        >
          Predictions need the Flask server at <code>{API_BASE_URL}</code>. Start it with{' '}
          <code>python backend/app.py</code>. You can still fill in the form meanwhile.
        </Alert>
      )}

      <div className="grid grid-analyze">
        <FeatureForm
          values={values}
          errors={errors}
          visibleErrors={visibleErrors}
          advisories={advisories}
          loadedExample={loadedExample}
          loading={prediction.status === 'loading'}
          onChange={handleChange}
          onBlur={handleBlur}
          onSubmit={handleSubmit}
          onReset={handleReset}
          onLoadExample={handleLoadExample}
        />
        <div className="result-col" ref={resultRef}>
          <ResultPanel
            status={prediction.status}
            result={prediction.result}
            error={prediction.error}
            stale={stale}
            onRetry={retry}
          />
        </div>
      </div>

      <ResearchNotice />
    </>
  )
}
