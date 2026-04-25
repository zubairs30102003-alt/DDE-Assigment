/* global window, BSI, DDE_DATA */
// Wires up the Bremen Scaler Index live site.

const D = window.DDE_DATA;

// ── CONFIG ────────────────────────────────────────────────────────
// Replace with your deployed Streamlit URL once it's live.
const STREAMLIT_URL = ""; // e.g. "https://bremen-scaler-index.streamlit.app"

// ── FINDINGS CARDS ────────────────────────────────────────────────
const findings = [
  { span: 5, rank: "01", stat: "32.5%", h: "Hospitality is the unlikely champion.",
    body: "Bremen's hotels, food-service and tourism operators scale at almost 3× the city average — the highest rate of any NACE section.",
    chart: () => miniBars(D.sectors.slice(0, 6), { maxKey: "rate" }) },
  { span: 4, rank: "02", stat: "18.2%", h: "Going AG pays.",
    body: "The 11 Aktiengesellschaften scale at 18.2%. KGs scale at 3.2% — a six-fold gap.",
    chart: () => miniBars(D.legalForm) },
  { span: 3, rank: "03", stat: "2×", h: "B2B beats B2C.",
    body: "B2B firms scale at 12.2%, B2C at 6.7%. Selling to other businesses still wins.",
    chart: () => b2bSplit() },
  { span: 4, rank: "04", stat: "18.2%", h: "Younger firms scale faster.",
    body: "Firms under 10 years old scale at 18.2%; centenarians at 3.6%. Age is destiny — until you reset the company.",
    chart: () => miniBars(D.age) },
  { span: 5, rank: "05", stat: "25–49", h: "There's a sweet spot in headcount.",
    body: "The 25–49 employee band scales most often (16.7%). Below 25, you're scrappy; above 50, momentum carries you.",
    chart: () => miniBars(D.size, { labelSuffix: " emp" }) },
  { span: 3, rank: "—", stat: "5", h: "Gazelles are vanishingly rare.",
    body: "Only five firms cleared the 20% AAGR / 3-yr bar. Most growth is steady, not explosive.",
    dark: true },
];

function miniBars(rows, opts = {}) {
  const max = Math.max(...rows.map(r => r.rate));
  return rows.map(r => `
    <div style="display:grid; grid-template-columns:90px 1fr 50px; gap:8px; align-items:center; margin-bottom:5px;">
      <span style="font-size:11px; color:var(--ink-2);">${r.k || r.name}${opts.labelSuffix||""}</span>
      <div class="ed-bar-track"><div class="ed-bar-fill" style="width:${(r.rate/max)*100}%"></div></div>
      <span class="ed-mono" style="font-size:10.5px; text-align:right;">${r.rate.toFixed(1)}%</span>
    </div>`).join("");
}

function b2bSplit() {
  const colors = ["var(--whu-blue)", "var(--ink)", "var(--whu-red)"];
  return `<div style="display:flex; gap:0; height:90px; align-items:flex-end;">
    ${D.b2b.map((b,i)=>`<div style="flex:1; text-align:center;">
      <div class="ed-mono" style="font-size:11px; margin-bottom:4px;">${b.rate}%</div>
      <div style="background:${colors[i]}; height:${(b.rate/13)*100}%; margin-right:${i<2?4:0}px;"></div>
      <div style="font-size:10.5px; margin-top:6px; color:var(--ink-2);">${b.k}</div>
    </div>`).join("")}
  </div>`;
}

function renderFindings() {
  const grid = document.getElementById("findingsGrid");
  grid.innerHTML = findings.map(f => `
    <div style="grid-column: span ${f.span}; padding:24px; border:1px solid var(--line);
                background:${f.dark?"var(--ink)":"var(--paper)"}; color:${f.dark?"var(--paper)":"var(--ink)"};
                display:flex; flex-direction:column; min-height:340px;">
      <div class="ed-mono" style="font-size:11px; letter-spacing:0.12em;
           color:${f.dark?"rgba(250,250,247,0.5)":"var(--ink-3)"};">FINDING ${f.rank}</div>
      <div class="ed-display" style="font-size:64px; line-height:0.95; margin-top:16px;
           color:${f.dark?"var(--paper)":"var(--whu-blue)"};">${f.stat}</div>
      <div style="font-size:18px; line-height:1.3; margin-top:14px; font-weight:500;">${f.h}</div>
      <div style="font-size:13px; line-height:1.55; margin-top:10px; flex:1;
           color:${f.dark?"rgba(250,250,247,0.7)":"var(--ink-2)"};">${f.body}</div>
      ${f.chart ? `<div style="margin-top:18px;">${f.chart()}</div>` : ""}
    </div>`).join("");
}

