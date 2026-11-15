// Aerogel k Simulator front end. Builds every row from GET /api/models.
// No physics and no labels here: every word comes from the backend (method files, ui_text.py).
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

let UI = {};             // words from aerosim/core/ui_text.py
let ROWS = [];           // rows and methods from the method files
let SNAP = {};           // last results and totals from the backend
const chosen = {};       // row key -> index of the selected method
const values = {};       // "row/method" -> {input: text typed by the user}
const dirty = new Set(); // rows whose inputs changed since they last ran
const els = {};          // row key -> its DOM element

// ---------------- tooltips ----------------
const tip = document.getElementById("tip");
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function hover(el, html) {
  el.onmouseenter = () => { tip.innerHTML = typeof html === "function" ? html() : html; tip.style.opacity = 1; };
  el.onmousemove = e => {
    tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 8) + "px";
    tip.style.top = Math.min(e.clientY + 14, innerHeight - tip.offsetHeight - 8) + "px";
  };
  el.onmouseleave = () => { tip.style.opacity = 0; };
}

async function api(path, body) {
  const opts = body === undefined ? {} :
    { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const res = await fetch(path, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

// ---------------- sidebar ----------------
function buildRow(row) {
  const last = SNAP.results[row.key];
  chosen[row.key] = Math.max(0, row.methods.findIndex(m => m.key === (last && last.method)));
  const el = document.createElement("div");
  el.className = "row" + (row.key === ROWS[0].key || row.key === ROWS[1].key ? " open" : "");
  el.dataset.row = row.key;
  el.innerHTML = `
    <div class="row-head"><span class="chev">▸</span><span class="dot" style="background:${esc(row.COLOR)}"></span>
      <span class="row-title">${esc(row.ROW)}</span><span class="row-sum"></span></div>
    <div class="row-body">
      <div class="left"><div class="capsule"></div>
        <button class="start">${esc(UI.START)}</button><div class="bar" hidden><i></i></div>
        <div class="result"></div></div>
      <div class="inputs"></div>
    </div>`;
  document.getElementById("rows").appendChild(el);
  els[row.key] = el;
  hover(el.querySelector(".row-title"), esc(row.HELP));
  el.querySelector(".row-head").onclick = () => el.classList.toggle("open");
  const cap = el.querySelector(".capsule");
  row.methods.forEach((m, j) => {
    const b = document.createElement("button");
    b.innerHTML = `${esc(m.NAME)}<span class="lvl">${m.LEVEL === "detailed" ? esc(UI.DETAILED_MARK) : ""}</span>`;
    hover(b, `<b>${esc(m.NAME)}</b> · ${esc(m.LEVEL)}<br>${esc(m.HELP)}<div class="eq">${esc(m.EQUATION)}</div>` +
             `<div class="meta">${esc(m.SOURCE)} · ${esc(m.COST)}</div>`);
    b.onclick = () => { chosen[row.key] = j; renderInputs(row); };
    cap.appendChild(b);
  });
  el.querySelector(".start").onclick = () => run(row);
  hover(el.querySelector(".result"), () => resultTip(row));
  renderInputs(row);
  renderRow(row);
}

function renderInputs(row) {
  const el = els[row.key], m = row.methods[chosen[row.key]];
  el.querySelectorAll(".capsule button").forEach((b, j) => b.classList.toggle("on", j === chosen[row.key]));
  const box = el.querySelector(".inputs");
  box.innerHTML = "";
  const typed = values[`${row.key}/${m.key}`] ||= {};
  const keys = Object.keys(m.INPUTS);
  if (!keys.length) box.innerHTML = `<span class="empty">${esc(UI.NO_INPUTS)}</span>`;
  keys.forEach(key => {
    const v = m.INPUTS[key];
    const lab = document.createElement("label");
    lab.innerHTML = `<span class="st ${esc(v.status)}"></span>${esc(key)}`;
    hover(lab, `<b>${esc(key)}</b> · ${esc(v.status)}<br>${esc(v.help)}` +
               `<div class="meta">${esc(UI.STATUS[v.status] || "")}<br>${esc(v.source)}</div>`);
    const inp = document.createElement("input");
    inp.value = typed[key] ?? v.value;
    inp.dataset.key = key;
    inp.oninput = () => { typed[key] = inp.value; dirty.add(row.key); renderAll(); };
    const unit = document.createElement("span");
    unit.className = "unit";
    unit.textContent = v.unit;
    box.append(lab, inp, unit);
  });
}

function renderRow(row) {
  const el = els[row.key], r = SNAP.results[row.key];
  const m = row.methods.find(x => x.key === r.method) || row.methods[0];
  const sum = el.querySelector(".row-sum");
  sum.textContent = `${m.NAME} · ${r.summary}`;
  sum.classList.toggle("old", dirty.has(row.key) || SNAP.totals.stale.includes(row.ROW));
  const res = el.querySelector(".result");
  if (!res.classList.contains("error")) res.textContent = r.summary;
}

function resultTip(row) {
  const r = SNAP.results[row.key];
  return (r.notes || []).map(esc).join("<br>") + `<div class="meta">${esc(r.method)} · ${esc(r.seconds)} s</div>`;
}

function renderFooter() {
  const t = SNAP.totals, f = document.getElementById("footer");
  const names = [...new Set([...t.stale, ...ROWS.filter(r => dirty.has(r.key)).map(r => r.ROW)])];
  f.classList.toggle("stale", names.length > 0);
  f.innerHTML = `<div class="formula">${esc(t.formula)}</div>` +
    `<div class="line">${esc(t.k_trans_text)}</div><div class="line">${esc(t.k_par_text)}</div>` +
    `<div class="small">${esc(t.anisotropy_text)}</div>` +
    t.notes.map(n => `<div class="small">${esc(n)}</div>`).join("") +
    (names.length ? `<div class="stale-text">${esc(UI.STALE.replace("{rows}", names.join(", ")))}</div>` : "");
}

function renderAll() { ROWS.forEach(renderRow); renderFooter(); }

async function run(row) {
  const el = els[row.key], m = row.methods[chosen[row.key]];
  const btn = el.querySelector(".start"), bar = el.querySelector(".bar"), res = el.querySelector(".result");
  const inputs = {};
  el.querySelectorAll(".inputs input").forEach(inp => { inputs[inp.dataset.key] = Number(inp.value); });
  btn.disabled = true;
  btn.textContent = UI.RUNNING;
  bar.hidden = m.LEVEL !== "detailed";
  try {
    const data = await api(`/api/run/${row.key}/${m.key}`, inputs);
    SNAP.results = data.results;
    SNAP.totals = data.totals;
    dirty.delete(row.key);
    res.classList.remove("error");
    if (row.key === ROWS[0].key) await loadStructure();
    if (data.result.field) showField(data.result.field);
  } catch (err) {
    res.classList.add("error");
    res.textContent = err.message;
  }
  btn.disabled = false;
  btn.textContent = UI.START;
  bar.hidden = true;
  renderAll();
}

// ---------------- 3D view ----------------
const host = document.getElementById("view");
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
host.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
camera.position.set(8, 7, 11);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.6;
scene.add(new THREE.HemisphereLight(0xffffff, 0x445566, 1.6));
const sun = new THREE.DirectionalLight(0xffffff, 1.4);
sun.position.set(5, 10, 6);
scene.add(sun);
const group = new THREE.Group();
group.rotation.x = -Math.PI / 2; // channels (local z) point up
scene.add(group);
const wallMat = new THREE.MeshStandardMaterial({ color: 0xd9dde3, roughness: 0.6 });
const DEPTH = 3;   // scene units along the channels
let box = [1, 1];  // block size in µm, from the backend
let scale = 1;     // scene units per µm
let isWall = () => true; // (fx, fy) in 0..1 of the block → is there wall here? (for the field overlay)

// Flat-to-flat size of the hexagon (pointy-top, flats facing ±x) that passes through (dx, dy).
function hexSize(dx, dy) {
  return 2 * Math.max(Math.abs(dx), Math.abs(0.5 * dx + 0.866 * dy), Math.abs(-0.5 * dx + 0.866 * dy));
}

function hexPoints(r, cx, cy) {
  const p = [];
  for (let k = 0; k < 6; k++) {
    const a = Math.PI / 6 + k * Math.PI / 3;
    p.push(new THREE.Vector2(cx + r * Math.cos(a), cy + r * Math.sin(a)));
  }
  return p;
}

function buildStructure(geo) {
  group.clear();
  showField(null);
  document.getElementById("note").textContent = geo.note || "";
  if (!geo.box) return;
  box = geo.box;
  scale = 5 / box[0];
  const ox = -box[0] / 2, oy = -box[1] / 2;
  if (geo.kind === "cells") {
    const shapes = geo.centres.map(([x, y]) => {
      const s = new THREE.Shape(hexPoints(geo.pitch / Math.sqrt(3) * scale, (x + ox) * scale, (y + oy) * scale));
      s.holes.push(new THREE.Path(hexPoints((geo.pitch - geo.wall) / Math.sqrt(3) * scale, (x + ox) * scale, (y + oy) * scale)));
      return s;
    });
    group.add(new THREE.Mesh(new THREE.ExtrudeGeometry(shapes, { depth: DEPTH, bevelEnabled: false }), wallMat));
    isWall = (fx, fy) => {
      const x = fx * box[0], y = fy * box[1];
      const h = Math.min(...geo.centres.map(([cx, cy]) => hexSize(x - cx, y - cy)));
      return h > geo.pitch - geo.wall;
    };
  } else if (geo.kind === "pixels") {
    const ny = geo.wall.length, nx = geo.wall[0].length, w = box[0] / nx * scale, h = box[1] / ny * scale;
    let count = 0;
    geo.wall.forEach(line => { for (const c of line) if (c === "1") count++; });
    const mesh = new THREE.InstancedMesh(new THREE.BoxGeometry(w, h, DEPTH), wallMat, count);
    const m = new THREE.Matrix4();
    let n = 0;
    geo.wall.forEach((line, j) => {
      for (let i = 0; i < nx; i++) if (line[i] === "1") {
        m.makeTranslation(((i + 0.5) / nx - 0.5) * box[0] * scale, ((j + 0.5) / ny - 0.5) * box[1] * scale, DEPTH / 2);
        mesh.setMatrixAt(n++, m);
      }
    });
    group.add(mesh);
    isWall = (fx, fy) => geo.wall[Math.min(ny - 1, Math.floor(fy * ny))][Math.min(nx - 1, Math.floor(fx * nx))] === "1";
  }
  group.position.y = -DEPTH / 2;
  placeAxes();
}

let fieldMesh = null;
function showField(field) {
  const legend = document.getElementById("legend");
  if (fieldMesh) { group.remove(fieldMesh); fieldMesh = null; }
  legend.hidden = !field;
  if (!field) return;
  const rows = field.values, ny = rows.length, nx = rows[0].length;
  const flat = rows.flat().filter(v => v !== null);
  const lo = Math.min(...flat), hi = Math.max(...flat);
  const data = new Uint8Array(nx * ny * 4);
  const blue = new THREE.Color(0x2c5bd6), white = new THREE.Color(0xf2f2f2), red = new THREE.Color(0xd6452c);
  const c = new THREE.Color();
  rows.forEach((line, j) => line.forEach((v, i) => {
    const f = v === null || hi === lo ? 0.5 : (v - lo) / (hi - lo);
    if (f < 0.5) c.lerpColors(blue, white, f * 2); else c.lerpColors(white, red, f * 2 - 1);
    const alpha = v === null ? 0 : isWall((i + 0.5) / nx, (j + 0.5) / ny) ? 255 : 70;
    data.set([c.r * 255, c.g * 255, c.b * 255, alpha], (j * nx + i) * 4);
  }));
  const tex = new THREE.DataTexture(data, nx, ny);
  tex.needsUpdate = true;
  fieldMesh = new THREE.Mesh(new THREE.PlaneGeometry(box[0] * scale, box[1] * scale),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide }));
  fieldMesh.position.z = DEPTH + 0.01;
  group.add(fieldMesh);
  document.getElementById("legend-name").textContent = field.name;
  document.getElementById("legend-low").textContent = field.low;
  document.getElementById("legend-high").textContent = field.high;
}

// Axis arrows: z = along the channels (k∥), x = across (k⊥, the direction of the 2D runs).
const axisColor = 0x8b94a1;
const axes = [new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1), new THREE.Vector3(), 1, axisColor, 0.18, 0.1),
              new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), new THREE.Vector3(), 1, axisColor, 0.18, 0.1)];
