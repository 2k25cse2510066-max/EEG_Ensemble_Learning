import { classMeta } from '../../constants/classes.js'

export default function ClassTag({ name, short = false }) {
  const meta = classMeta(name)
  return (
    <span className="class-tag">
      <span className="class-swatch" style={{ background: meta.color }} aria-hidden="true" />
      {short ? meta.short : meta.label}
    </span>
  )
}
