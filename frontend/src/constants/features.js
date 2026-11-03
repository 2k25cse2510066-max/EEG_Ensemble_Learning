// The 15 original model inputs, in the order the Flask backend expects them.
// Descriptions are generic statistical definitions; units and band edges are
// not documented in the project files, so none are claimed here.

export const FEATURE_GROUPS = [
  {
    id: 'amplitude',
    title: 'Amplitude statistics',
    hint: 'Summary of the signal amplitude distribution',
  },
  {
    id: 'shape',
    title: 'Distribution shape',
    hint: 'Asymmetry and tail weight of the amplitude distribution',
  },
  {
    id: 'power',
    title: 'Band power',
    hint: 'Spectral power per frequency band, plus the total',
  },
]

export const FEATURES = [
  { key: 'mean', label: 'Mean', group: 'amplitude', description: 'Average amplitude' },
  { key: 'std', label: 'Standard deviation', group: 'amplitude', description: 'Spread of amplitude around the mean' },
  { key: 'variance', label: 'Variance', group: 'amplitude', description: 'Square of the standard deviation' },
  { key: 'minimum', label: 'Minimum', group: 'amplitude', description: 'Lowest amplitude' },
  { key: 'maximum', label: 'Maximum', group: 'amplitude', description: 'Highest amplitude' },
  { key: 'range', label: 'Range', group: 'amplitude', description: 'Maximum minus minimum' },
  { key: 'rms', label: 'RMS', group: 'amplitude', description: 'Root-mean-square amplitude' },
  { key: 'skewness', label: 'Skewness', group: 'shape', description: 'Asymmetry of the amplitude distribution' },
  { key: 'kurtosis', label: 'Kurtosis', group: 'shape', description: 'Tail weight of the amplitude distribution' },
  { key: 'delta_power', label: 'Delta power', group: 'power', description: 'Power in the delta band' },
  { key: 'theta_power', label: 'Theta power', group: 'power', description: 'Power in the theta band' },
  { key: 'alpha_power', label: 'Alpha power', group: 'power', description: 'Power in the alpha band' },
  { key: 'beta_power', label: 'Beta power', group: 'power', description: 'Power in the beta band' },
  { key: 'gamma_power', label: 'Gamma power', group: 'power', description: 'Power in the gamma band' },
  { key: 'total_power', label: 'Total power', group: 'power', description: 'Total spectral power' },
]

export const FEATURE_KEYS = FEATURES.map((f) => f.key)

// The 14 derived features, mirroring preprocessing/feature_engineering.py.
// eps = 1e-10 in the ratio denominators.
export const DERIVED_FEATURES = [
  { group: 'Relative band power', name: 'delta_ratio', formula: 'delta_power / (total_power + eps)' },
  { group: 'Relative band power', name: 'theta_ratio', formula: 'theta_power / (total_power + eps)' },
  { group: 'Relative band power', name: 'alpha_ratio', formula: 'alpha_power / (total_power + eps)' },
  { group: 'Relative band power', name: 'beta_ratio', formula: 'beta_power / (total_power + eps)' },
  { group: 'Relative band power', name: 'gamma_ratio', formula: 'gamma_power / (total_power + eps)' },
  { group: 'Band-to-band ratios', name: 'theta_alpha_ratio', formula: 'theta_power / (alpha_power + eps)' },
  { group: 'Band-to-band ratios', name: 'delta_alpha_ratio', formula: 'delta_power / (alpha_power + eps)' },
  { group: 'Band-to-band ratios', name: 'delta_beta_ratio', formula: 'delta_power / (beta_power + eps)' },
  { group: 'Band-to-band ratios', name: 'theta_beta_ratio', formula: 'theta_power / (beta_power + eps)' },
  { group: 'Combined band power', name: 'delta_theta_power', formula: 'delta_power + theta_power' },
  { group: 'Combined band power', name: 'alpha_beta_power', formula: 'alpha_power + beta_power' },
  { group: 'Band differences', name: 'delta_alpha_difference', formula: 'delta_power − alpha_power' },
  { group: 'Band differences', name: 'theta_alpha_difference', formula: 'theta_power − alpha_power' },
  { group: 'Band differences', name: 'beta_gamma_difference', formula: 'beta_power − gamma_power' },
]

export const BANDS = [
  { key: 'delta', symbol: 'δ', label: 'Delta' },
  { key: 'theta', symbol: 'θ', label: 'Theta' },
  { key: 'alpha', symbol: 'α', label: 'Alpha' },
  { key: 'beta', symbol: 'β', label: 'Beta' },
  { key: 'gamma', symbol: 'γ', label: 'Gamma' },
]
