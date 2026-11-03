import { API_BASE_URL } from '../../config.js'
import { classMeta } from '../../constants/classes.js'
import { projectData } from '../../data/projectData.js'
import { formatPercent } from '../../utils/format.js'
import BrainCanvas from '../brain/BrainCanvas.jsx'
import ProbabilityRing from '../charts/ProbabilityRing.jsx'
import ProbabilityBars from '../charts/ProbabilityBars.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import Icon from '../ui/Icon.jsx'
import Spinner from '../ui/Spinner.jsx'

function EmptyState() {
  return (
    <div className="result-empty">
      <svg width="64" height="40" viewBox="0 0 64 40" fill="none" aria-hidden="true">
        <path
          d="M2 20h10l5-14 8 28 7-22 4 8h26"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray="3 5"
        />
      </svg>
      <h3>No prediction yet</h3>
      <p>
        Fill in the 15 features, or start from a real training row, then choose <strong>Run classifier</strong>. The
        predicted class and the model's class probabilities will appear here.
      </p>
    </div>
  )
}

function LoadingState() {
  return (
    <div className="result-loading" role="status">
      <Spinner size={28} />
      <h3>Waiting for the model</h3>
      <p>The backend is engineering the 14 derived features and running the Extra Trees ensemble.</p>
      <div className="skeleton" />
      <div className="skeleton short" />
    </div>
  )
}

const ERROR_COPY = {
  network: { title: 'Cannot reach the backend' },
  timeout: { title: 'The backend took too long to respond' },
  validation: { title: 'The backend rejected the input' },
  server: { title: 'The backend reported an error' },
  'invalid-response': { title: 'Unexpected response from the backend' },
}

function ErrorState({ error, onRetry }) {
  const copy = ERROR_COPY[error.kind] ?? ERROR_COPY.server
  return (
    <div className="result-error">
      <Alert tone="danger" title={copy.title}>
        {error.kind === 'network' || error.kind === 'timeout' ? (
          <>
            <p>
              Nothing answered at <code>{API_BASE_URL}</code>. Start the Flask server from the project root with{' '}
              <code>python backend/app.py</code>, then try again.
            </p>
            <p>If the backend runs on another address, set VITE_API_BASE_URL and restart the dev server.</p>
          </>
        ) : (
          <>
            <p>{error.message}</p>
            {error.missing.length > 0 && (
              <p>
                Missing features: <code>{error.missing.join(', ')}</code>
              </p>
            )}
          </>
        )}
      </Alert>
      <Button icon="refresh" onClick={onRetry}>
        Try again
      </Button>
    </div>
  )
}

function SuccessState({ result }) {
  const meta = classMeta(result.prediction)
  const probabilities = result.classProbabilities
  const sorted = probabilities ? Object.entries(probabilities).sort((a, b) => b[1] - a[1]) : []
  const topProbability = result.probability ?? probabilities?.[result.prediction] ?? null
  const runnerUp = sorted.find(([name]) => name !== result.prediction)
  const margin = runnerUp && topProbability !== null ? topProbability - runnerUp[1] : null
  const { cvMean, cvStd } = projectData.model

  return (
    <div className="result-success">
      <div className="verdict" style={{ '--class-color': meta.color }}>
        <div className="verdict-main">
          <div className="verdict-label">Predicted class</div>
          <div className="verdict-name">{meta.label}</div>
          {topProbability !== null && (
            <div className="verdict-prob">
              <span className="verdict-prob-caption">
                Model probability for this class: {formatPercent(topProbability)}
              </span>
            </div>
          )}
        </div>
        {topProbability !== null && <ProbabilityRing value={topProbability} color={meta.color} />}
      </div>

      {margin !== null && margin < 20 && (
        <Alert tone="warn" title="Close call">
          The runner-up, {classMeta(runnerUp[0]).label}, is only {margin.toFixed(1)} percentage points behind. The
          model separates these two classes less decisively for this input.
        </Alert>
      )}

      {probabilities ? (
        <section aria-labelledby="prob-heading">
          <h3 id="prob-heading">Probability by class</h3>
          <ProbabilityBars probabilities={probabilities} predicted={result.prediction} />
        </section>
      ) : (
        <Alert tone="info">The backend did not return per-class probabilities for this request.</Alert>
      )}

      <section className="context-box" aria-labelledby="context-heading">
        <h3 id="context-heading">How to read these numbers</h3>
        <p>
          The probability above is the average of the 1,000 trees' class probabilities for this one input. It is not
          calibrated, and it is not an accuracy.
        </p>
        <p>
          Model-level accuracy comes from validation: <strong>{cvMean.toFixed(2)}% ± {cvStd.toFixed(2)}%</strong> in
          10-fold cross-validation.{' '}
          <a href="#/performance">See the evaluation details</a>.
        </p>
      </section>

      <details className="raw">
        <summary>
          <Icon name="info" size={14} /> Raw backend response ({result.elapsedMs} ms)
        </summary>
        <pre>{JSON.stringify(result.raw, null, 2)}</pre>
      </details>
    </div>
  )
}

function brainFor(status, result) {
  if (status === 'success' && result) {
    const meta = classMeta(result.prediction)
    const p = result.probability ?? result.classProbabilities?.[result.prediction] ?? 70
    return { color: meta.glow, intensity: 0.55 + 0.45 * (p / 100), pulse: 1 }
  }
  if (status === 'loading') return { color: '#9b8cff', intensity: 0.9, pulse: 3.5 }
  if (status === 'error') return { color: '#ffb347', intensity: 0.5, pulse: 0.6 }
  return { color: '#46dcef', intensity: 0.28, pulse: 0.6 }
}

export default function ResultPanel({ status, result, error, stale, onRetry }) {
  const brain = brainFor(status, result)
  return (
    <section className="panel result" aria-labelledby="result-title" aria-live="polite">
      <header className="panel-head">
        <div>
          <h2 id="result-title">Classification result</h2>
          <p className="panel-desc">Output of the deployed Extra Trees model.</p>
        </div>
      </header>
      <div className="result-brain">
        <BrainCanvas {...brain} controls={false} compact label="Stylised brain that glows in the colour of the predicted class." />
      </div>
      <div className="panel-body">
        {status === 'idle' && <EmptyState />}
        {status === 'loading' && <LoadingState />}
        {status === 'error' && <ErrorState error={error} onRetry={onRetry} />}
        {status === 'success' && stale && (
          <Alert tone="info" title="Inputs changed since this result">
            Run the classifier again to classify the current values.
          </Alert>
        )}
        {status === 'success' && <SuccessState result={result} />}
      </div>
    </section>
  )
}
