import { useEffect, useState } from 'react'

const prefersReducedMotion = () =>
  typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

// Eases a number from 0 to `target`. Reduced-motion users get the final value immediately.
export function useCountUp(target, duration = 1200) {
  const [value, setValue] = useState(() => (prefersReducedMotion() ? target : 0))

  useEffect(() => {
    if (prefersReducedMotion()) return undefined
    let frame
    let start
    const tick = (now) => {
      start ??= now
      const progress = Math.min(1, (now - start) / duration)
      setValue(target * (1 - Math.pow(1 - progress, 3)))
      if (progress < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [target, duration])

  return prefersReducedMotion() ? target : value
}
