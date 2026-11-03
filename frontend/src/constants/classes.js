// Display metadata for the five classes the model was trained on.
// The keys are the exact labels returned by the backend.

export const CLASS_ORDER = [
  'Healthy_Eyes_Open',
  'Healthy_Eyes_Closed',
  'Epileptic_No_Seizure',
  'Epileptogenic_Region',
  'Seizure',
]

const META = {
  Healthy_Eyes_Open: { label: 'Healthy, eyes open', short: 'Eyes open' },
  Healthy_Eyes_Closed: { label: 'Healthy, eyes closed', short: 'Eyes closed' },
  Epileptic_No_Seizure: { label: 'Epileptic, no seizure', short: 'No seizure' },
  Epileptogenic_Region: { label: 'Epileptogenic region', short: 'Epileptogenic' },
  Seizure: { label: 'Seizure', short: 'Seizure' },
}

// Brighter versions of the class colours, used for glows on dark backgrounds.
const GLOW = {
  Healthy_Eyes_Open: '#3fc8ff',
  Healthy_Eyes_Closed: '#35f0c8',
  Epileptic_No_Seizure: '#8f7bff',
  Epileptogenic_Region: '#e066ff',
  Seizure: '#ff2d55',
}

// Falls back gracefully if the backend ever returns an unexpected class name.
export function classMeta(name) {
  const known = META[name]
  const label = known?.label ?? String(name).replaceAll('_', ' ')
  return {
    key: name,
    label,
    short: known?.short ?? label,
    color: known ? `var(--c-${name})` : 'var(--text-2)',
    glow: GLOW[name] ?? '#46dcef',
  }
}