// ── AGENTS ROW ────────────────────────────────────────────────────
const AGENTS = [
  { id: "01", name: "Router", role: "Classifies intent", note: "text · code · visual", glyph: "⌥" },
  { id: "02", name: "Text Agent", role: "RAG over 1,083 firm cards", note: "FAISS + MiniLM", glyph: "⊕" },
  { id: "03", name: "Code Agent", role: "Live pandas in a sandbox", note: "exec → result", glyph: "⌘" },
  { id: "04", name: "Visual Agent", role: "Plotly figures, WHU-styled", note: "px / go", glyph: "◫" },
  { id: "05", name: "Editor", role: "Polishes the final answer", note: "tone + brevity", glyph: "✎" },
];
function renderAgents() {
  const row = document.getElementById("agentRow");
  row.innerHTML = AGENTS.map((a, i) => `
    <div style="padding:24px; background:var(--paper); border:1px solid var(--line);
                ${i<4?"border-right:none;":""} position:relative; min-height:200px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span class="ed-mono" style="font-size:11px; color:var(--ink-3); letter-spacing:0.12em;">AGENT ${a.id}</span>
        <span style="font-size:22px; color:var(--whu-blue);">${a.glyph}</span>
      </div>
      <div class="ed-display" style="font-size:28px; margin-top:20px;">${a.name}</div>
      <div style="font-size:13px; color:var(--ink-2); margin-top:8px;">${a.role}</div>
      <div class="ed-mono" style="font-size:10.5px; color:var(--ink-3); margin-top:14px; letter-spacing:0.05em;">${a.note}</div>
    </div>`).join("");
}

// ── METHOD ────────────────────────────────────────────────────────
const METHOD = [
  { n: "01", t: "Source", body: "Orbis: every Bremen-registered firm.", val: "1,083" },
  { n: "02", t: "Filter", body: "Keep firms whose peak headcount cleared 10 employees.", val: ">10 emp" },
  { n: "03", t: "Enrich", body: "Anthropic Claude Haiku + Serper to extract industry, B2B/B2C, key activities.", val: "27 cols" },
  { n: "04", t: "Label", body: "OECD scaler & gazelle definitions, applied to 5-yr employment series.", val: "AAGR" },
  { n: "05", t: "Model", body: "Logistic regression on legal form, sector, B2B/B2C, age.", val: "L1" },
];
function renderMethod() {
  const wrap = document.getElementById("methodSteps");
  wrap.innerHTML = METHOD.map((s, i) => `
    <div style="padding:24px; border-top:2px solid var(--ink); ${i<4?"border-right:1px solid var(--line);":""}">
      <div class="ed-mono" style="font-size:11px; color:var(--ink-3); letter-spacing:0.12em;">${s.n}</div>
      <div style="font-size:22px; margin-top:14px; font-family:'Instrument Serif', serif;">${s.t}</div>
      <div style="font-size:13px; line-height:1.5; color:var(--ink-2); margin-top:8px; min-height:60px;">${s.body}</div>
      <div class="ed-mono" style="font-size:12px; color:var(--whu-red); margin-top:10px;">→ ${s.val}</div>
    </div>`).join("");
}

// ── CHAT ──────────────────────────────────────────────────────────
const log = document.getElementById("chatLog");
const scratch = document.getElementById("scratchpad");
const input = document.getElementById("chatInput");
const form = document.getElementById("chatForm");
const datasetChip = document.getElementById("datasetChip");

function addMsg(who, html, tag) {
  const el = document.createElement("div");
  el.className = "msg " + (who === "user" ? "user" : "agent");
  el.innerHTML = `<div class="msg-tag">${tag || (who === "user" ? "YOU" : "AGENT")}</div><div class="msg-body">${html}</div>`;
  log.appendChild(el);
  log.scrollTop = log.scrollHeight;
  return el;
}

