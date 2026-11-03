// The cross-validation file calls the deployed configuration "Extra Trees Baseline".
// The UI names it by what it is.
export const DEPLOYED_LABEL = 'Extra Trees (deployed settings)'

export function labelDeployed(items) {
  return items.map((item) => (item.model === 'Extra Trees Baseline' ? { ...item, model: DEPLOYED_LABEL } : item))
}
