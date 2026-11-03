import { useCallback, useEffect, useRef } from 'react'
import { useTicker } from '../../hooks/useTicker.js'

// Stylised oscillation per band. Cycles per 100 px are fixed per band (slow delta ... fast gamma),
// so the line reads as a band signature. Height is driven by `amp` (0..1). It is not EEG data.
const SHAPE = {
  delta: { cycles: 0.55, harmonics: [[1, 1], [2.3, 0.22]], speed: 0.018 },
  theta: { cycles: 1.0, harmonics: [[1, 1], [2.1, 0.3], [3.7, 0.12]], speed: 0.024 },
  alpha: { cycles: 1.7, harmonics: [[1, 1], [2.9, 0.26], [4.3, 0.14]], speed: 0.03 },
  beta: { cycles: 3.1, harmonics: [[1, 1], [1.9, 0.5], [4.7, 0.2]], speed: 0.036 },
  gamma: { cycles: 6.2, harmonics: [[1, 1], [1.7, 0.6], [3.3, 0.35], [7.1, 0.2]], speed: 0.042 },
}

export default function WaveCanvas({ band, amp = 0.5, color = '#8fe9f7', height = 44, glow = 10, className = '' }) {
  const ref = useRef(null)
  const state = useRef({ w: 0, h: 0, dpr: 1, amp, shown: amp, offset: 0 })

  useEffect(() => {
    state.current.amp = amp
  }, [amp])

  const paint = useCallback(() => {
    const canvas = ref.current
    const ctx = canvas?.getContext('2d')
    const s = state.current
    if (!ctx || !s.w) return
    const shape = SHAPE[band] ?? SHAPE.alpha
    ctx.setTransform(s.dpr, 0, 0, s.dpr, 0, 0)
    ctx.clearRect(0, 0, s.w, s.h)
    const mid = s.h / 2
    const maxAmp = s.h * 0.42

    const trace = () => {
      ctx.beginPath()
      for (let x = 0; x <= s.w; x += 2) {
        const phase = ((x + s.offset) / 100) * Math.PI * 2 * shape.cycles
        // Fade the line in and out at both ends.
        const edge = Math.min(1, x / 28, (s.w - x) / 28)
        let y = 0
        for (const [mult, weight] of shape.harmonics) y += Math.sin(phase * mult + mult * 1.7) * weight
        y = (y / 1.6) * maxAmp * s.shown * edge
        if (x === 0) ctx.moveTo(x, mid + y)
        else ctx.lineTo(x, mid + y)
      }
    }
    ctx.lineJoin = 'round'
    trace()
    ctx.strokeStyle = color
    ctx.globalAlpha = 0.35
    ctx.lineWidth = 3.4
    ctx.shadowColor = color
    ctx.shadowBlur = glow
    ctx.stroke()
    trace()
    ctx.globalAlpha = 1
    ctx.lineWidth = 1.4
    ctx.shadowBlur = glow * 0.5
    ctx.stroke()
  }, [band, color, glow])

  useEffect(() => {
    const canvas = ref.current
    if (!canvas) return undefined
    const resize = () => {
      const { width, height: h } = canvas.getBoundingClientRect()
      const dpr = Math.min(2, window.devicePixelRatio || 1)
      Object.assign(state.current, { w: width, h, dpr })
      canvas.width = Math.round(width * dpr)
      canvas.height = Math.round(h * dpr)
      state.current.shown = state.current.amp
      paint()
    }
    resize()
    const observer = new ResizeObserver(resize)
    observer.observe(canvas)
    return () => observer.disconnect()
  }, [paint])

  // Reduced motion: no ticker runs, so repaint once when the amplitude changes.
  useEffect(() => {
    state.current.shown = amp
    paint()
  }, [amp, paint])

  useTicker((now, dt) => {
    const s = state.current
    const shape = SHAPE[band] ?? SHAPE.alpha
    s.offset += dt * shape.speed * 6
    s.shown += (s.amp - s.shown) * 0.1
    paint()
  })

  return <canvas ref={ref} className={`wave ${className}`} style={{ height }} aria-hidden="true" />
}