function setStatus(name, state) {
  document.querySelectorAll(".agent-pip").forEach(p => {
    if (p.dataset.a === name) {
      p.classList.remove("active", "done");
      if (state) p.classList.add(state);
    }
  });
}
function resetStatus() { document.querySelectorAll(".agent-pip").forEach(p => p.classList.remove("active","done")); }

function pushScratch(text, color) {
  if (scratch.firstElementChild && scratch.firstElementChild.style.color === "var(--ink-3)") {
    scratch.innerHTML = "";
  }
  const t = (performance.now() / 1000).toFixed(2).padStart(6, "0");
  const div = document.createElement("div");
  div.className = "scratch-line";
  div.innerHTML = `<span style="color:var(--ink-3);">${t}</span> <span style="color:${color||"var(--whu-blue)"}">${text}</span>`;
  scratch.appendChild(div);
  scratch.scrollTop = scratch.scrollHeight;
}

function renderRateTable(t) {
  const max = Math.max(...t.rows.map(r => r.rate));
  return `<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:10px;">${t.title.toUpperCase()}</div>
  ${t.rows.map(r => `
    <div style="display:grid; grid-template-columns:130px 1fr 70px; gap:10px; align-items:center; padding:5px 0; border-top:1px dashed var(--line-2);">
      <span style="font-size:12px;">${r.k}</span>
      <div class="ed-bar-track" style="height:10px;"><div class="ed-bar-fill" style="width:${(r.rate/max)*100}%; height:10px;"></div></div>
      <span class="ed-mono" style="font-size:11px; text-align:right;">${(r.rate*100).toFixed(1)}% <span style="color:var(--ink-3);">n=${r.n}</span></span>
    </div>`).join("")}`;
}

function renderTopTable(t) {
  return `<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:10px;">${t.title.toUpperCase()}</div>
    ${t.rows.map((r, i) => `
      <div style="display:grid; grid-template-columns:24px 1fr 70px; gap:10px; padding:6px 0; border-top:1px dashed var(--line-2); font-size:12px;">
        <span class="ed-mono" style="color:var(--ink-3);">${String(i+1).padStart(2,"0")}</span>
        <span>${r["Company name Latin alphabet"]} <span style="color:var(--ink-3); font-size:11px;">· ${r.Legal_Form || ""}</span></span>
        <span class="ed-mono" style="color:var(--whu-red); text-align:right;">+${(r["aagr 2024"]||0).toFixed(1)}%</span>
      </div>`).join("")}`;
}

function renderVisual(v) {
  // Simple SVG bar chart, sorted desc
  const rows = [...v.rows].sort((a,b)=>b.rate-a.rate);
  const max = Math.max(...rows.map(r => r.rate));
  const W = 540, BH = 22, GAP = 8, padL = 110;
  const H = rows.length * (BH + GAP) + 40;
  const bars = rows.map((r, i) => {
    const y = 24 + i*(BH+GAP);
    const w = ((r.rate/max) * (W - padL - 60));
    return `
      <text x="${padL-8}" y="${y+BH/2+4}" text-anchor="end" font-size="11" fill="#3B4566" font-family="Inter, sans-serif">${r.k}</text>
      <rect x="${padL}" y="${y}" width="${w}" height="${BH}" fill="${r.rate*100>11.82?'#2C4592':'#6B7493'}"/>
      <text x="${padL+w+6}" y="${y+BH/2+4}" font-size="10.5" fill="#0E1530" font-family="JetBrains Mono, monospace">${(r.rate*100).toFixed(1)}%</text>`;
  }).join("");
  return `<div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:6px;">FIG · ${v.title.toUpperCase()}</div>
    <svg viewBox="0 0 ${W} ${H}" style="width:100%; max-width:${W}px;">${bars}</svg>`;
}

function renderScalar(s) {
  return `<div style="text-align:center; padding:12px;">
    <div class="ed-display" style="font-size:64px; color:var(--whu-blue); line-height:1;">${s.value}</div>
    <div style="font-size:13px; color:var(--ink-2); margin-top:8px;">${s.label}</div>
  </div>`;
}

