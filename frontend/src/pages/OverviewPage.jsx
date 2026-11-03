import { useEffect, useMemo, useState } from 'react'
import BrainCanvas from '../components/brain/BrainCanvas.jsx'
import AccuracyColumns from '../components/dashboard/AccuracyColumns.jsx'
import BandCards from '../components/dashboard/BandCards.jsx'
import BandPanel from '../components/dashboard/BandPanel.jsx'
import ClassScrubber from '../components/dashboard/ClassScrubber.jsx'
import Button from '../components/ui/Button.jsx'
import { CLASS_ORDER, classMeta } from '../constants/classes.js'
import { BANDS } from '../constants/features.js'
import { projectData } from '../data/projectData.js'
import { prefersReducedMotion } from '../hooks/useTicker.js'
import { formatPercent } from '../utils/format.js'

const { dataset, model } = projectData
const TOUR_MS = 4200

const PIPELINE = [
  { title: 'Input', text: `${dataset.originalFeatureCount} extracted features: amplitude, shape and band power.` },
  { title: 'Feature engineering', text: `${dataset.engineeredFeatureCount - dataset.originalFeatureCount} derived ratios, sums and differences give ${dataset.engineeredFeatureCount} inputs.` },
  { title: 'Extra Trees', text: `${Number(model.info['Number of Trees']).toLocaleString('en-US')} trees, ${model.info.Criterion} criterion, max depth ${model.info['Max Depth']}.` },
  { title: 'Output', text: 'The predicted class and a probability for each of the five classes.' },
]

// For each band, the highest median share over all classes. Used to scale the wave heights.
const bandMax = Object.fromEntries(BANDS.map((b) => [b.key, Math.max(...CLASS_ORDER.map((c) => dataset.bandSignature[c][b.key]))]))
const relative = Object.fromEntries(
  CLASS_ORDER.map((c) => [c, Object.fromEntries(BANDS.map((b) => [b.key, 0.18 + 0.82 * (dataset.bandSignature[c][b.key] / bandMax[b.key])]))]),
)

export default function OverviewPage({ onNavigate }) {
  const [classKey, setClassKey] = useState('Seizure')
  const [playing, setPlaying] = useState(false)
  const meta = classMeta(classKey)
  const shares = dataset.bandSignature[classKey]

  useEffect(() => {
    if (!playing || prefersReducedMotion()) return undefined
    const timer = setInterval(() => {
      setClassKey((current) => CLASS_ORDER[(CLASS_ORDER.indexOf(current) + 1) % CLASS_ORDER.length])
    }, TOUR_MS)
    return () => clearInterval(timer)
  }, [playing])

  const choose = (name) => {
    setPlaying(false)
    setClassKey(name)
  }

  const readout = useMemo(() => {
    const top = BANDS.reduce((best, b) => (shares[b.key] > shares[best.key] ? b : best), BANDS[0])
    return `${top.label} holds the largest share, ${formatPercent(shares[top.key] * 100, 1)} of total power.`
  }, [shares])

  return (
    <>
      <h1 id="page-title" tabIndex={-1} className="sr-only">
        Epilepsy-related EEG state classification: overview
      </h1>

      <div className="dash">
        <section className="panel brain-panel" aria-label="Class explorer" style={{ '--class-glow': meta.glow }}>
          <BrainCanvas color={meta.glow} intensity={1} />
          <div className="brain-title">
            <span className="brain-kicker">Selected class</span>
            <strong>{meta.label}</strong>
            <span aria-live="polite">{readout}</span>
          </div>
          <dl className="brain-kpis">
            <div>
              <dt>10-fold CV accuracy</dt>
              <dd>
                {model.cvMean.toFixed(1)}%<small> ± {model.cvStd.toFixed(1)}</small>
              </dd>
            </div>
            <div>
              <dt>Holdout accuracy</dt>
              <dd>{model.holdoutAccuracy.toFixed(1)}%</dd>
            </div>
            <div>
              <dt>Samples, inputs</dt>
              <dd>
                {dataset.samples}
                <small>, {dataset.engineeredFeatureCount}</small>
              </dd>
            </div>
          </dl>
          <div className="brain-cta">
            <Button variant="primary" icon="analyze" onClick={() => onNavigate('analyze')}>
              Analyze a sample
            </Button>
          </div>
          <p className="brain-caption">Illustration. The glow marks the selected class, not a location in the brain.</p>
        </section>

        <div className="dash-right">
          <BandPanel classKey={classKey} onClassChange={choose} signature={dataset.bandSignature} relative={relative} />
          <AccuracyColumns />
        </div>

        <BandCards shares={shares} relative={relative[classKey]} />

        <ClassScrubber
          value={classKey}
          onChange={choose}
          playing={playing}
          onTogglePlay={() => setPlaying((p) => !p)}
          counts={dataset.classCounts}
        />
      </div>

      <section className="panel steps-panel" aria-labelledby="steps-title">
        <header className="panel-head">
          <div>
            <h2 id="steps-title">How a prediction is made</h2>
            <p className="panel-desc">Everything the backend does between the form and the result.</p>
          </div>
        </header>
        <ol className="steps">
          {PIPELINE.map((step, index) => (
            <li key={step.title}>
              <span className="pipeline-index">{index + 1}</span>
              <div>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>
    </>
  )
}
