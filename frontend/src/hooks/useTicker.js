import { useEffect, useRef } from 'react'

// One shared requestAnimationFrame loop for every canvas on the page.
const callbacks = new Set()
let frame = 0
let last = 0

function loop(now) {
  const dt = Math.min(64, now - (last || now))
  last = now
  callbacks.forEach((cb) => cb(now, dt))
  frame = callbacks.size ? requestAnimationFrame(loop) : 0
  if (!frame) last = 0
}

export function prefersReducedMotion() {
  return typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

// Calls `callback(now, dt)` every frame while mounted. Does nothing for reduced-motion users.
export function useTicker(callback, enabled = true) {
  const saved = useRef(callback)
  useEffect(() => {
    saved.current = callback
  })
  useEffect(() => {
    if (!enabled || prefersReducedMotion()) return undefined
    const cb = (now, dt) => saved.current(now, dt)
    callbacks.add(cb)
    if (!frame) frame = requestAnimationFrame(loop)
    return () => {
      callbacks.delete(cb)
    }
  }, [enabled])
}
