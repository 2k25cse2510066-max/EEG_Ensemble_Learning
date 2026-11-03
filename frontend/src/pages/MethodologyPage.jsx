import ResearchNotice from '../components/layout/ResearchNotice.jsx'
import SpectralExplorer from '../components/charts/SpectralExplorer.jsx'
import ClassTag from '../components/ui/ClassTag.jsx'
import Panel from '../components/ui/Panel.jsx'
import { CLASS_ORDER } from '../constants/classes.js'
import { DERIVED_FEATURES, FEATURE_GROUPS, FEATURES } from '../constants/features.js'
import { projectData } from '../data/projectData.js'
import { formatNumber } from '../utils/format.js'

const { dataset, model } = projectData

const STEPS = [
  {
    title: 'Feature extraction',
    text: 'Each EEG segment is summarized as 15 numbers: 7 amplitude statistics, skewness, kurtosis, and 6 power values. This step happens before the code in this repository.',
  },
  {
    title: 'Feature engineering',
    text: '14 features are derived from the band powers: five relative powers, four band-to-band ratios, two sums, and three differences. The backend applies the same formulas at prediction time.',
  },
  {
    title: 'Training',
    text: `An Extra Trees classifier (${Number(model.info['Number of Trees']).toLocaleString('en-US')} trees, ${model.info.Criterion} criterion, max depth ${model.info['Max Depth']}, balanced class weights) is fitted on all ${dataset.samples} rows.`,
  },
  {
    title: 'Validation',
    text: 'Accuracy is estimated with 10-fold stratified cross-validation and with a separate 80/20 stratified holdout split.',
  },
  {
    title: 'Inference',
    text: 'The Flask backend validates the 15 values, engineers the 14 extra features, and returns the predicted class with per-class probabilities.',
  },
]

const LIMITS = [
  'The model reads feature summaries only. There is no raw EEG upload, waveform view, or spectrogram, because the project does not support them.',
  'The extraction step is not in this repository, so units, sampling rate, segment length, and band edges are not documented here.',
  `With ${dataset.samples} samples and a cross-validation spread of ±${model.cvStd.toFixed(1)} points, results vary noticeably between folds.`,
  'Probabilities are tree averages, not calibrated likelihoods. A high value does not mean a correct prediction.',
  'Inputs far outside the training ranges are extrapolation. The form flags values outside the observed range.',
  'This is a research prototype. It has no clinical validation and must not inform diagnosis or treatment.',
]

export default function MethodologyPage() {
  const bandCoverage = CLASS_ORDER.map((c) => Object.values(dataset.bandSignature[c]).reduce((a, b) => a + b, 0))
  const coverageMin = Math.round(Math.min(...bandCoverage) * 100)
  const coverageMax = Math.round(Math.max(...bandCoverage) * 100)

  return (
    <>
      <header className="page-header">
        <div>
          <h1 id="page-title" tabIndex={-1}>
            Data and methods
          </h1>
          <p>What the model was trained on, how features are built, and where the approach stops being reliable.</p>
        </div>
      </header>

      <div className="grid grid-main">
        <Panel title="Dataset" description="dataset/EEG_Extracted_Features.csv">
          <dl className="kv kv-wide">
            <div>
              <dt>Samples</dt>
              <dd>{dataset.samples}</dd>
            </div>
            <div>
              <dt>Extracted features</dt>
              <dd>{dataset.originalFeatureCount}</dd>
            </div>
            <div>
              <dt>Model inputs after engineering</dt>
              <dd>{dataset.engineeredFeatureCount}</dd>
            </div>
            <div>
              <dt>Missing values</dt>
              <dd>{dataset.missingValues}</dd>
            </div>
            <div>
              <dt>Duplicate rows</dt>
              <dd>{dataset.duplicateRows}</dd>
            </div>
          </dl>
          <ul className="class-list class-list-flush">
            {CLASS_ORDER.map((name) => (
              <li key={name}>
                <ClassTag name={name} />
                <span className="class-count">{dataset.classCounts[name]} samples</span>
              </li>
            ))}
          </ul>
        </Panel>

        <Panel title="Pipeline" description="From a feature vector to a class.">
          <ol className="pipeline pipeline-vertical">
            {STEPS.map((step, index) => (
              <li key={step.title}>
                <span className="pipeline-index">{index + 1}</span>
                <div>
                  <h3>{step.title}</h3>
                  <p>{step.text}</p>
                </div>
              </li>
            ))}
          </ol>
        </Panel>
      </div>

      <Panel
        title="Spectral signatures"
        description="Median share of total power in each EEG band, by class, across the 500 training rows. The classes spread their power across bands differently, which is what the ratio features capture."
      >
        <SpectralExplorer signature={dataset.bandSignature} classOrder={CLASS_ORDER} />
        <p className="chart-note">
          The five bands carry {coverageMin} to {coverageMax}% of total power depending on the class; the rest lies
          outside them.
        </p>
      </Panel>

      <Panel
        title="The 15 input features"
        description="Ranges are the minimum, median and maximum over the 500 training rows."
        flush
      >
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th scope="col">Feature</th>
                <th scope="col">Group</th>
                <th scope="col">Meaning</th>
                <th scope="col" className="num">Min</th>
                <th scope="col" className="num">Median</th>
                <th scope="col" className="num">Max</th>
              </tr>
            </thead>
            <tbody>
              {FEATURES.map((f) => {
                const stats = dataset.featureStats[f.key]
                return (
                  <tr key={f.key}>
                    <th scope="row">
                      <code>{f.key}</code>
                    </th>
                    <td>{FEATURE_GROUPS.find((g) => g.id === f.group).title}</td>
                    <td>{f.description}</td>
                    <td className="num">{formatNumber(stats.min)}</td>
                    <td className="num">{formatNumber(stats.median)}</td>
                    <td className="num">{formatNumber(stats.max)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </Panel>

      <Panel
        title="The 14 derived features"
        description="Computed by the backend from the band powers. eps is 1e-10 and only guards against division by zero."
        flush
      >
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th scope="col">Feature</th>
                <th scope="col">Type</th>
                <th scope="col">Formula</th>
              </tr>
            </thead>
            <tbody>
              {DERIVED_FEATURES.map((f) => (
                <tr key={f.name}>
                  <th scope="row">
                    <code>{f.name}</code>
                  </th>
                  <td>{f.group}</td>
                  <td>
                    <code>{f.formula}</code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>

      <Panel title="Limits of this prototype">
        <ul className="limits">
          {LIMITS.map((text) => (
            <li key={text}>{text}</li>
          ))}
        </ul>
      </Panel>

      <ResearchNotice />
    </>
  )
}
