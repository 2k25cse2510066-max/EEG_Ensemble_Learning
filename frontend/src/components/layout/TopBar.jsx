import { NAV_ITEMS } from '../../constants/navigation.js'
import Icon from '../ui/Icon.jsx'

function BrandMark() {
  return (
    <svg width="26" height="26" viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <defs>
        <linearGradient id="brand-grad" x1="3" y1="4" x2="29" y2="28" gradientUnits="userSpaceOnUse">
          <stop stopColor="#46dcef" />
          <stop offset="1" stopColor="#8f7bff" />
        </linearGradient>
      </defs>
      <circle cx="16" cy="16" r="12.5" stroke="url(#brand-grad)" strokeWidth="1.6" opacity="0.55" />
      <path
        d="M4 16.5h5l2.6-7.5 4.4 14 3.6-10.5 1.8 4H28"
        stroke="url(#brand-grad)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

const STATUS_LABEL = {
  online: 'Backend online',
  offline: 'Backend offline',
  checking: 'Checking backend',
}

export default function TopBar({ route, onNavigate, backend }) {
  const index = Math.max(0, NAV_ITEMS.findIndex((item) => item.id === route))
  return (
    <header className="topbar">
      <a className="brand" href="#/overview" onClick={(e) => { e.preventDefault(); onNavigate('overview') }}>
        <BrandMark />
        <span className="brand-name">
          EEG State Classifier<span className="brand-plus" aria-hidden="true">+</span>
        </span>
      </a>

      <nav className="tabs" aria-label="Main" style={{ '--idx': index, '--count': NAV_ITEMS.length }}>
        <span className="tabs-thumb" aria-hidden="true" />
        {NAV_ITEMS.map((item) => (
          <a
            key={item.id}
            href={`#/${item.id}`}
            aria-current={route === item.id ? 'page' : undefined}
            title={item.hint}
            onClick={(event) => {
              event.preventDefault()
              onNavigate(item.id)
            }}
          >
            {item.short}
          </a>
        ))}
      </nav>

      <div className="topbar-right">
        <button
          type="button"
          className="status-chip"
          data-state={backend.state}
          onClick={backend.recheck}
          disabled={backend.state === 'checking'}
          title={`${backend.message}. Click to check again.`}
        >
          <span className="status-dot" aria-hidden="true" />
          <span>{STATUS_LABEL[backend.state]}</span>
          <Icon name="refresh" size={13} />
        </button>
        <span className="chip-note" title="Research prototype. Not for clinical use.">
          <Icon name="shield" size={14} />
          <span>Research use only</span>
        </span>
      </div>
    </header>
  )
}
