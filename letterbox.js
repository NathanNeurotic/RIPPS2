// Portrait phones: the site as a player. Held upright, a phone gets the page letterboxed at the top of its screen
// (only the camera's and the curved corners' inset above it), laid out as on a landscape screen and scaled to fit,
// with the chin underneath: an arrow up to the player, a glowing note to pinch to zoom or turn the phone, and a switch
// between a 16:9 and a 4:3 box. The page runs inside the player (an iframe of itself, which lays out landscape), so the
// page around it draws nothing of its own; turning the phone sideways goes back to the page itself, where the player was.
//
// Usage, first thing in a page's module:
//   import { letterbox } from "./letterbox.js";
//   if (!letterbox()) { ...start the page... }
// letterbox() is true when it has taken the page over. ?letterbox=1 forces it (a desktop check).

const PORTRAIT_PHONE = "(orientation: portrait) and (pointer: coarse) and (max-width: 700px)";
const SHAPES = { "16:9": [960, 540], "4:3": [720, 540] }; // the landscape page the player lays out
const KEY = "ripps2.letterbox";

const CSS = `
html.lb-embedded .hero { touch-action: manipulation; }
html.lb-embedded canvas#orbs { touch-action: pan-y pinch-zoom; }
html.lb-embedded .ripps2-foot { display: none; }
html.letterboxed, html.letterboxed body { background: #03040b; min-height: 100%; }
html.letterboxed body > :not(.lb) { display: none !important; }
.lb { min-height: 100vh; min-height: 100dvh; box-sizing: border-box; display: flex; flex-direction: column;
  padding: env(safe-area-inset-top) env(safe-area-inset-right) 0 env(safe-area-inset-left); color: #dce7ff;
  background: radial-gradient(120% 60% at 50% 0%, rgba(20, 44, 120, .35), transparent 70%); }
.lb-screen { position: relative; width: 100%; overflow: hidden; background: #000; flex: none;
  box-shadow: 0 1px 0 rgba(120, 170, 255, .35), 0 10px 40px rgba(40, 90, 255, .25); transition: aspect-ratio .35s ease; }
.lb-player { position: absolute; left: 0; top: 0; border: 0; transform-origin: 0 0; background: #03040b; }
.lb-chin { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 22px; padding: 26px 16px 64px;
  text-align: center; }
.lb-arrow { width: 34px; height: 22px; color: #9cc2ff; filter: drop-shadow(0 0 6px rgba(110, 160, 255, .9));
  animation: lb-bob 1.6s ease-in-out infinite; }
@keyframes lb-bob { 50% { transform: translateY(-7px); } }
.lb-note { margin: 0; font-family: "Master", "Albert Sans", system-ui, sans-serif; text-transform: uppercase;
  letter-spacing: .08em; line-height: 1.5; font-size: clamp(18px, 5.8vw, 28px); color: #f4f8ff;
  text-shadow: 0 0 6px rgba(200, 222, 255, .9), 0 0 22px rgba(110, 160, 255, .8); }
.lb-note span { display: block; font-size: .78em; color: #c8d8ff; opacity: .85; }
.lb-shape { display: flex; align-items: center; gap: 12px; font-family: "Master", "Albert Sans", system-ui, sans-serif;
  font-size: 15px; letter-spacing: .08em; }
.lb-shape b { font-weight: 400; opacity: .45; transition: opacity .3s, text-shadow .3s; }
.lb-shape b.on { opacity: 1; text-shadow: 0 0 10px rgba(110, 160, 255, .8); }
.lb-switch { position: relative; width: 56px; height: 30px; border-radius: 15px; border: 1px solid rgba(140, 180, 255, .55);
  background: rgba(10, 26, 82, .8); padding: 0; cursor: pointer; -webkit-tap-highlight-color: transparent;
  box-shadow: inset 0 0 10px rgba(47, 107, 255, .35); }
.lb-switch::after { content: ""; position: absolute; top: 3px; left: 3px; width: 22px; height: 22px; border-radius: 50%;
  background: #dce7ff; box-shadow: 0 0 10px rgba(110, 160, 255, .9); transition: transform .3s cubic-bezier(.2, .7, .3, 1); }
.lb-switch[aria-checked="true"]::after { transform: translateX(26px); }
.lb-switch:focus-visible { outline: 2px solid rgba(170, 205, 255, .8); outline-offset: 3px; }
@media (prefers-reduced-motion: reduce) { .lb-arrow { animation: none; } .lb-screen, .lb-switch::after { transition: none; } }
`;

