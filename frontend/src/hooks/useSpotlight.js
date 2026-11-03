import { useEffect } from 'react'

// Cursor-reactive lighting: cards get a local glow, the page gets a soft global one.
export function useSpotlight() {
  useEffect(() => {
    let frame = 0
    const onMove = (event) => {
      const card = event.target.closest?.('.panel, .stat, .explain')
      if (card) {
        const rect = card.getBoundingClientRect()
        card.style.setProperty('--mx', `${event.clientX - rect.left}px`)
        card.style.setProperty('--my', `${event.clientY - rect.top}px`)
      }
      if (!frame) {
        frame = requestAnimationFrame(() => {
          frame = 0
          document.documentElement.style.setProperty('--gx', `${event.clientX}px`)
          document.documentElement.style.setProperty('--gy', `${event.clientY}px`)
        })
      }
    }
    document.addEventListener('pointermove', onMove, { passive: true })
    return () => {
      document.removeEventListener('pointermove', onMove)
      cancelAnimationFrame(frame)
    }
  }, [])
}
