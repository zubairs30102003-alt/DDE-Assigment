/* global window */
// Light client-side "agent" engine for the Bremen Scaler Index.
// - Loads companies.json (1,083 firms)
// - Routes via Claude (window.claude.complete)
// - text → Claude w/ retrieved snippets (cheap RAG by keyword)
// - code → Claude proposes a plan, JS executes the aggregation
// - visual → returns a small chart spec we render with vanilla SVG

window.BSI = (function () {
  let DATA = null;
  let META = null;

  async function load() {
    if (DATA) return DATA;
    if (window.__COMPANIES) {
      DATA = window.__COMPANIES;
    } else {
      const r = await fetch("companies.json");
      DATA = await r.json();
    }
    const n = DATA.length;
    const scalers = DATA.filter(d => d.Scaler_2024 === 1).length;
    META = { n, scalers, rate: scalers / n };
    return DATA;
  }

  // ── primitive aggregations ──────────────────────────────────────
  function groupRate(field, minN = 5) {
    const m = {};
    for (const r of DATA) {
      const k = r[field]; if (!k || k === "Not found") continue;
      m[k] = m[k] || { n: 0, s: 0 };
      m[k].n++; m[k].s += (r.Scaler_2024 || 0);
    }
    return Object.entries(m)
      .filter(([, v]) => v.n >= minN)
      .map(([k, v]) => ({ k, n: v.n, rate: v.s / v.n }))
      .sort((a, b) => b.rate - a.rate);
  }

  function topScalers(limit = 10) {
    return [...DATA]
      .filter(r => r.Scaler_2024 === 1 && r["aagr 2024"])
      .sort((a, b) => (b["aagr 2024"] || 0) - (a["aagr 2024"] || 0))
      .slice(0, limit);
  }

  function search(keyword, limit = 6) {
    const k = keyword.toLowerCase();
    return DATA.filter(r =>
      (r["Company name Latin alphabet"] || "").toLowerCase().includes(k) ||
      (r.Industry || "").toLowerCase().includes(k)
    ).slice(0, limit);
  }

  // ── router ──────────────────────────────────────────────────────
  async function route(q) {
    if (!window.claude || !window.claude.complete) {
      // Standalone fallback: keyword routing
      const ql = q.toLowerCase();
      if (/(plot|chart|graph|visual|show|draw)/.test(ql)) return "visual";
      if (/(top|fastest|how many|count|rate|average|group|by sector|legal form|b2b|b2c|age|size)/.test(ql)) return "code";
      return "text";
    }
    const sys = `Classify the user question as exactly one word: "text", "code", or "visual".
- "code" = aggregations, counts, comparisons, group-by, top-N, statistics
- "visual" = explicit chart/plot/graph request
- "text" = factual look-ups about specific companies, definitions, summaries
Reply with ONLY the word.`;
    const out = await window.claude.complete({
      messages: [
        { role: "user", content: `${sys}\n\nQuestion: "${q}"\n\nClassification:` },
      ],
    });
    const t = (out || "").toLowerCase().trim().replace(/[^a-z]/g, "");
    return ["text", "code", "visual"].includes(t) ? t : "text";
  }

  // ── code agent (heuristic; falls back to Claude prose) ─────────
  function codeAgent(q) {
    const ql = q.toLowerCase();
    let result = null;
    let plan = "";

    const has = (...needles) => needles.some(n => ql.includes(n));

    if (has("legal form", "gmbh", "ag ", "kg ", "legal")) {
      plan = `df.groupby("Legal_Form")["Scaler_2024"].agg(["mean","count"])`;
      result = { kind: "rate-table", title: "Scaling rate by legal form", rows: groupRate("Legal_Form") };
    } else if (has("b2b", "b2c", "customer")) {
      plan = `df.groupby("B2B_or_B2C")["Scaler_2024"].agg(["mean","count"])`;
      result = { kind: "rate-table", title: "Scaling rate by customer model", rows: groupRate("B2B_or_B2C") };
    } else if (has("sector", "industry", "nace")) {
      plan = `df.groupby("NACE_Section")["Scaler_2024"].agg(["mean","count"])`;
      result = { kind: "rate-table", title: "Scaling rate by NACE section", rows: groupRate("NACE_Section") };
    } else if (has("top", "fastest", "highest growth", "best growers")) {
      plan = `df[df.Scaler_2024==1].nlargest(10, "aagr 2024")`;
      result = { kind: "top-table", title: "Top 10 scalers by AAGR", rows: topScalers(10) };
    } else if (has("age", "old", "young")) {
      plan = `df.groupby(age_bucket)["Scaler_2024"].agg(["mean","count"])`;
      const buckets = { "0–10y": [0, 10], "10–25y": [10, 25], "25–50y": [25, 50], "50–100y": [50, 100], "100y+": [100, 999] };
      const m = {};
      for (const r of DATA) {
        const a = r.Company_Age; if (!a) continue;
        for (const [k, [lo, hi]] of Object.entries(buckets)) {
          if (a >= lo && a < hi) { m[k] = m[k] || { n: 0, s: 0 }; m[k].n++; m[k].s += r.Scaler_2024 || 0; break; }
        }
      }
      const order = ["0–10y", "10–25y", "25–50y", "50–100y", "100y+"];
      result = { kind: "rate-table", title: "Scaling rate by company age", rows: order.map(k => ({ k, n: m[k].n, rate: m[k].s / m[k].n })) };
    } else if (has("how many scalers", "scaler count", "number of scalers")) {
      plan = `df["Scaler_2024"].sum()`;
      result = { kind: "scalar", value: META.scalers, label: "scalers in the dataset" };
    } else if (has("overall rate", "scaling rate", "rate overall")) {
      plan = `df["Scaler_2024"].mean()`;
      result = { kind: "scalar", value: (META.rate * 100).toFixed(2) + "%", label: "overall scaling rate" };
    }
    return { plan, result };
  }

  // ── visual agent ────────────────────────────────────────────────
  function visualAgent(q) {
    const ql = q.toLowerCase();
    if (ql.includes("legal")) {
      return { title: "Scaling rate by legal form", rows: groupRate("Legal_Form") };
    }
    if (ql.includes("b2b") || ql.includes("b2c") || ql.includes("customer")) {
      return { title: "Scaling rate by customer model", rows: groupRate("B2B_or_B2C") };
    }
    if (ql.includes("age")) {
      const buckets = { "0–10y": [0, 10], "10–25y": [10, 25], "25–50y": [25, 50], "50–100y": [50, 100], "100y+": [100, 999] };
      const m = {};
      for (const r of DATA) {
        const a = r.Company_Age; if (!a) continue;
        for (const [k, [lo, hi]] of Object.entries(buckets)) {
          if (a >= lo && a < hi) { m[k] = m[k] || { n: 0, s: 0 }; m[k].n++; m[k].s += r.Scaler_2024 || 0; break; }
        }
      }
      const order = ["0–10y", "10–25y", "25–50y", "50–100y", "100y+"];
      return { title: "Scaling rate by company age", rows: order.map(k => ({ k, n: m[k].n, rate: m[k].s / m[k].n })) };
    }
    // default: by sector
    return { title: "Scaling rate by NACE sector", rows: groupRate("NACE_Section") };
  }

  // ── offline text fallback ───────────────────────────────────────
  function offlineTextAnswer(q, hits) {
    if (hits.length) {
      const r = hits[0];
      const tag = r.Scaler_2024 ? "qualifies as a Scaler" : "does not qualify as a Scaler";
      return `${r["Company name Latin alphabet"]} (${r.Legal_Form || "—"}, ${r.NACE_Section || "—"}) ${tag} in our 2024 sample. Sector: ${r.Industry || "—"}. Age: ${r.Company_Age || "—"} yrs.`;
    }
    return `Across 1,083 Bremen firms, 11.8% scaled (2019–2024). Hospitality leads at 32.5%; AGs scale best by legal form (18.2%); B2B firms outpace B2C (12.2% vs 6.7%). Use a more specific keyword to look up a single company.`;
  }

  // ── text agent (RAG-lite using Claude) ─────────────────────────
  async function textAgent(q) {
    // Cheap "retrieval": keyword filter over name + industry
    const tokens = q.toLowerCase().split(/\s+/).filter(t => t.length > 3);
    let hits = [];
    for (const r of DATA) {
      const blob = (r["Company name Latin alphabet"] + " " + (r.Industry || "")).toLowerCase();
      const score = tokens.reduce((s, t) => s + (blob.includes(t) ? 1 : 0), 0);
      if (score > 0) hits.push({ r, score });
    }
    hits.sort((a, b) => b.score - a.score);
    hits = hits.slice(0, 8).map(h => h.r);

    const ctx = hits.length
      ? hits.map(r => `• ${r["Company name Latin alphabet"]} | ${r.Legal_Form} | ${r.NACE_Section} | ${r.Industry} | scaler=${r.Scaler_2024}`).join("\n")
      : "(no specific firms matched — answer using dataset statistics)";

    const overall = `Dataset stats: ${META.n} Bremen firms (>10 employees), ${META.scalers} scalers (${(META.rate*100).toFixed(1)}%). Top sector: Hospitality (32.5%). Best legal form: AG (18.2%). B2B 12.2% vs B2C 6.7%.`;

    const prompt = `You are a Bremen company-data analyst for the WHU DDE project. Answer concisely (2–4 sentences). Use ONLY the context.

${overall}

Retrieved rows:
${ctx}

Question: ${q}
Answer:`;
    if (!window.claude || !window.claude.complete) {
      return { answer: offlineTextAnswer(q, hits), cited: hits };
    }
    const out = await window.claude.complete(prompt);
    return { answer: out, cited: hits };
  }

  // ── editor ─────────────────────────────────────────────────────
  async function editor(draft) {
    if (!draft || draft.length < 60) return draft;
    if (!window.claude || !window.claude.complete) return draft;
    const out = await window.claude.complete(
      `Polish this analytical answer to 1-3 tight sentences. Keep all numbers exact. No filler. Output only the polished text.\n\n${draft}`
    );
    return out || draft;
  }

  return { load, route, codeAgent, visualAgent, textAgent, editor, search, get meta() { return META; } };
})();
