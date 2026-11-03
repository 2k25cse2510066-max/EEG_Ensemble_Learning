// Procedural, stylised brain: two hemispheres with folded surface, a cerebellum and a brain stem.
// Built once as a flat point cloud. This is an illustration, not anatomy or EEG data.

function mulberry32(seed) {
  let a = seed
  return () => {
    a |= 0
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

// Domain-warped sine fields give winding, maze-like ridges, a decent stand-in for cortical folds. Range about -1..1.
const fold = (x, y, z) =>
  0.5 * Math.sin(11 * x + 3.4 * Math.sin(7 * z + 2.2 * y) + 0.6) +
  0.5 * Math.sin(10 * y + 3 * Math.sin(8 * x - 3.1 * z) + 1.9)

// Uniform random points on the unit sphere (no visible lattice, unlike a Fibonacci spiral).
function fibonacci(count, rand) {
  const out = []
  for (let i = 0; i < count; i += 1) {
    const y = rand() * 2 - 1
    const t = rand() * Math.PI * 2
    const r = Math.sqrt(1 - y * y)
    out.push([Math.cos(t) * r, y, Math.sin(t) * r])
  }
  return out
}

// Hotspot direction (unit vector) on the left outer surface; fixed, because the model has no spatial output.
export const HOTSPOT = (() => {
  const v = [-0.9, 0.34, -0.12]
  const n = Math.hypot(...v)
  return v.map((c) => c / n)
})()

export function buildBrain() {
  const rand = mulberry32(7)
  const pts = []
  const push = (x, y, z, nx, ny, nz, kind, ridge = 0) => {
    const n = Math.hypot(nx, ny, nz) || 1
    pts.push({ x, y, z, nx: nx / n, ny: ny / n, nz: nz / n, kind, ridge, tw: rand() * Math.PI * 2 })
  }

  // Cerebrum: one deformed ellipsoid, split into two hemispheres by a fissure.
  for (const [ux, uy, uz] of fibonacci(11000, rand)) {
    const f = fold(ux, uy, uz)
    let r = 1 + 0.065 * f
    let x = ux * 0.62 * r
    let y = uy * 0.5 * r
    let z = uz * 0.74 * r
    if (y < 0) y *= 0.72 // flatter underside
    if (y < -0.1 && Math.abs(x) > 0.24 && z > -0.35 && z < 0.2) {
      y -= 0.05 * (1 - Math.abs(z + 0.05) * 2.2) // temporal lobe bulge
    }
    const side = x >= 0 ? 1 : -1
    x += side * 0.035 // fissure
    if (y > 0.18) y -= 0.1 * Math.exp(-Math.pow(x / 0.09, 2)) // dip along the midline
    push(x, y, z, ux, uy * 1.2, uz, 'cerebrum', f)
  }

  // Cerebellum: tucked under the back, with fine ridges.
  for (const [ux, uy, uz] of fibonacci(2100, rand)) {
    if (uy > 0.55) continue
    const ridge = 1 + 0.05 * Math.sin(38 * uy + 2 * ux)
    push(ux * 0.34 * ridge, -0.34 + uy * 0.17 * ridge, 0.46 + uz * 0.21 * ridge, ux, uy, uz, 'cerebellum', Math.sin(38 * uy))
  }

  // Brain stem.
  for (let i = 0; i < 520; i += 1) {
    const t = rand()
    const a = rand() * Math.PI * 2
    const rad = 0.075 * (1 - t * 0.25)
    push(Math.cos(a) * rad, -0.3 - t * 0.34, 0.12 + t * 0.1 + Math.sin(a) * rad, Math.cos(a), 0, Math.sin(a), 'stem')
  }
  return pts
}

// Pairs of points that make a few "signal" arcs travelling out from the hotspot.
export function buildArcs(points) {
  const rand = mulberry32(21)
  const cerebrum = points.filter((p) => p.kind === 'cerebrum')
  const origin = {
    x: HOTSPOT[0] * 0.62,
    y: HOTSPOT[1] * 0.5,
    z: HOTSPOT[2] * 0.74,
  }
  const arcs = []
  for (let i = 0; i < 9; i += 1) {
    const target = cerebrum[Math.floor(rand() * cerebrum.length)]
    const mid = {
      x: (origin.x + target.x) / 2 * 1.18,
      y: (origin.y + target.y) / 2 * 1.18 + 0.05,
      z: (origin.z + target.z) / 2 * 1.18,
    }
    arcs.push({ a: origin, m: mid, b: target, phase: rand(), speed: 0.00018 + rand() * 0.00016 })
  }
  return arcs
}
