import AccuracyBars from '../components/charts/AccuracyBars.jsx'
import ConfusionMatrix from '../components/charts/ConfusionMatrix.jsx'
import RankedBars from '../components/charts/RankedBars.jsx'
import AnimatedNumber from '../components/ui/AnimatedNumber.jsx'
import ResearchNotice from '../components/layout/ResearchNotice.jsx'
import Alert from '../components/ui/Alert.jsx'
import Panel from '../components/ui/Panel.jsx'
import ClassTag from '../components/ui/ClassTag.jsx'
import { projectData } from '../data/projectData.js'
import { DEPLOYED_LABEL, labelDeployed } from '../utils/models.js'

const { model, evaluation } = projectData

const cvItems = labelDeployed(evaluation.cvModels)
const topImportance = evaluation.importance.slice(0, 15)
const derivedInTop10 = evaluation.importance.slice(0, 10).filter((f) => f.derived).length

const CONFIG_ROWS = [
  'Model',
  'Number of Trees',
  'Criterion',
  'Max Depth',
  'Min Samples Split',
  'Min Samples Leaf',
  'Max Features',
  'Class Weight',
  'Random State',
  'Training Samples',
  'Number of Features',
]

function Bar({ value }) {
  return (
    <span className="mini-bar" aria-hidden="true">
      <span style={{ width: `${value * 100}%` }} />
    </span>
  )
}

export default function PerformancePage() {
  return (
    <>
      <header className="page-header">
        <div>
          <h1 id="page-title" tabIndex={-1}>
            Model performance
          </h1>
          <p>
            Every figure on this page is read from the project's own result files. Three different numbers are in play,
            and they answer different questions.
          </p>
        </div>
      </header>

      <section className="grid grid-3" aria-label="What each number means">
        <article className="explain explain-cyan">
          <h2>Cross-validation accuracy</h2>
          <div className="explain-value">
            <AnimatedNumber value={model.cvMean} decimals={2} suffix="%" /> <span className="explain-std">± {model.cvStd.toFixed(2)}</span>
          </div>
          <p>
            Mean and standard deviation of accuracy over 10 stratified, shuffled folds. Each fold is scored on rows the
            model was not fitted on. This is the headline estimate of how well the approach generalizes.
          </p>
        </article>
        <article className="explain explain-violet">
          <h2>Holdout accuracy</h2>
          <div className="explain-value">
            <AnimatedNumber value={model.holdoutAccuracy} decimals={2} suffix="%" />
          </div>
          <p>
            One stratified 80/20 split: a model fitted on 400 rows, scored on {evaluation.holdoutSupport} unseen rows.
            The confusion matrix below comes from this split. With so few test rows, one sample moves it by a point.
          </p>
        </article>
        <article className="explain">
          <h2>Prediction probability</h2>
          <div className="explain-value explain-value-plain">Per input</div>
          <p>
            Returned with each prediction on the Analyze page: the average of the trees' class probabilities for that
            input. It describes one prediction, is not calibrated, and is not an accuracy.
          </p>
        </article>
      </section>

      <div className="grid grid-main">
        <Panel
          title="Confusion matrix"
          description={`Holdout split, ${evaluation.holdoutSupport} samples. Rows are the true class, columns the predicted class; shading shows the share of each row.`}
        >
          <ConfusionMatrix classes={evaluation.confusionClasses} matrix={evaluation.confusion} />
        </Panel>

        <Panel title="Per-class results" description="Same holdout split.">
          <div className="table-scroll">
            <table className="data-table compact">
              <thead>
                <tr>
                  <th scope="col">Class</th>
                  <th scope="col" className="num">Precision</th>
                  <th scope="col" className="num">Recall</th>
                  <th scope="col" className="num">F1</th>
                </tr>
              </thead>
              <tbody>
                {evaluation.perClass.map((row) => (
                  <tr key={row.class}>
                    <th scope="row">
                      <ClassTag name={row.class} short />
                    </th>
                    <td className="num">
                      <Bar value={row.precision} />
                      {row.precision.toFixed(2)}
                    </td>
                    <td className="num">
                      <Bar value={row.recall} />
                      {row.recall.toFixed(2)}
                    </td>
                    <td className="num">
                      <Bar value={row.f1} />
                      {row.f1.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr>
                  <th scope="row">Macro average</th>
                  <td className="num">{evaluation.macro.precision.toFixed(2)}</td>
                  <td className="num">{evaluation.macro.recall.toFixed(2)}</td>
                  <td className="num">{evaluation.macro.f1.toFixed(2)}</td>
                </tr>
              </tfoot>
            </table>
          </div>
          <p className="chart-note">Each class has {evaluation.perClass[0].support} test samples.</p>
        </Panel>
      </div>

      <div className="grid grid-2">
        <Panel
          title="Approaches compared"
          description="10-fold cross-validation on the engineered features. The deployed settings scored highest, though the whiskers overlap with several alternatives."
        >
          <AccuracyBars items={cvItems} highlight={DEPLOYED_LABEL} caption="Cross-validated accuracy by approach" />
        </Panel>
        <Panel
          title="Algorithm benchmark"
          description="Earlier 10-fold comparison across algorithm families. Its Extra Trees run used 500 trees, so its figure differs slightly from the deployed settings."
        >
          <AccuracyBars
            items={evaluation.benchmark}
            highlight="ExtraTrees"
            caption="Cross-validated accuracy by algorithm"
          />
        </Panel>
      </div>

      <div className="grid grid-main">
        <Panel
          title="Which features the model relies on"
          description="Top 15 of 29 by impurity-based importance in the deployed model, as a share of the total."
        >
          <RankedBars
            label="Feature importance"
            items={topImportance.map((f) => ({
              name: f.feature,
              value: f.importance,
              display: `${(f.importance * 100).toFixed(1)}%`,
              tone: f.derived ? 'violet' : 'cyan',
            }))}
          />
          <div className="legend" aria-hidden="true">
            <span><i className="legend-swatch cyan" /> Extracted feature</span>
            <span><i className="legend-swatch violet" /> Derived feature</span>
          </div>
          <p className="chart-note">
            {derivedInTop10} of the 10 most important features are derived, so feature engineering matters to this
            model. Correlated features share credit, so read the ranking as indicative rather than exact.
          </p>
        </Panel>

        <Panel title="Model configuration" description="From results/final_model/final_model_information.csv.">
          <dl className="kv">
            {CONFIG_ROWS.map((row) => (
              <div key={row}>
                <dt>{row}</dt>
                <dd>{model.info[row]}</dd>
              </div>
            ))}
          </dl>
        </Panel>
      </div>

      <Panel title="How far to trust these numbers">
        <div className="caveats">
          <Alert tone="info" title="The deployed model has no untouched test set">
            It was refitted on all 500 rows, so the holdout figure describes a 400-row model with the same settings, not
            the deployed one.
          </Alert>
          <Alert tone="warn" title="Selection can inflate the estimate">
            Settings and feature variants were compared on this same data across the optimization scripts. The best
            cross-validated score among many tries tends to be somewhat optimistic.
          </Alert>
          <Alert tone="warn" title="Subject-level leakage is not ruled out">
            The project files do not say whether rows from the same subject or recording can fall into both training
            and test folds. If they can, accuracy on genuinely new subjects could be lower.
          </Alert>
        </div>
      </Panel>

      <ResearchNotice />
    </>
  )
}
