import { useState } from 'react'
import { classMeta } from '../../constants/classes.js'

// Rows are the true class, columns the predicted class. Hover or focus a cell to read it in words.
export default function ConfusionMatrix({ classes, matrix }) {
  const [cell, setCell] = useState(null)

  let readout = 'Hover or focus a cell to read it.'
  if (cell) {
    const total = matrix[cell.i].reduce((a, b) => a + b, 0)
    const count = matrix[cell.i][cell.j]
    const actual = classMeta(classes[cell.i]).label
    const predicted = classMeta(classes[cell.j]).label
    readout =
      cell.i === cell.j
        ? `${count} of ${total} true "${actual}" samples were classified correctly.`
        : `${count} of ${total} true "${actual}" samples were predicted as "${predicted}".`
  }

  return (
    <div className="cm-wrap" onPointerLeave={() => setCell(null)}>
      <table className="cm">
        <caption className="sr-only">
          Confusion matrix on the 100-sample holdout set. Rows are actual classes, columns are predicted classes.
        </caption>
        <thead>
          <tr>
            <th scope="col" className="cm-corner">
              <span>Actual</span>
              <span>Predicted</span>
            </th>
            {classes.map((c, j) => (
              <th scope="col" key={c} title={classMeta(c).label} data-hot={cell?.j === j}>
                {classMeta(c).short}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => {
            const total = row.reduce((a, b) => a + b, 0)
            return (
              <tr key={classes[i]}>
                <th scope="row" data-hot={cell?.i === i}>
                  {classMeta(classes[i]).label}
                </th>
                {row.map((count, j) => {
                  const rate = total ? count / total : 0
                  const diagonal = i === j
                  const background = diagonal
                    ? `rgba(60, 203, 224, ${0.1 + rate * 0.5})`
                    : count > 0
                      ? `rgba(242, 113, 123, ${0.14 + rate * 1.2})`
                      : 'transparent'
                  const hot = cell && (cell.i === i || cell.j === j)
                  return (
                    <td
                      key={classes[j]}
                      style={{ background, '--i': i + j }}
                      data-diagonal={diagonal}
                      data-hot={hot ? (cell.i === i && cell.j === j ? 'self' : 'line') : undefined}
                      tabIndex={0}
                      onPointerEnter={() => setCell({ i, j })}
                      onFocus={() => setCell({ i, j })}
                    >
                      <span className="cm-count">{count}</span>
                      <span className="cm-rate">{Math.round(rate * 100)}%</span>
                    </td>
                  )
                })}
              </tr>
            )
          })}
        </tbody>
      </table>
      <p className="cm-readout" aria-live="polite">
        {readout}
      </p>
    </div>
  )
}