async function handleQuestion(q) {
  resetStatus();
  scratch.innerHTML = "";
  addMsg("user", escapeHTML(q));
  const thinking = addMsg("agent", `<span style="color:var(--ink-3);">Routing…</span>`, "ROUTER");

  setStatus("router", "active");
  pushScratch("Router · classifying intent");

  let route;
  try { route = await BSI.route(q); }
  catch { route = "text"; }

  pushScratch(`Router → ${route}`, "var(--whu-red)");
  setStatus("router", "done");

  thinking.querySelector(".msg-tag").textContent = route.toUpperCase();

  try {
    if (route === "code") {
      setStatus("code", "active");
      pushScratch("Code · planning aggregation");
      const { plan, result } = BSI.codeAgent(q);
      pushScratch("Code · " + (plan || "fallback"), "var(--ink-2)");
      if (result && result.kind === "rate-table") {
        thinking.querySelector(".msg-body").innerHTML = renderRateTable(result);
      } else if (result && result.kind === "top-table") {
        thinking.querySelector(".msg-body").innerHTML = renderTopTable(result);
      } else if (result && result.kind === "scalar") {
        thinking.querySelector(".msg-body").innerHTML = renderScalar(result);
      } else {
        // fallback: ask Claude
        pushScratch("Code · no template hit, deferring to text", "var(--ink-3)");
        const r = await BSI.textAgent(q);
        thinking.querySelector(".msg-body").innerHTML = escapeHTML(r.answer);
      }
      setStatus("code", "done");
    } else if (route === "visual") {
      setStatus("visual", "active");
      pushScratch("Visual · building figure");
      const v = BSI.visualAgent(q);
      thinking.querySelector(".msg-body").innerHTML = renderVisual(v);
      setStatus("visual", "done");
    } else {
      setStatus("text", "active");
      pushScratch("Text · retrieving rows");
      const r = await BSI.textAgent(q);
      pushScratch(`Text · ${r.cited.length} rows cited`, "var(--ink-2)");
      setStatus("text", "done");

      setStatus("editor", "active");
      pushScratch("Editor · polishing");
      const polished = await BSI.editor(r.answer);
      setStatus("editor", "done");

      let html = escapeHTML(polished || r.answer);
      if (r.cited.length) {
        html += `<div style="margin-top:12px; padding-top:10px; border-top:1px dashed var(--line-2); font-family:'JetBrains Mono', monospace; font-size:10.5px; color:var(--ink-3);">
          <div style="margin-bottom:4px; letter-spacing:0.1em;">CITED · ${r.cited.length}</div>
          ${r.cited.slice(0,4).map(c => `<div>· ${escapeHTML(c["Company name Latin alphabet"])}</div>`).join("")}
        </div>`;
      }
      thinking.querySelector(".msg-body").innerHTML = html;
    }
    pushScratch("done.", "var(--pos)");
  } catch (e) {
    thinking.querySelector(".msg-body").innerHTML = `<span style="color:var(--whu-red);">Error: ${escapeHTML(e.message || String(e))}</span>`;
    pushScratch("error · " + (e.message || e), "var(--whu-red)");
  }
}

function escapeHTML(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));
}

// ── BOOT ──────────────────────────────────────────────────────────
async function boot() {
  renderFindings();
  renderAgents();
  renderMethod();

  // Streamlit slot toggling
  if (STREAMLIT_URL) {
    document.getElementById("stOpen").href = STREAMLIT_URL;
    const wrap = document.getElementById("streamlitFrameWrap");
    document.getElementById("streamlitFrame").src = STREAMLIT_URL;
    wrap.style.display = "block";
  } else {
    document.getElementById("stOpen").addEventListener("click", e => {
      e.preventDefault();
      alert("Set STREAMLIT_URL in site.js to your deployed Streamlit Cloud URL.");
    });
  }

  // chat
  await BSI.load();
  datasetChip.textContent = `${BSI.meta.n.toLocaleString()} firms loaded`;

  form.addEventListener("submit", e => {
    e.preventDefault();
    const q = input.value.trim(); if (!q) return;
    input.value = ""; handleQuestion(q);
  });
  document.querySelectorAll(".suggest").forEach(b => {
    b.addEventListener("click", () => { input.value = b.textContent; form.requestSubmit(); });
  });

  // smooth scroll
  document.querySelectorAll('#navLinks a').forEach(a => {
    a.addEventListener("click", e => {
      e.preventDefault();
      const t = document.querySelector(a.getAttribute("href"));
      if (t) t.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

document.addEventListener("DOMContentLoaded", boot);
