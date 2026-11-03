import Icon from './Icon.jsx'

const ICONS = { info: 'info', warn: 'alert', danger: 'alert', ok: 'check' }

export default function Alert({ tone = 'info', title, children, action, role }) {
  const resolvedRole = role ?? (tone === 'danger' ? 'alert' : 'status')
  return (
    <div className={`alert alert-${tone}`} role={resolvedRole}>
      <Icon name={ICONS[tone]} size={18} className="alert-icon" />
      <div className="alert-body">
        {title && <strong>{title}</strong>}
        {children && <div>{children}</div>}
      </div>
      {action && <div className="alert-action">{action}</div>}
    </div>
  )
}
