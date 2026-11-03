import { CLASS_ORDER, classMeta } from '../../constants/classes.js'
import Icon from '../ui/Icon.jsx'

// Native select, styled to look like the "Today v" menu in the reference design.
export default function ClassSelect({ value, onChange, id = 'class-select' }) {
  return (
    <label className="menu-select" htmlFor={id} style={{ '--class-color': classMeta(value).color }}>
      <span className="sr-only">Class</span>
      <select id={id} value={value} onChange={(event) => onChange(event.target.value)}>
        {CLASS_ORDER.map((name) => (
          <option key={name} value={name}>
            {classMeta(name).label}
          </option>
        ))}
      </select>
      <Icon name="chevron" size={14} />
    </label>
  )
}
