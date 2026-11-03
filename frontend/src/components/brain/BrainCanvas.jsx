import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { prefersReducedMotion, useTicker } from '../../hooks/useTicker.js'
import Icon from '../ui/Icon.jsx'
import { HOTSPOT, buildArcs, buildBrain } from './brainGeometry.js'

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v))

function hexToRgb(hex) {
  const h = hex.replace('#', '')
  const n = parseInt(h.length === 3 ? h.replace(/./g, '$&$&') : h, 16)
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255]
}

/**
 * Interactive, stylised 3D brain drawn on a canvas.
 * `color` tints the glowing hotspot (the selected class), `intensity` sets how strong it is.
 * Drag to rotate, use the buttons or arrow keys / +/- to zoom. Purely illustrative.
 */
export default function BrainCanvas({
  color = '#ff3350',
  intensity = 1,
  pulse = 1,
  controls = true,
  compact = false,
  label = 'Stylised 3D brain. The glow marks the selected class, not a location.',
}) {
  const wrapRef = useRef(null)
  const canvasRef = useRef(null)
  const brain = useMemo(() => {
    const points = buildBrain()
    return { points, arcs: buildArcs(points) }
  }, [])

  const view = useRef({ yaw: 1.0, pitch: 0.1, zoom: 1, sway: 0.5, dragging: false, lastX: 0, lastY: 0, vyaw: 0, size: [0, 0], dpr: 1 })
  const live = useRef({ color: hexToRgb(color), intensity, pulse, shownColor: hexToRgb(color), shownIntensity: intensity })
  const [zoomLabel, setZoomLabel] = useState(100)
  const reduced = prefersReducedMotion()

  useEffect(() => {
    live.current.color = hexToRgb(color)
    live.current.intensity = intensity
    live.current.pulse = pulse
  }, [color, intensity, pulse])

  const draw = useCallback(
    (now) => {
      const canvas = canvasRef.current
      const ctx = canvas?.getContext('2d')
      const v = view.current
      if (!ctx || !v.size[0]) return
      const [W, H] = v.size
      const L = live.current

      // Ease colour and intensity toward their targets so class changes feel continuous.
      for (let i = 0; i < 3; i += 1) L.shownColor[i] += (L.color[i] - L.shownColor[i]) * 0.12
      L.shownIntensity += (L.intensity - L.shownIntensity) * 0.1
      const [cr, cg, cb] = L.shownColor.map(Math.round)

      ctx.setTransform(v.dpr, 0, 0, v.dpr, 0, 0)
      ctx.clearRect(0, 0, W, H)

      const scale = Math.min(W * 0.5, H * 0.62) * v.zoom
      const cx = W / 2
      const cy = H * (compact ? 0.5 : 0.47)

      // Platform rings under the brain.
      const ringY = H * (compact ? 0.86 : 0.84)
      ctx.save()
      ctx.globalCompositeOperation = 'lighter'
      for (const [k, a] of [[0.62, 0.55], [0.8, 0.18]]) {
        ctx.beginPath()
        ctx.ellipse(cx, ringY, scale * k * 1.12, scale * k * 0.2, 0, 0, Math.PI * 2)
        ctx.strokeStyle = `rgba(70, 220, 239, ${a})`
        ctx.lineWidth = k < 0.7 ? 1.6 : 1
        ctx.shadowColor = 'rgba(70, 220, 239, 0.9)'
        ctx.shadowBlur = k < 0.7 ? 14 : 6
        ctx.stroke()
      }
      ctx.restore()

      const yawNow = v.yaw + v.sway * Math.sin(now * 0.00028)
      const cosY = Math.cos(yawNow)
      const sinY = Math.sin(yawNow)
      const cosP = Math.cos(v.pitch)
      const sinP = Math.sin(v.pitch)
      const project = (x, y, z) => {
        const x1 = x * cosY + z * sinY
        const z1 = -x * sinY + z * cosY
        const y2 = y * cosP - z1 * sinP
        const z2 = y * sinP + z1 * cosP
        return [x1, y2, z2]
      }

      // Hotspot position and how much it faces the camera.
      const [hx, hy] = project(HOTSPOT[0] * 0.62, HOTSPOT[1] * 0.5, HOTSPOT[2] * 0.74)
      const [, , hn] = project(HOTSPOT[0], HOTSPOT[1], HOTSPOT[2])
      const facing = clamp((hn + 0.15) / 0.85, 0, 1)
      const beat = 0.78 + 0.22 * Math.sin(now * 0.0028 * L.pulse)
      const strength = L.shownIntensity * facing

      ctx.globalCompositeOperation = 'lighter'
      const cosHot = HOTSPOT
      for (const p of brain.points) {
        const [x, y, z] = project(p.x, p.y, p.z)
        const [, , nz] = project(p.nx, p.ny, p.nz)
        const front = clamp(nz * 0.5 + 0.5, 0, 1)
        const depth = clamp((z + 0.8) / 1.6, 0, 1)
        const rim = Math.pow(1 - Math.abs(nz), 2.2)
        const crest = p.ridge * 0.5 + 0.5 // folds: ridges bright, grooves dark
        let light = (0.1 + front * 0.5 + rim * 0.34 + depth * 0.18) * (0.3 + 1.15 * crest * crest)
        const near = p.kind === 'cerebrum' ? p.nx * cosHot[0] + p.ny * cosHot[1] + p.nz * cosHot[2] : -1
        const heat = clamp((near - 0.82) / 0.18, 0, 1) * L.shownIntensity
        const sx = cx + x * scale
        const sy = cy - y * scale
        const size = (0.75 + depth * 0.75 + heat * 1.1) * (compact ? 0.85 : 1) * Math.min(1.4, v.zoom * 0.7 + 0.3)
        if (heat > 0.02) {
          const k = heat * beat
          ctx.fillStyle = `rgba(${Math.round(150 + (cr - 150) * k)}, ${Math.round(190 + (cg - 190) * k)}, ${Math.round(235 + (cb - 235) * k)}, ${clamp(light * 0.9 + k * 0.45, 0, 1)})`
        } else {
          const tw = 0.88 + 0.12 * Math.sin(now * 0.0016 + p.tw)
          ctx.fillStyle = `rgba(170, 195, 240, ${clamp(light * 0.7 * tw, 0, 0.95)})`
        }
        ctx.fillRect(sx - size / 2, sy - size / 2, size, size)
      }

      // Signal arcs travelling away from the hotspot.
      if (strength > 0.05) {
        ctx.lineWidth = 1
        for (const arc of brain.arcs) {
          const t = ((now * arc.speed + arc.phase) % 1)
          const bez = (u) => {
            const w = 1 - u
            return [
              w * w * arc.a.x + 2 * w * u * arc.m.x + u * u * arc.b.x,
              w * w * arc.a.y + 2 * w * u * arc.m.y + u * u * arc.b.y,
              w * w * arc.a.z + 2 * w * u * arc.m.z + u * u * arc.b.z,
            ]
          }
          ctx.beginPath()
          const tail = Math.max(0, t - 0.22)
          for (let i = 0; i <= 10; i += 1) {
            const [x, y, z] = bez(tail + ((t - tail) * i) / 10)
            const [px, py] = project(x, y, z)
            if (i === 0) ctx.moveTo(cx + px * scale, cy - py * scale)
            else ctx.lineTo(cx + px * scale, cy - py * scale)
          }
          ctx.strokeStyle = `rgba(${cr}, ${cg}, ${cb}, ${0.5 * strength * (1 - t)})`
          ctx.stroke()
        }
      }

      // Soft glow at the hotspot.
      if (strength > 0.01) {
        const gx = cx + hx * scale
        const gy = cy - hy * scale
        const radius = scale * (0.36 + 0.06 * beat)
        const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, radius)
        g.addColorStop(0, `rgba(${cr}, ${cg}, ${cb}, ${0.8 * strength * beat})`)
        g.addColorStop(0.35, `rgba(${cr}, ${cg}, ${cb}, ${0.28 * strength})`)
        g.addColorStop(1, `rgba(${cr}, ${cg}, ${cb}, 0)`)
        ctx.fillStyle = g
        ctx.beginPath()
        ctx.arc(gx, gy, radius, 0, Math.PI * 2)
        ctx.fill()
      }
      ctx.globalCompositeOperation = 'source-over'
    },
    [brain, compact],
  )

  const resize = useCallback(() => {
    const wrap = wrapRef.current
    const canvas = canvasRef.current
    if (!wrap || !canvas) return
    const { width, height } = wrap.getBoundingClientRect()
    const dpr = Math.min(2, window.devicePixelRatio || 1)
    view.current.size = [width, height]
    view.current.dpr = dpr
    canvas.width = Math.round(width * dpr)
    canvas.height = Math.round(height * dpr)
    draw(performance.now())
  }, [draw])

  useEffect(() => {
    resize()
    const observer = new ResizeObserver(resize)
    if (wrapRef.current) observer.observe(wrapRef.current)
    return () => observer.disconnect()
  }, [resize])

  // Redraw once when props change for reduced-motion users (no ticker running).
  useEffect(() => {
    if (!reduced) return undefined
    const id = requestAnimationFrame(function settle() {
      draw(performance.now())
      const L = live.current
      const done = L.shownColor.every((c, i) => Math.abs(c - L.color[i]) < 1) && Math.abs(L.shownIntensity - L.intensity) < 0.01
      if (!done) requestAnimationFrame(settle)
    })
    return () => cancelAnimationFrame(id)
  }, [color, intensity, reduced, draw])

  useTicker((now) => {
    const v = view.current
    if (!v.dragging) {
      v.yaw += v.vyaw
      v.vyaw *= 0.94
    }
    draw(now)
  })

  const setZoom = (next) => {
    view.current.zoom = clamp(next, 0.7, 1.7)
    setZoomLabel(Math.round(view.current.zoom * 100))
    if (reduced) draw(performance.now())
  }
  const reset = () => {
    Object.assign(view.current, { yaw: 1.0, pitch: 0.1, vyaw: 0, sway: 0.5 })
    setZoom(1)
  }

  const onPointerDown = (event) => {
    const v = view.current
    v.dragging = true
    v.sway = 0
    v.lastX = event.clientX
    v.lastY = event.clientY
    v.vyaw = 0
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  const onPointerMove = (event) => {
    const v = view.current
    if (!v.dragging) return
    const dx = event.clientX - v.lastX
    const dy = event.clientY - v.lastY
    v.lastX = event.clientX
    v.lastY = event.clientY
    v.yaw += dx * 0.009
    v.vyaw = dx * 0.0016
    v.pitch = clamp(v.pitch + dy * 0.006, -0.6, 0.7)
    if (reduced) draw(performance.now())
  }
  const onPointerUp = () => {
    view.current.dragging = false
  }
  const onKeyDown = (event) => {
    const v = view.current
    const keys = {
      ArrowLeft: () => ((v.sway = 0), (v.yaw -= 0.18)),
      ArrowRight: () => ((v.sway = 0), (v.yaw += 0.18)),
      ArrowUp: () => (v.pitch = clamp(v.pitch - 0.1, -0.6, 0.7)),
      ArrowDown: () => (v.pitch = clamp(v.pitch + 0.1, -0.6, 0.7)),
      '+': () => setZoom(v.zoom + 0.1),
      '=': () => setZoom(v.zoom + 0.1),
      '-': () => setZoom(v.zoom - 0.1),
      0: reset,
    }
    if (keys[event.key]) {
      event.preventDefault()
      keys[event.key]()
      if (reduced) draw(performance.now())
    }
  }

  return (
    <div className="brain" data-compact={compact} ref={wrapRef}>
      <canvas
        ref={canvasRef}
        className="brain-canvas"
        role="img"
        aria-label={`${label} Drag or use arrow keys to rotate, plus and minus to zoom.`}
        tabIndex={0}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        onKeyDown={onKeyDown}
      />
      {controls && (
        <div className="brain-controls" role="group" aria-label="Brain view controls">
          <button type="button" className="round-btn" aria-label="Zoom in" onClick={() => setZoom(view.current.zoom + 0.15)}>
            <Icon name="plus" size={16} />
          </button>
          <button type="button" className="round-btn" aria-label="Zoom out" onClick={() => setZoom(view.current.zoom - 0.15)}>
            <Icon name="minus" size={16} />
          </button>
          <button type="button" className="round-btn" aria-label={`Reset view (zoom ${zoomLabel}%)`} onClick={reset}>
            <Icon name="target" size={16} />
          </button>
        </div>
      )}
    </div>
  )
}