const axisTips = [new THREE.Vector3(), new THREE.Vector3()];
function placeAxes() {
  const x0 = -box[0] * scale / 2 - 0.4, y0 = -box[1] * scale / 2 - 0.4;
  axes[0].position.set(x0, y0, 0); axes[0].setLength(DEPTH + 0.6, 0.18, 0.1);
  axes[1].position.set(x0, y0, 0); axes[1].setLength(box[0] * scale + 0.6, 0.18, 0.1);
  axisTips[0].set(x0, y0, DEPTH + 0.95);
  axisTips[1].set(x0 + box[0] * scale + 0.6, y0 - 0.45, 0);
  axes.forEach(a => group.add(a));
}
function drawAxisLabels() {
  ["axis-par", "axis-trans"].forEach((id, k) => {
    const p = axisTips[k].clone().applyMatrix4(group.matrixWorld).project(camera);
    const el = document.getElementById(id);
    el.style.left = ((p.x + 1) / 2 * host.clientWidth) + "px";
    el.style.top = ((1 - p.y) / 2 * host.clientHeight) + "px";
  });
}

async function loadStructure() { buildStructure(await api("/api/structure")); }

function resize() {
  const w = host.clientWidth, h = host.clientHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
addEventListener("resize", resize);
resize();
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); drawAxisLabels(); });
controls.addEventListener("start", () => { controls.autoRotate = false; });

// ---------------- start ----------------
const data = await api("/api/models");
UI = data.ui;
ROWS = data.rows;
SNAP = data;
document.title = UI.TITLE;
document.getElementById("title").textContent = UI.TITLE;
document.getElementById("badge").textContent = UI.BADGE;
document.getElementById("reminder").textContent = UI.REMINDER;
document.getElementById("axis-par").textContent = UI.AXIS_PAR;
document.getElementById("axis-trans").textContent = UI.AXIS_TRANS;
ROWS.forEach(buildRow);
renderFooter();
await loadStructure();
