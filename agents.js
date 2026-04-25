/* global window */
// Bremen Scaler Index — client-side agent engine
// Supports: optional Anthropic API key (entered in sidebar) for real LLM answers
// Falls back to a rich heuristic engine when no key is present.

window.BSI = (function () {
  let DATA = null;
  let META = null;

  // ── load data ───────────────────────────────────────────────────
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

  // ── Claude API via browser fetch ────────────────────────────────
  async function callClaude(prompt, systemMsg) {
    const key = window.ANTHROPIC_KEY || "";
    if (!key) return null;
    try {
      const body = {
        model: "claude-haiku-4-5-20251001",
        max_tokens: 512,
        messages: [{ role: "user", content: prompt }]
      };
      if (systemMsg) body.system = systemMsg;
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "x-api-key": key,
          "anthropic-version": "2023-06-01",
          "anthropic-dangerous-direct-browser-access": "true",
          "content-type": "application/json"
        },
        body: JSON.stringify(body)
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error?.message || `HTTP ${res.status}`);
      }
      const data = await res.json();
      return data.content?.[0]?.text || null;
    } catch (e) {
      console.warn("Claude API error:", e.message);
      return null;
    }
  }

  function hasKey() { return !!(window.ANTHROPIC_KEY || "").trim(); }

  // ── aggregation helpers ─────────────────────────────────────────
  function groupRate(field, minN = 5, filterFn) {
    const m = {};
    const rows = filterFn ? DATA.filter(filterFn) : DATA;
    for (const r of rows) {
      const k = r[field]; if (!k || k === "Not found") continue;
      m[k] = m[k] || { n: 0, s: 0 };
      m[k].n++; m[k].s += (r.Scaler_2024 || 0);
    }
    return Object.entries(m)
      .filter(([, v]) => v.n >= minN)
      .map(([k, v]) => ({ k, n: v.n, rate: v.s / v.n }))
      .sort((a, b) => b.rate - a.rate);
  }

  function countByField(field, filterFn) {
    const m = {};
    const rows = filterFn ? DATA.filter(filterFn) : DATA;
    for (const r of rows) {
      const k = r[field] || "Unknown"; if (k === "Not found") continue;
      m[k] = (m[k] || 0) + 1;
    }
    return Object.entries(m).map(([k, n]) => ({ k, n })).sort((a, b) => b.n - a.n);
  }

  function ageBuckets(filterFn) {
    const buckets = { "0–10 yrs": [0,10], "10–25 yrs": [10,25], "25–50 yrs": [25,50], "50–100 yrs": [50,100], "100+ yrs": [100,999] };
    const m = {};
    const rows = filterFn ? DATA.filter(filterFn) : DATA;
    for (const r of rows) {
      const a = r.Company_Age; if (!a) continue;
      for (const [k,[lo,hi]] of Object.entries(buckets)) {
        if (a >= lo && a < hi) { m[k] = m[k] || {n:0,s:0}; m[k].n++; m[k].s += r.Scaler_2024||0; break; }
      }
    }
    return Object.keys(buckets).filter(k=>m[k]).map(k => ({ k, n: m[k].n, rate: m[k].s/m[k].n }));
  }

  function topScalers(limit = 10, filterFn) {
    return [...DATA]
      .filter(r => r.Scaler_2024 === 1 && r["aagr 2024"] && (!filterFn || filterFn(r)))
      .sort((a, b) => (b["aagr 2024"]||0) - (a["aagr 2024"]||0))
      .slice(0, limit);
  }

  // ── NACE section → readable name ────────────────────────────────
  const NACE_NAMES = {
    A:"Agriculture",B:"Mining",C:"Manufacturing",D:"Energy",E:"Water & Waste",
    F:"Construction",G:"Wholesale & Retail",H:"Transport",I:"Hospitality",
    J:"Information & Comms",K:"Finance",L:"Real Estate",M:"Professional Services",
    N:"Admin Services",O:"Public Admin",P:"Education",Q:"Health & Social",
    R:"Arts & Recreation",S:"Other Services",T:"Households",U:"Extraterritorial"
  };

  // Sector keyword map → NACE codes
  const SECTOR_KEYWORDS = {
    hospitality: ["I"], "hotel": ["I"], "restaurant": ["I"], "food": ["I"], "coffee": ["I"], "cafe": ["I"], "catering": ["I"],
    "real estate": ["L"], "property": ["L"], "rental": ["L"],
    "education": ["P"], "school": ["P"], "university": ["P"], "training": ["P"],
    "health": ["Q"], "medical": ["Q"], "hospital": ["Q"], "social": ["Q"],
    "manufacturing": ["C"], "production": ["C"], "industrial": ["C"],
    "construction": ["F"], "building": ["F"], "engineering": ["F"],
    "transport": ["H"], "logistics": ["H"], "shipping": ["H"], "freight": ["H"],
    "technology": ["J"], "software": ["J"], "it ": ["J"], "digital": ["J"], "tech": ["J"],
    "finance": ["K"], "bank": ["K"], "insurance": ["K"], "financial": ["K"],
    "retail": ["G"], "wholesale": ["G"], "trade": ["G"], "shop": ["G"], "store": ["G"],
    "arts": ["R"], "culture": ["R"], "sport": ["R"], "recreation": ["R"],
    "professional": ["M"], "consulting": ["M"], "law": ["M"], "accounting": ["M"],
    "admin": ["N"], "security": ["N"], "cleaning": ["N"],
    "energy": ["D","E"], "water": ["E"], "waste": ["E"]
  };

  function detectSectorFilter(ql) {
    for (const [kw, codes] of Object.entries(SECTOR_KEYWORDS)) {
      if (ql.includes(kw)) return r => codes.includes(r.NACE_Section);
    }
    return null;
  }

  function detectSectorLabel(ql) {
    for (const [kw, codes] of Object.entries(SECTOR_KEYWORDS)) {
      if (ql.includes(kw)) return codes.map(c => NACE_NAMES[c] || c).join("/");
    }
    return null;
  }

  // ── smart keyword search ────────────────────────────────────────
  function smartSearch(q, limit = 8) {
    const tokens = q.toLowerCase().split(/\s+/).filter(t => t.length > 2 &&
      !["which","company","companies","can","help","the","for","all","are","how","what","show","me","about","list","find","give"].includes(t));
    const hits = [];
    for (const r of DATA) {
      const blob = [
        r["Company name Latin alphabet"],
        r.Industry, r.NACE_Section, r.Legal_Form,
        r.B2B_or_B2C, r.Company_Description, r.Key_Activities
      ].join(" ").toLowerCase();
      const score = tokens.reduce((s, t) => s + (blob.includes(t) ? 1 : 0), 0);
      if (score > 0) hits.push({ r, score });
    }
    return hits.sort((a,b) => b.score - a.score).slice(0, limit).map(h => h.r);
  }

  // ── router ──────────────────────────────────────────────────────
  async function route(q) {
    if (hasKey()) {
      const sys = `Classify as exactly one word: "text", "code", or "visual".
- "visual" = user explicitly says chart/plot/graph/draw/visualise
- "code" = aggregations, counts, rates, top-N, comparisons, group-by stats
- "text" = look up specific company, definitions, summaries, open questions
Reply with ONLY the word.`;
      const out = await callClaude(`Question: "${q}"\n\nClassification:`, sys);
      if (out) {
        const t = out.toLowerCase().trim().replace(/[^a-z]/g, "");
        if (["text","code","visual"].includes(t)) return t;
      }
    }
    // Heuristic fallback
    const ql = q.toLowerCase();
    if (/(pie|bar|chart|graph|visual|plot|draw|show me a|visualis)/.test(ql)) return "visual";
    // "which company", "open a", "help me" → always text even if other code words present
    if (/(which company|what company|who can|help me|open a|start a|find a company|recommend|suggest)/.test(ql)) return "text";
    if (/(top \d|fastest|most|how many|count|rate|average|group|by sector|legal form|b2b|b2c|age|size|distribution|breakdown|compare|vs |versus)/.test(ql)) return "code";
    return "text";
  }

  // ── code agent ──────────────────────────────────────────────────
  function codeAgent(q) {
    const ql = q.toLowerCase();
    let result = null, plan = "";
    const has = (...ns) => ns.some(n => ql.includes(n));
    const sectorFilter = detectSectorFilter(ql);
    const sectorLabel = detectSectorLabel(ql);

    if (has("legal form", "gmbh", "ag ", " kg ", "legal")) {
      plan = `df.groupby("Legal_Form")["Scaler_2024"].mean()`;
      result = { kind:"rate-table", title:"Scaling rate by legal form", rows:groupRate("Legal_Form") };
    } else if (has("b2b","b2c","customer model","customer type")) {
      plan = `df.groupby("B2B_or_B2C")["Scaler_2024"].mean()`;
      result = { kind:"rate-table", title:"Scaling rate by customer model", rows:groupRate("B2B_or_B2C") };
    } else if (has("sector","nace","industry breakdown","by industry")) {
      plan = `df.groupby("NACE_Section")["Scaler_2024"].mean()`;
      result = { kind:"rate-table", title:"Scaling rate by NACE sector", rows:groupRate("NACE_Section") };
    } else if (has("age","young","old","founded")) {
      plan = `df.groupby(age_bucket)["Scaler_2024"].mean()`;
      result = { kind:"rate-table", title:"Scaling rate by company age", rows:ageBuckets() };
    } else if (has("size","headcount","employee")) {
      plan = `df.groupby(size_bucket)["Scaler_2024"].mean()`;
      const buckets = {"11–24":[11,25],"25–49":[25,50],"50–99":[50,100],"100–249":[100,250],"250+":[250,99999]};
      const m = {};
      for (const r of DATA) {
        const e = r["Number of employees 2024"]||0;
        for (const [k,[lo,hi]] of Object.entries(buckets)) {
          if (e>=lo && e<hi) { m[k]=m[k]||{n:0,s:0}; m[k].n++; m[k].s+=r.Scaler_2024||0; break; }
        }
      }
      result = { kind:"rate-table", title:"Scaling rate by employee count", rows:Object.keys(buckets).filter(k=>m[k]).map(k=>({k,n:m[k].n,rate:m[k].s/m[k].n})) };
    } else if (/top\s*\d+|fastest|best grower/.test(ql)) {
      const limit = parseInt(ql.match(/\d+/)?.[0] || "10");
      plan = `df[df.Scaler_2024==1].nlargest(${limit},"aagr 2024")`;
      result = { kind:"top-table", title:`Top ${limit} scalers by AAGR`, rows:topScalers(limit, sectorFilter||undefined) };
    } else if (has("how many scaler","number of scaler","count scaler")) {
      const filtered = sectorFilter ? DATA.filter(sectorFilter) : DATA;
      const n = filtered.filter(r=>r.Scaler_2024===1).length;
      plan = `df["Scaler_2024"].sum()`;
      result = { kind:"scalar", value:n, label:`scalers${sectorLabel?" in "+sectorLabel+" sector":""}` };
    } else if (has("overall rate","scaling rate","what is the rate","what percent")) {
      plan = `df["Scaler_2024"].mean()`;
      result = { kind:"scalar", value:(META.rate*100).toFixed(1)+"%", label:"overall scaling rate (1,083 firms)" };
    } else if (has("how many","count","number of","how much") && sectorFilter) {
      const filtered = DATA.filter(sectorFilter);
      const scalerCount = filtered.filter(r=>r.Scaler_2024===1).length;
      result = { kind:"scalar", value:filtered.length, label:`companies in ${sectorLabel} sector · ${scalerCount} are scalers (${((scalerCount/filtered.length)*100).toFixed(1)}%)` };
    } else if (sectorFilter) {
      plan = `df[df.NACE_Section.isin([...])]["Scaler_2024"].mean()`;
      result = { kind:"rate-table", title:`Scaling stats — ${sectorLabel} sector`, rows:groupRate("Legal_Form", 1, sectorFilter) };
    }
    return { plan, result };
  }

  // ── visual agent ────────────────────────────────────────────────
  function visualAgent(q) {
    const ql = q.toLowerCase();
    const isPie = /(pie|donut)/.test(ql);
    const sectorFilter = detectSectorFilter(ql);
    const sectorLabel  = detectSectorLabel(ql);

    let rows, title, chartType = isPie ? "pie" : "bar";

    if (sectorFilter && /(company|companies|distribution|breakdown|list)/.test(ql)) {
      // Show count distribution within a sector (e.g. "pie chart of real estate companies")
      rows = countByField("Legal_Form", sectorFilter).map(r => ({ k: r.k, rate: r.n, _rawCount: true }));
      title = `${sectorLabel} companies by legal form (count)`;
    } else if (has(ql,"legal form","gmbh","ag ","kg")) {
      rows = groupRate("Legal_Form");
      title = "Scaling rate by legal form";
    } else if (has(ql,"b2b","b2c","customer")) {
      rows = groupRate("B2B_or_B2C");
      title = "Scaling rate by customer model";
    } else if (has(ql,"age","young","old","founded")) {
      rows = ageBuckets();
      title = "Scaling rate by company age";
    } else if (has(ql,"size","employee","headcount")) {
      const buckets={"11–24":[11,25],"25–49":[25,50],"50–99":[50,100],"100–249":[100,250],"250+":[250,99999]};
      const m={};
      for (const r of DATA) {
        const e=r["Number of employees 2024"]||0;
        for (const [k,[lo,hi]] of Object.entries(buckets)) {
          if(e>=lo&&e<hi){m[k]=m[k]||{n:0,s:0};m[k].n++;m[k].s+=r.Scaler_2024||0;break;}
        }
      }
      rows=Object.keys(buckets).filter(k=>m[k]).map(k=>({k,n:m[k].n,rate:m[k].s/m[k].n}));
      title="Scaling rate by company size";
    } else if (sectorFilter) {
      rows = groupRate("NACE_Section", 1, sectorFilter).length
        ? countByField("Legal_Form", sectorFilter).map(r=>({k:r.k,rate:r.n,_rawCount:true}))
        : groupRate("NACE_Section");
      title = sectorLabel ? `${sectorLabel} sector breakdown` : "Scaling rate by sector";
    } else {
      rows = groupRate("NACE_Section");
      title = "Scaling rate by NACE sector";
    }

    return { title, rows, chartType };
  }

  function has(str, ...needles) { return needles.some(n => str.includes(n)); }

  // ── rich offline text answers ────────────────────────────────────
  function offlineTextAnswer(q, hits) {
    const ql = q.toLowerCase();
    const sectorFilter = detectSectorFilter(ql);
    const sectorLabel  = detectSectorLabel(ql);

    // "which company can help me with X" → list relevant companies
    if (/(which company|what company|who can|who help|recommend|suggest|looking for|open a|start a|find a)/.test(ql)) {
      const relevant = sectorFilter
        ? DATA.filter(sectorFilter).sort((a,b)=>(b["aagr 2024"]||0)-(a["aagr 2024"]||0)).slice(0,5)
        : hits.slice(0,5);
      if (relevant.length) {
        const sLabel = sectorLabel || "relevant";
        const list = relevant.map(r =>
          `• **${r["Company name Latin alphabet"]}** (${r.Legal_Form||"—"}) — ${r.Industry||r.NACE_Section||"—"}${r.Scaler_2024?" ✓ Scaler":""}`
        ).join("\n");
        return `Here are the top ${sLabel} companies in our Bremen dataset:\n\n${list}\n\n*Tip: ✓ Scaler means avg. employment growth ≥10%/yr over 5 years (OECD definition).*`;
      }
    }

    // Single company lookup
    if (hits.length === 1 || (hits.length && ql.split(" ").some(t=>t.length>5 && hits[0]["Company name Latin alphabet"].toLowerCase().includes(t)))) {
      const r = hits[0];
      const scaleTag = r.Scaler_2024===1 ? "is a confirmed Scaler (≥10% AAGR, 5 yrs)" : "did not meet scaler criteria in 2024";
      const emp2024 = r["Number of employees 2024"] ? `${r["Number of employees 2024"]} employees (2024)` : "";
      const growth = r["aagr 2024"] ? `, AAGR ${r["aagr 2024"].toFixed(1)}%` : "";
      return `**${r["Company name Latin alphabet"]}** — ${r.Industry||"—"}\n\nLegal form: ${r.Legal_Form||"—"} · NACE: ${r.NACE_Section||"—"} · Founded: ${r.Founded_Year||"—"} (${r.Company_Age||"—"} yrs old)\n${emp2024}${growth}\n\nThis company ${scaleTag}. Customer model: ${r.B2B_or_B2C||"—"}.`;
    }

    // Multiple hits
    if (hits.length > 1) {
      const scalerHits = hits.filter(r=>r.Scaler_2024===1);
      const list = hits.slice(0,5).map(r =>
        `• **${r["Company name Latin alphabet"]}** (${r.Legal_Form||"—"}, ${r.NACE_Section||"—"})${r.Scaler_2024?" ✓":""}`
      ).join("\n");
      return `Found ${hits.length} matching companies (${scalerHits.length} are Scalers):\n\n${list}\n\n*Add more specific keywords to narrow results.*`;
    }

    // Sector-specific stat questions
    if (sectorFilter && /(scale|scaler|grow|rate)/.test(ql)) {
      const filtered = DATA.filter(sectorFilter);
      const n = filtered.length;
      const s = filtered.filter(r=>r.Scaler_2024===1).length;
      return `In the **${sectorLabel}** sector, ${s} of ${n} Bremen companies (${((s/n)*100).toFixed(1)}%) qualify as Scalers. The overall Bremen average is 11.8%.`;
    }

    // Short/unclear questions
    if (q.trim().length < 5) {
      return `Please ask a question about Bremen companies — e.g. "Which sectors scale best?", "Tell me about ArcelorMittal", or "How does B2B vs B2C affect scaling?"`;
    }

    // Generic fallback with context
    return `Across **1,083 Bremen firms** studied (2019–2024), **128 qualify as Scalers** (11.8% rate).\n\n**Key findings:**\n• Top sector: Hospitality (32.5%)\n• Best legal form: AG (18.2%)\n• B2B outpaces B2C: 12.2% vs 6.7%\n• Youngest firms (0–10 yrs) scale at 18.2%; oldest (100+ yrs) at 3.6%\n\nTry asking about a specific company, sector, or legal form.`;
  }

  // ── text agent ──────────────────────────────────────────────────
  async function textAgent(q) {
    const hits = smartSearch(q);

    if (hasKey()) {
      const ctx = hits.length
        ? hits.map(r => `• ${r["Company name Latin alphabet"]} | ${r.Legal_Form} | ${r.NACE_Section} | ${r.Industry} | B2B_or_B2C=${r.B2B_or_B2C} | scaler=${r.Scaler_2024} | aagr=${r["aagr 2024"]||"—"} | employees_2024=${r["Number of employees 2024"]||"—"}`).join("\n")
        : "(no specific firms matched — use dataset-wide statistics)";

      const overall = `Dataset: 1,083 Bremen firms (>10 employees, 2019–2024). 128 scalers (11.8%). Top sector: Hospitality (32.5%). Best legal form: AG (18.2%). B2B 12.2% vs B2C 6.7%. Young firms (0–10 yr) scale at 18.2%.`;
      const prompt = `${overall}\n\nRetrieved firms:\n${ctx}\n\nQuestion: ${q}\n\nAnswer in 2–4 sentences. Be specific, cite company names and numbers when relevant.`;
      const out = await callClaude(prompt, "You are a Bremen company-data analyst for the WHU DDE project. Be concise and factual.");
      if (out) return { answer: out, cited: hits };
    }

    return { answer: offlineTextAnswer(q, hits), cited: hits };
  }

  // ── editor ──────────────────────────────────────────────────────
  async function editor(draft) {
    if (!draft || draft.length < 60 || !hasKey()) return draft;
    const out = await callClaude(
      `Polish to 2–3 tight sentences. Keep all numbers exact. No filler words. Output only the polished text.\n\n${draft}`
    );
    return out || draft;
  }

  return { load, route, codeAgent, visualAgent, textAgent, editor, search: smartSearch, get meta() { return META; } };
})();
