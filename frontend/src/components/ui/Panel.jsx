import { useId } from 'react'

export default function Panel({ title, description, actions, children, className = '', flush = false }) {
  const headingId = useId()
  return (
    <section className={`panel ${className}`} aria-labelledby={title ? headingId : undefined}>
      {(title || actions) && (
        <header className="panel-head">
          <div>
            {title && <h2 id={headingId}>{title}</h2>}
            {description && <p className="panel-desc">{description}</p>}
          </div>
          {actions && <div className="panel-actions">{actions}</div>}
        </header>
      )}
      <div className={flush ? 'panel-body flush' : 'panel-body'}>{children}</div>
    </section>
  )
}
