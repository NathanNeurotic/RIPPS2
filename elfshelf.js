// The elf shelf: STORAGE's showcase. uOPL's wooden plank (gfx/plank.png, AFL-3.0) as a shelf in front of
// the towers, and on it the RIPPS2 mark ten times over: an elf's felt hat standing brim-down in its own
// pool of blood, one per Colors and More theme. Three show at a time, the way RIPFLOW shows covers: the
// middle one turns to follow the pointer (the nearer the pointer, the quicker it turns), and a touch on
// either neighbour, or Left / Right, brings that one to the middle.
//
// One hat is a link (the `link` element, its data-hat naming which): while it stands in the middle the link
// lies over it, and pointing at it (or focusing it) rings the bell as RIPPS2's memory card icon does in the
// PS2 browser (make_hat_icon.py's keys: four rings dying away, then rest, a 1.5 s loop).
//
// A hat pressed (or brought to the middle by Left / Right) calls onHatPress with its Color Theme's name, and the page
// sends that theme across the towers (pillars.js colorWave): a tap is a burst of colour, a hold keeps it up.
//
// Usage:
//   import { createElfShelf } from "./elfshelf.js";
//   const shelf = createElfShelf(canvas, { interactTarget: heroEl, caption: captionEl, link: anchorEl,
//     onHatPress: (name, clientX, clientY) => handle });   // a hat pressed (its handle's release() when let go)
//   shelf.show(true | false);  shelf.destroy();

import * as THREE from "three";
import { mergeVertices } from "three/addons/utils/BufferGeometryUtils.js";

// one hat per Colors and More theme; the bend is how far the felt flops over toward its bell
const HATS = [
  { name: "Ectoplasm", felt: "#1f8a3c", sheen: "#7fe0a0", bend: 1.55, lean: 0.05, turn: 0.75, seed: 7 },
  { name: "RIPPS2", felt: "#2450c8", sheen: "#9ec0ff", bend: 1.25, lean: -0.08, turn: 0.95, seed: 19 },
  { name: "Ember", felt: "#c2501a", sheen: "#ffc08a", bend: 1.85, lean: 0.12, turn: 0.55, seed: 31 },
  { name: "Blood", felt: "#7c0c18", sheen: "#ff8a96", bend: 1.4, lean: -0.14, turn: 1.1, seed: 43 },
  { name: "Amethyst", felt: "#6a34b8", sheen: "#d8b8ff", bend: 1.7, lean: 0.09, turn: 0.65, seed: 57 },
  { name: "Bone", felt: "#cfc4a8", sheen: "#ffffff", bend: 1.1, lean: -0.05, turn: 0.85, seed: 71 },
  // build 114's four; Moonlight's felt glows faintly, as its theme's lift does
  { name: "Tangerine", felt: "#e0700f", sheen: "#ffc27a", bend: 1.6, lean: 0.07, turn: 0.7, seed: 83 },
  { name: "Flamingo", felt: "#e2508f", sheen: "#ffc6de", bend: 1.3, lean: -0.1, turn: 1.0, seed: 97 },
  { name: "Turquoise", felt: "#11a596", sheen: "#8ff5ea", bend: 1.75, lean: 0.1, turn: 0.6, seed: 109 },
  { name: "Moonlight", felt: "#c3cbe6", sheen: "#ffffff", glow: "#a9bcff", bend: 1.2, lean: -0.06, turn: 0.9, seed: 127 },
];
const SLOT_X = 4.1;       // world units between the shelf's three places
const SIDE_SCALE = 0.78;  // the neighbours stand a little smaller, as RIPFLOW's side covers do
const SLIDE_S = 0.55;     // a step along the shelf

