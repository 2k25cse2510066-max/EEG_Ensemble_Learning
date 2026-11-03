import { useCountUp } from '../../hooks/useCountUp.js'

// Counts up visually; assistive tech reads the final value once.
export default function AnimatedNumber({ value, decimals = 0, suffix = '' }) {
  const current = useCountUp(value)
  const format = (n) => n.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
  return (
    <>
      <span aria-hidden="true">
        {format(current)}
        {suffix}
      </span>
      <span className="sr-only">
        {format(value)}
        {suffix}
      </span>
    </>
  )
}