function addStyle() {
  const s = document.createElement("style");
  s.textContent = CSS;
  document.head.append(s);
}

function stored() {
  try { return localStorage.getItem(KEY); } catch { return null; }
}

function store(v) {
  try { localStorage.setItem(KEY, v); } catch { /* private mode: the choice lasts the visit */ }
}

export function letterbox() {
  if (window.top !== window) { // the player itself: the page, with pinch-zoom let through to the phone
    addStyle();
    document.documentElement.classList.add("lb-embedded");
    return false;
  }
  const mq = matchMedia(PORTRAIT_PHONE);
  const forced = new URLSearchParams(location.search).get("letterbox") === "1";
  if (!mq.matches && !forced) {
    mq.addEventListener("change", (e) => { if (e.matches) location.reload(); }); // turned upright: the player
    return false;
  }

  addStyle();
  document.documentElement.classList.add("letterboxed");
  // the camera's and the curved corners' inset is the only space above the player
  const vp = document.querySelector('meta[name="viewport"]');
  if (vp && !/viewport-fit/.test(vp.content)) vp.content += ", viewport-fit=cover";

  let shape = SHAPES[stored()] ? stored() : "16:9";
  const box = document.createElement("div");
  box.className = "lb";
  box.innerHTML = `
    <div class="lb-screen"><iframe class="lb-player" title="RIPPS2" allow="gamepad; fullscreen"></iframe></div>
    <div class="lb-chin">
      <svg class="lb-arrow" viewBox="0 0 34 22" aria-hidden="true"><path d="M3 19 17 5l14 14" fill="none"
        stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <p class="lb-note">Pinch to zoom<span>or turn your phone sideways</span></p>
      <div class="lb-shape"><b data-s="4:3">4:3</b><button class="lb-switch" role="switch"
        aria-label="Widescreen (16:9) box"></button><b data-s="16:9">16:9</b></div>
    </div>
    <p class="ripps2-foot">RIPPS2 (vision interactive mock-up)</p>`;
  document.body.prepend(box);

  const screen = box.querySelector(".lb-screen"), frame = box.querySelector(".lb-player");
  const sw = box.querySelector(".lb-switch"), labels = box.querySelectorAll(".lb-shape b");
  const fit = () => {
    const [w, h] = SHAPES[shape];
    screen.style.aspectRatio = `${w} / ${h}`;
    frame.style.width = w + "px";
    frame.style.height = h + "px";
    frame.style.transform = `scale(${screen.clientWidth / w})`;
    sw.setAttribute("aria-checked", String(shape === "16:9"));
    labels.forEach((b) => b.classList.toggle("on", b.dataset.s === shape));
  };
  sw.addEventListener("click", () => { shape = shape === "16:9" ? "4:3" : "16:9"; store(shape); fit(); });
  labels.forEach((b) => b.addEventListener("click", () => { shape = b.dataset.s; store(shape); fit(); }));
  new ResizeObserver(fit).observe(screen);
  fit();
  const src = new URL(location.href);
  src.searchParams.delete("letterbox");
  frame.src = src.href;

  // turned sideways: the page itself, on whichever page the player was showing
  mq.addEventListener("change", (e) => {
    if (e.matches || forced) return;
    let here = src.href;
    try { here = frame.contentWindow.location.href; } catch { /* the player left the site */ }
    history.replaceState(null, "", here);
    location.reload();
  });
  return true;
}