// the memory card icon's ring, in the icon's frames (60 a second): the curl swings about the hat's own axis,
// more toward the tip, by RING_SWING radians at full weight; the bell swings a little past the felt holding it
const RING_KEYS = [[0, 0], [6, 1], [12, 0], [18, -1], [24, 0], [30, 0.6], [36, 0], [42, -0.35], [48, 0], [90, 0]];
const RING_REST = 48, RING_LOOP = 90, RING_SWING = 0.75, BELL_SWING = Math.pow(1.3, 1.3);
function ringAt(f) {
  for (let i = 1; i < RING_KEYS.length; i++) {
    const [t1, v1] = RING_KEYS[i];
    if (f <= t1) { const [t0, v0] = RING_KEYS[i - 1], u = (f - t0) / (t1 - t0); return v0 + (v1 - v0) * u * u * (3 - 2 * u); }
  }
  return 0;
}

export function createElfShelf(canvas, { interactTarget = canvas, caption = null, link = null, onHatPress = null } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);

  // ---- a dark room to reflect: the blood stays near black and only its highlights show ----
  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = (() => {
    const room = new THREE.Scene();
    room.background = new THREE.Color("#000000");
    const panel = (w, h, col, pos) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: col, side: THREE.DoubleSide }));
      m.position.copy(pos); m.lookAt(0, 0, 0); room.add(m);
    };
    panel(6, 4, new THREE.Color(5, 4.2, 3.4), new THREE.Vector3(-6, 9, 5));
    panel(0.6, 7, new THREE.Color("#2f6bff").multiplyScalar(4), new THREE.Vector3(8, 4, -6));
    panel(7, 0.22, new THREE.Color(1.6, 1.5, 1.5), new THREE.Vector3(-6, 6, -7.5));
    panel(3, 0.4, new THREE.Color(2.5, 2.5, 2.8), new THREE.Vector3(2, 7, 8));
    return pmrem.fromScene(room, 0.02).texture;
  })();

  // ---- small helpers ----
  const rng = (seed) => { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; };
  function canvasTex(w, h, draw, srgb = true) {
    const c = document.createElement("canvas"); c.width = w; c.height = h;
    draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c);
    if (srgb) t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4;
    return t;
  }

  // ---- the shelf: uOPL's plank, its grain on top and its lit edge on the front ----
  const shelf = new THREE.Group();
  scene.add(shelf);
  // The plank is short (1024 x 256): its grain (rows 0-185) and its front edge (rows 186-212) are cut
  // apart and each tiled, mirrored, at its own proportions along a shelf wider than any screen; never
  // stretched. The camera looks down on it steeply, as uOPL shows it, so the grain reads deep.
  const SHELF_W = 40, SHELF_D = 4.6, SHELF_T = 0.36;
  const plankImg = new Image();
  plankImg.onload = () => {
    const cut = (y0, h) => {
      const c = document.createElement("canvas"); c.width = plankImg.width; c.height = h;
      c.getContext("2d").drawImage(plankImg, 0, y0, plankImg.width, h, 0, 0, plankImg.width, h);
      const t = new THREE.CanvasTexture(c);
      t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
      t.wrapS = THREE.MirroredRepeatWrapping; t.wrapT = THREE.ClampToEdgeWrapping;
      return t;
    };
    const grain = cut(0, 185), edge = cut(186, 26);
    grain.repeat.set(SHELF_W / (SHELF_D * plankImg.width / 185), 1);   // one tile is as wide as the grain is deep allows
    edge.repeat.set(SHELF_W / (SHELF_T * plankImg.width / 26), 1);
    const wood = (map) => new THREE.MeshStandardMaterial({ map, roughness: 0.55, metalness: 0, envMap: env, envMapIntensity: 0.35 });
    const dark = new THREE.MeshStandardMaterial({ color: "#3a1c0c", roughness: 0.8 });
    // box faces: +x, -x, +y (top), -y, +z (front), -z
    const box = new THREE.Mesh(new THREE.BoxGeometry(SHELF_W, SHELF_T, SHELF_D), [dark, dark, wood(grain), dark, wood(edge), dark]);
    box.position.set(0, -SHELF_T / 2, 0.3);
    box.receiveShadow = true;
    shelf.add(box);
  };
  plankImg.src = "assets/plank.png";

  // ---- blood ----
  function blobShape(r, lobes, jag, rnd, cx = 0, cy = 0) {
    const sh = new THREE.Shape(), N = 140, ph = [rnd() * 6, rnd() * 6, rnd() * 6];
    for (let i = 0; i <= N; i++) {
      const a = (i / N) * Math.PI * 2;
      const k = 1 + 0.14 * Math.sin(a * lobes + ph[0]) + 0.09 * Math.sin(a * (lobes * 2 + 1) + ph[1]) + 0.05 * Math.sin(a * 7 + ph[2] * 2)
        + jag * Math.sin(a * 11 + ph[2]) + 0.4 * jag * Math.sin(a * 17 + ph[0]);
      const x = cx + Math.cos(a) * r * k * 1.15, y = cy + Math.sin(a) * r * k * 0.95;
      i ? sh.lineTo(x, y) : sh.moveTo(x, y);
    }
    return sh;
  }
  const bloodMat = new THREE.MeshPhysicalMaterial({
    color: "#560009", roughness: 0.035, clearcoat: 1, clearcoatRoughness: 0.02, sheen: 0.25, sheenColor: new THREE.Color("#c0101c"),
    envMap: env, envMapIntensity: 1.1, ior: 1.36,
  });
  function puddle(shape, depth) {
    const g = new THREE.ExtrudeGeometry(shape, { depth: depth * 0.2, bevelEnabled: true, bevelThickness: depth * 0.8, bevelSize: depth * 3, bevelSegments: 8, curveSegments: 48 });
    const m = new THREE.Mesh(g, bloodMat);
    m.rotation.x = -Math.PI / 2; m.receiveShadow = true;
    return m;
  }

  // ---- a hat: felt cone by lathe, its upper part flopped over toward a gold bell, a fur brim ----
  const feltBump = canvasTex(256, 256, (c, w, h) => {
    const r = rng(3); c.fillStyle = "#808080"; c.fillRect(0, 0, w, h);
    for (let i = 0; i < 20000; i++) { const v = r() < 0.5 ? 255 : 0; c.fillStyle = `rgba(${v},${v},${v},${0.4 * r()})`; c.fillRect(r() * w, r() * h, 1, 1); }
  }, false);
  const furMap = canvasTex(512, 128, (c, w, h) => {
    const r = rng(5); c.fillStyle = "#ece4d2"; c.fillRect(0, 0, w, h);
    for (let i = 0; i < 12000; i++) { const x = r() * w, y = r() * h; c.strokeStyle = r() < 0.5 ? "rgba(255,255,255,0.3)" : "rgba(120,100,80,0.2)"; c.beginPath(); c.moveTo(x, y); c.lineTo(x + r() * 3 - 1.5, y + 3 + r() * 5); c.stroke(); }
    for (let x = 0; x < w; x++) { const top = h * (0.45 + 0.15 * Math.sin(x * 0.04) * Math.cos(x * 0.013)); const g = c.createLinearGradient(0, top, 0, h);
      g.addColorStop(0, "rgba(110,0,10,0)"); g.addColorStop(0.25, "rgba(110,0,10,0.85)"); g.addColorStop(1, "rgba(60,0,4,1)"); c.fillStyle = g; c.fillRect(x, top, 1, h - top); }
  });
  const bellMat = new THREE.MeshPhysicalMaterial({ color: "#d4a640", metalness: 1, roughness: 0.22, envMap: env, envMapIntensity: 1.4 });
  const furGeo = (() => {
    const g = new THREE.TorusGeometry(0.64, 0.13, 24, 120), p = g.attributes.position, v = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const n = 1 + 0.03 * (Math.sin(v.x * 23) * Math.cos(v.y * 19) + 0.6 * Math.sin(v.z * 29)); p.setXYZ(i, v.x * (1 + (n - 1) * 0.3), v.y * n, v.z * (1 + (n - 1) * 0.3)); }
    g.computeVertexNormals(); return g;
  })();

  // the felt's flop as a vertex-shader bend about (R, uBendY): above uBendY the cone curls toward +x by
  // uBend radians over its length, normals turned with it; then the curl swings about the hat's axis by
  // uSwing radians at the tip (the icon's ring), less toward the bend
  function bendFelt(mat, u) {
    mat.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, u);
      sh.vertexShader = sh.vertexShader
        .replace("#include <common>", "#include <common>\nuniform float uBend, uBendY, uLen, uSwing;")
        .replace("#include <beginnormal_vertex>", `#include <beginnormal_vertex>
          if (position.y > uBendY) { float bR = (uLen - uBendY) / max(0.05, uBend); float th = (position.y - uBendY) / bR;
            float c = cos(th), s = sin(th); objectNormal = vec3(c * objectNormal.x - s * objectNormal.y, s * objectNormal.x + c * objectNormal.y, objectNormal.z);
            float sw = uSwing * pow((position.y - uBendY) / (uLen - uBendY), 1.3); float cw = cos(sw), sn = sin(sw);
            objectNormal = vec3(cw * objectNormal.x - sn * objectNormal.z, objectNormal.y, sn * objectNormal.x + cw * objectNormal.z); }`)
        .replace("#include <begin_vertex>", `#include <begin_vertex>
          if (position.y > uBendY) { float bR = (uLen - uBendY) / max(0.05, uBend); float th = (position.y - uBendY) / bR; float r = bR - position.x;
            transformed.x = bR - r * cos(th); transformed.y = uBendY + r * sin(th);
            float sw = uSwing * pow((position.y - uBendY) / (uLen - uBendY), 1.3); float cw = cos(sw), sn = sin(sw);
            transformed.xz = vec2(cw * transformed.x - sn * transformed.z, sn * transformed.x + cw * transformed.z); }`);
    };
  }

  function makeHat(def) {
    const rnd = rng(def.seed);
    const feltMap = canvasTex(512, 512, (c, w, h) => {
      c.fillStyle = def.felt; c.fillRect(0, 0, w, h);
      for (let i = 0; i < 9000; i++) { const x = rnd() * w, y = rnd() * h, a = rnd() * Math.PI, l = 2 + rnd() * 6;
        c.strokeStyle = rnd() < 0.5 ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.1)"; c.beginPath(); c.moveTo(x, y); c.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); c.stroke(); }
      for (let x = 0; x < w; x += 2) { // blood wicking up from the brim (v 0, the canvas top)
        const reach = h * (0.28 + 0.15 * Math.sin(x * 0.026 + def.seed) * Math.sin(x * 0.062) + 0.05 * rnd());
        const g = c.createLinearGradient(0, 0, 0, reach);
        g.addColorStop(0, "rgba(50,0,4,0.97)"); g.addColorStop(0.6, "rgba(80,0,8,0.78)"); g.addColorStop(1, "rgba(80,0,8,0)");
        c.fillStyle = g; c.fillRect(x, 0, 2, reach);
      }
    });
    feltMap.flipY = false;

    // The cone is built straight; the flop toward the bell is done live in the vertex shader (bendFelt),
    // so the pointer's up / down lifts or drops the tip on a spring instead of tipping the hat over.
    const L = 2.3, BEND_Y = 0.42 * L;
    const prof = [];
    for (let i = 0; i <= 40; i++) { const t = i / 40; prof.push(new THREE.Vector2(0.62 * Math.pow(1 - t, 1.15) + 0.012, t * L)); }
    let geo = mergeVertices(new THREE.LatheGeometry(prof, 72));
    const p = geo.attributes.position, v = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) {
      v.fromBufferAttribute(p, i);
      const t = v.y / L, ang = Math.atan2(v.z, v.x);
      // felt is never perfect: soft dents, and a crinkle where the cone gathers into the fur
      let k = 1 + 0.025 * Math.sin(v.y * 9 + v.z * 7) * Math.sin(ang * 5);
      if (t < 0.14) k += 0.07 * (1 - t / 0.14) * Math.sin(ang * 13 + Math.sin(ang * 3) * 2);
      v.x *= k; v.z *= k;
      p.setXYZ(i, v.x, v.y, v.z);
    }
    geo.computeVertexNormals();
    const bendU = { uBend: { value: def.bend }, uBendY: { value: BEND_Y }, uLen: { value: L }, uSwing: { value: 0 } };
    const hat = new THREE.Group();
    const felt = new THREE.MeshPhysicalMaterial({ shadowSide: THREE.FrontSide, map: feltMap, bumpMap: feltBump, bumpScale: 0.5, roughness: 0.92, sheen: 0.6, sheenRoughness: 0.7,
      sheenColor: new THREE.Color(def.sheen), side: THREE.DoubleSide, envMap: env, envMapIntensity: 0.4 });
    if (def.glow) { felt.emissive.set(def.glow); felt.emissiveMap = feltMap; felt.emissiveIntensity = 0.22; } // the blood stays dark
    bendFelt(felt, bendU);
    const cone = new THREE.Mesh(geo, felt); cone.castShadow = true; hat.add(cone);
    const depth = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking });
    bendFelt(depth, bendU);
    cone.customDepthMaterial = depth;   // its shadow bends with it
    const fur = new THREE.Mesh(furGeo, new THREE.MeshStandardMaterial({ map: furMap, roughness: 1, bumpMap: feltBump, bumpScale: 3 }));
    fur.rotation.x = Math.PI / 2; fur.position.y = 0.05; fur.castShadow = true; hat.add(fur);
    const bell = new THREE.Mesh(new THREE.SphereGeometry(0.15, 32, 20), bellMat);
    bell.castShadow = true; hat.add(bell);
    const placeBell = (a, sw = 0) => { // at the bent tip, wherever the spring (and the ring) has the felt
      const R = (L - BEND_Y) / Math.max(0.05, a), x = R - R * Math.cos(a) + 0.04, b = sw * BELL_SWING;
      bell.position.set(x * Math.cos(b), BEND_Y + R * Math.sin(a) - 0.1, x * Math.sin(b));
    };
    placeBell(def.bend);
    // the hat's outline in its own space, for the link laid over it: brim, bend, the curl and the bell
    const rim = [], curl = [], marks = [];
    for (let j = 0; j < 8; j++) { const a = (j / 8) * Math.PI * 2;
      rim.push(new THREE.Vector3(Math.cos(a) * 0.8, -0.05, Math.sin(a) * 0.8), new THREE.Vector3(Math.cos(a) * 0.8, 0.22, Math.sin(a) * 0.8),
        new THREE.Vector3(Math.cos(a) * 0.45, BEND_Y, Math.sin(a) * 0.45)); }
    for (let j = 0; j < 16; j++) curl.push(new THREE.Vector3());
    const outline = (a, sw) => {
      const R = (L - BEND_Y) / Math.max(0.05, a);
      for (let j = 0; j < 4; j++) {
        const th = a * (j + 1) / 4, k = Math.pow((j + 1) / 4, 1.3) * sw, cx = R - R * Math.cos(th), cy = BEND_Y + R * Math.sin(th);
        for (let q = 0; q < 4; q++) {
          const x = cx + (q & 1 ? 0.3 : -0.3), z = q & 2 ? 0.3 : -0.3;
          curl[j * 4 + q].set(x * Math.cos(k) - z * Math.sin(k), cy + (q & 2 ? 0.3 : -0.3), x * Math.sin(k) + z * Math.cos(k));
        }
      }
      marks.length = 0; marks.push(...rim, ...curl, bell.position);
      return marks;
    };

    // the hat stands in its own pool, sunk to half the fur; the pool keeps still while the hat turns
    const holder = new THREE.Group();
    const spin = new THREE.Group();   // yaw (follows the pointer on the middle hat)
    spin.add(hat);
    // upright on the wood, its fur in the blood: the brim's underside rests on the plank, never through it
    hat.rotation.set(0, def.turn, 0);
    hat.scale.setScalar(1.25);
    hat.position.y = 0.105;
    const pool = puddle(blobShape(1.55, 2, 0.02, rnd), 0.03);
    holder.add(pool);
    for (let i = 0; i < 4; i++) { // a few drops close by, each hat its own
      const a = rnd() * Math.PI * 2, d = 1.95 + rnd() * 0.35, r = 0.04 + rnd() * 0.08;
      holder.add(puddle(blobShape(r, 2, 0.02, rnd, Math.cos(a) * d, Math.sin(a) * d * 0.6), 0.012 + r * 0.05));
    }
    holder.add(spin);
    // the bell's spring: bend (rad) and its speed
    holder.userData = { spin, hat, yaw: 0, bendU, placeBell, outline, base: def.bend, bend: def.bend, bendV: 0 };
    holder.traverse((o) => { if (o.isMesh) o.userData.holder = holder; });
    return holder;
  }

  const hats = HATS.map((def) => { const h = makeHat(def); scene.add(h); return h; });

  // ---- light ----
  const key = new THREE.SpotLight("#ffd9b0", 260, 40, 0.55, 0.6, 1.6);
  key.position.set(-5, 10, 7); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024); key.shadow.bias = -0.0006; key.shadow.normalBias = 0.04; key.shadow.radius = 5;
  scene.add(key, key.target);
  const rim = new THREE.SpotLight("#3c6ef0", 150, 40, 0.3, 0.6, 1.6);
  rim.position.set(6, 6.5, -8); rim.target.position.set(0, 1.4, 0); scene.add(rim, rim.target); // on the felt, off the wood
  scene.add(new THREE.HemisphereLight("#28324a", "#0a0405", 0.45));

  // ---- the carousel ----
  const n = hats.length;
  // which hat is in the middle (pos eases after target): RIPPS2's blue on arrival, the mark's own colour
  const start = Math.max(0, HATS.findIndex((h) => h.name === "RIPPS2"));
  let target = start, pos = start;
  const wrap = (d) => ((d % n) + n + n / 2) % n - n / 2;   // the shortest way round
  function step(dir) { target += dir; if (caption) setCaption(); }
  function setCaption() {
    const k = ((Math.round(target) % n) + n) % n;
    sayCaption(HATS[k].name);
  }
  function sayCaption(text) {
    caption.textContent = text;
    caption.animate([{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "none" }], { duration: 380, easing: "cubic-bezier(.2,.7,.3,1)" });
  }
  if (caption) setCaption();

  // ---- the linked hat: pointed at or focused, it rings; a ring always plays out to its rest ----
  const linkIdx = link ? HATS.findIndex((h) => h.name === (link.dataset.hat || "RIPPS2")) : -1;
  let linkOn = false, ringHover = false, ringF = RING_REST;
  const ringStart = () => {
    if (!ringHover && ringF >= RING_REST) ringF = 0;
    if (!ringHover && caption && link.dataset.caption) sayCaption(link.dataset.caption);
    ringHover = true;
  };
  const ringStop = () => { if (ringHover && caption) setCaption(); ringHover = false; };
  if (linkIdx >= 0) {
    link.style.display = "none";
    link.addEventListener("pointerenter", ringStart);
    link.addEventListener("pointerleave", ringStop);
    link.addEventListener("focus", ringStart);
    link.addEventListener("blur", ringStop);
  }
  const lp = new THREE.Vector3();
  function placeLink() {
    const h = hats[linkIdx], on = visible && Math.abs(wrap(linkIdx - pos)) < 0.3;
    if (on !== linkOn) {
      linkOn = on;
      link.style.display = on ? "block" : "none";
      if (!on) { if (document.activeElement === link) link.blur(); ringStop(); }
    }
    if (!on) return;
    h.updateMatrixWorld(true);
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const p of h.userData.outline(h.userData.bend, h.userData.bendU.uSwing.value)) {
      lp.copy(p); h.userData.hat.localToWorld(lp).project(camera);
      x0 = Math.min(x0, lp.x); x1 = Math.max(x1, lp.x); y0 = Math.min(y0, lp.y); y1 = Math.max(y1, lp.y);
    }
    const w = canvas.clientWidth, ht = canvas.clientHeight;
    const left = (x0 + 1) / 2 * w, top = (1 - y1) / 2 * ht;
    link.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px)`;
    link.style.width = ((x1 - x0) / 2 * w).toFixed(1) + "px";
    link.style.height = ((y1 - y0) / 2 * ht).toFixed(1) + "px";
  }

  // ---- pointer ----
  const pointer = new THREE.Vector2(0, 0);
  let pointerIn = false;
  const ray = new THREE.Raycaster();
  function toNdc(e) {
    const r = canvas.getBoundingClientRect();
    pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  }
  const onMove = (e) => { toNdc(e); pointerIn = true; };
  const onLeave = () => { pointerIn = false; };
  // the hat being held down: its theme stays up on the towers until it is let go
  let press = null;
  const pressHat = (k, x, y) => { press?.release(); press = onHatPress?.(HATS[k].name, x, y) || null; };
  const onUp = () => { press?.release(); press = null; };
  const middleIdx = () => ((Math.round(target) % n) + n) % n;
  const onDown = (e) => {
    if (!visible) return;
    if (linkOn && e.target === link) { // the link opens on click
      e.stopImmediatePropagation(); hats[linkIdx].userData.bendV -= 4.5; pressHat(linkIdx, e.clientX, e.clientY); return;
    }
    toNdc(e);
    ray.setFromCamera(pointer, camera);
    const hit = ray.intersectObjects(hats, true)[0];
    if (!hit) {
      // anywhere on the shelf beside the middle hat counts as touching its neighbour
      const plank = ray.intersectObject(shelf, true)[0];
      if (plank && Math.abs(plank.point.x) > slotX * 0.45) {
        e.stopImmediatePropagation(); step(Math.sign(plank.point.x)); pressHat(middleIdx(), e.clientX, e.clientY);
      }
      return;
    }
    const holder = hit.object.userData.holder, k = hats.indexOf(holder);
    const off = wrap(k - pos);
    e.stopImmediatePropagation(); // a hat, not the towers' blast
    if (Math.abs(off) < 0.5) holder.userData.bendV -= 4.5;  // the middle one's bell jumps
    else step(Math.sign(off));
    pressHat(k, e.clientX, e.clientY);
  };
  const midScreen = new THREE.Vector3();
  const onKey = (e) => {
    if (!visible || (e.key !== "ArrowLeft" && e.key !== "ArrowRight") || e.repeat) return;
    step(e.key === "ArrowLeft" ? -1 : 1);
    // the new middle hat's theme bursts from where it stands
    const r = canvas.getBoundingClientRect();
    midScreen.set(0, 1.4, 0.4).project(camera);
    onHatPress?.(HATS[middleIdx()].name, r.left + (midScreen.x + 1) / 2 * r.width, r.top + (1 - midScreen.y) / 2 * r.height)?.release();
  };
  interactTarget.addEventListener("pointermove", onMove);
  interactTarget.addEventListener("pointerleave", onLeave);
  interactTarget.addEventListener("pointerdown", onDown, { capture: true });
  window.addEventListener("keydown", onKey);
  window.addEventListener("pointerup", onUp);
  window.addEventListener("pointercancel", onUp);
  window.addEventListener("blur", onUp);

  // ---- size ----
  let slotX = SLOT_X, sideScale = SIDE_SCALE;
  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // keep the three places in view on a narrow screen: step back a little, and close the places up
    const fit = Math.min(1.8, Math.max(1, 1.25 / camera.aspect));
    camera.position.set(0, 6.4 * fit, 11.8 * fit);   // looking down on the plank, as uOPL shows it
    const halfW = camera.position.length() * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.aspect;
    slotX = Math.min(SLOT_X, halfW * 0.64);
    sideScale = slotX < SLOT_X ? SIDE_SCALE * Math.max(0.75, slotX / SLOT_X) : SIDE_SCALE;
    camera.lookAt(0, 0.75, 0.3);
    camera.updateProjectionMatrix();
  }
  const ro = new ResizeObserver(resize); ro.observe(canvas); resize();

  // ---- frame ----
  let visible = false, raf = 0, last = performance.now();
  const hatScreen = new THREE.Vector3();
  function frame(now) {
    raf = requestAnimationFrame(frame);
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    const t = now / 1000;
    pos += (target - pos) * (1 - Math.exp(-dt / (SLIDE_S / 4)));
    if (ringHover) ringF = (ringF + dt * 60) % RING_LOOP;
    else if (ringF < RING_REST) ringF = Math.min(RING_REST, ringF + dt * 60);

    hats.forEach((h, k) => {
      const off = wrap(k - pos), a = Math.abs(off);
      const ud = h.userData;
      h.visible = a < 2.2;
      h.position.set(off * slotX, 0, -Math.min(a, 1) * 1.1 + 0.4);
      const s = (a < 1 ? 1 - (1 - sideScale) * a : sideScale) * Math.min(1, Math.max(0, 2.2 - a) / 0.8);
      h.scale.setScalar(Math.max(0.001, s));

      let goal;
      if (a < 0.5 && pointerIn) {
        // the middle hat looks toward the pointer; the nearer the pointer is to it, the quicker it turns
        hatScreen.set(h.position.x, 1.4, h.position.z).project(camera);
        const dx = pointer.x - hatScreen.x, dy = pointer.y - hatScreen.y;
        const near = Math.max(0, 1 - Math.hypot(dx, dy * 0.8) / 1.1);
        goal = Math.max(-1.3, Math.min(1.3, dx * 1.6));
        ud.yaw += (goal - ud.yaw) * (1 - Math.exp(-dt * (0.8 + 9 * near * near)));
        // up / down is the bell's: the pointer above lifts the tip, below lets it droop
        ud.bendGoal = ud.base + Math.max(-0.7, Math.min(0.6, -dy * 0.9)) * near;
      } else {
        goal = 0.25 * Math.sin(t * 0.6 + k * 1.7); // the others idle
        ud.yaw += (goal - ud.yaw) * (1 - Math.exp(-dt * 1.5));
        ud.bendGoal = ud.base + 0.06 * Math.sin(t * 0.9 + k * 2.3); // their bells breathing
      }
      // turning flings the bell: the spring takes the yaw's speed as a kick
      const yawV = (ud.yaw - (ud.lastYaw ?? ud.yaw)) / Math.max(dt, 1e-3); ud.lastYaw = ud.yaw;
      ud.bendV += (-(ud.bend - ud.bendGoal) * 42 - ud.bendV * 5.5 + Math.abs(yawV) * 0.9) * dt;
      ud.bend = Math.max(0.15, Math.min(2.4, ud.bend + ud.bendV * dt));
      ud.bendU.uBend.value = ud.bend;
      const sw = k === linkIdx ? RING_SWING * ringAt(ringF) : 0;
      ud.bendU.uSwing.value = sw;
      ud.placeBell(ud.bend, sw);
      ud.spin.rotation.y = ud.yaw;
    });
    if (linkIdx >= 0) placeLink();
    if (visible) renderer.render(scene, camera);
  }
  raf = requestAnimationFrame(frame);

  return {
    show(on) {
      visible = on;
      canvas.dataset.shelf = on ? "on" : "off";
      if (caption) caption.dataset.shelf = canvas.dataset.shelf;
    },
    step,
    destroy() {
      cancelAnimationFrame(raf); ro.disconnect();
      interactTarget.removeEventListener("pointermove", onMove);
      interactTarget.removeEventListener("pointerleave", onLeave);
      interactTarget.removeEventListener("pointerdown", onDown, { capture: true });
      window.removeEventListener("keydown", onKey);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
      window.removeEventListener("blur", onUp);
      onUp();
      if (linkIdx >= 0) {
        link.removeEventListener("pointerenter", ringStart); link.removeEventListener("pointerleave", ringStop);
        link.removeEventListener("focus", ringStart); link.removeEventListener("blur", ringStop);
      }
      renderer.dispose();
    },
  };
}
