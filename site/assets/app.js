/* Hash wiki: #/uk, #/uk/signs, #/uk/signs/670, #/uk/markings/1003, #/uk/furniture, #/uk/fonts */
(function () {
  const UK = window.ATLAS_UK;
  const $ = (sel, el) => (el || document).querySelector(sel);
  const main = $("#main");
  const navEl = $("#nav");
  const qEl = $("#q");

  if (!UK) {
    main.innerHTML = "<p class='note'>Missing assets/data.js. Run <code>python3 tools/extract_uk.py</code>.</p>";
    return;
  }

  const ATLASES = { uk: UK };
  const COUNTRIES = [
    { id: "uk", name: UK.country.name, live: true },
    { id: "us", name: "United States (placeholder)", live: false },
    { id: "de", name: "Germany (placeholder)", live: false },
  ];

  function parseHash() {
    const raw = (location.hash || "#/uk").replace(/^#\/?/, "");
    const p = raw.split("/").filter(Boolean);
    return { country: p[0] || "uk", kind: p[1] || "", id: decodeURIComponent(p[2] || "") };
  }

  function href(c, kind, id) {
    let h = "#/" + c;
    if (kind) h += "/" + kind;
    if (id) h += "/" + encodeURIComponent(id);
    return h;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function crumbs(parts) {
    return `<div class="crumbs">${parts.map((p, i) =>
      i === parts.length - 1 ? esc(p.label) : `<a href="${p.href}">${esc(p.label)}</a> / `
    ).join("")}</div>`;
  }

  function metres(n) {
    if (n == null || n === "") return "—";
    const x = Number(n);
    if (Number.isNaN(x)) return esc(n);
    return x.toFixed(x >= 10 ? 1 : 2) + " m";
  }

  const COUNT_KEYS = new Set(["arrows", "count"]);
  function dimTable(d) {
    if (!d) return "";
    const rows = Object.entries(d).map(([k, v]) => {
      const cell = COUNT_KEYS.has(k) ? String(v) : metres(v);
      return `<tr><th>${esc(k.replace(/_/g, " "))}</th><td>${cell}</td></tr>`;
    }).join("");
    return `<table class="meta">${rows}</table>`;
  }

  function nav(route) {
    const c = route.country;
    const items = [
      ["Home", href(c, "", "")],
      ["Signs", href(c, "signs", "")],
      ["Road markings", href(c, "markings", "")],
      ["Street furniture", href(c, "furniture", "")],
      ["Fonts & colours", href(c, "fonts", "")],
      ["Siting", href(c, "siting", "")],
      ["About", href(c, "about", "")],
    ];
    navEl.innerHTML =
      `<li class="sec">Catalogue</li>` +
      items.map(([lab, h]) => {
        const kind = (h.split("/")[2] || "");
        const on = (!route.kind && lab === "Home") || (route.kind === kind);
        return `<li><a class="${on ? "active" : ""}" href="${h}">${lab}</a></li>`;
      }).join("") +
      `<li class="sec">Countries</li>` +
      COUNTRIES.map((x) =>
        `<li><a class="${x.id === c ? "active" : ""}" href="${x.live ? href(x.id, "", "") : href("uk", "", "")}">${esc(x.name)}</a></li>`
      ).join("");
  }

  function home(atlas) {
    const co = atlas.country;
    const glyphs = atlas.signs.filter((s) => s.glyph);
    const families = {};
    atlas.signs.forEach((s) => { families[s.family] = (families[s.family] || 0) + 1; });
    main.innerHTML = `
      ${crumbs([{ href: href(co.id, "", ""), label: co.name }])}
      <h1>${esc(co.name)} signage</h1>
      <p class="lede">Procedural catalogue of UK plates, TSM markings and CHS posts GridForge can cook. Counts come from the JSON. Iterate faces here; port strokes back to <code>UkTsrgdFace</code> after the wiki looks right.</p>
      <p class="note">${esc(co.applies)} Spec ${esc((co.spec || []).join(", "))}. Units: ${esc(co.units)}.</p>
      <div class="filters">
        <span class="pill">${co.counts.signs} signs</span>
        <span class="pill glyph">${co.counts.glyphs} dedicated glyphs</span>
        <span class="pill fallback">${co.counts.fallback} family fallbacks</span>
        <span class="pill">${atlas.markings.length} markings</span>
        <span class="pill">${atlas.furniture.length} furniture</span>
      </div>
      <h2>Dedicated glyphs</h2>
      <div class="grid">${glyphs.map(cardSign).join("")}</div>
      <h2>Families</h2>
      <table class="meta">${Object.entries(families).sort((a, b) => b[1] - a[1]).map(([k, n]) =>
        `<tr><th><a href="${href(co.id, "signs", "")}?family=${encodeURIComponent(k)}">${esc(k)}</a></th><td>${n}</td></tr>`).join("")}</table>
      <p class="licence">${esc(co.licence.diagrams)} ${esc(co.licence.typeface)}</p>
    `;
    bindCards();
  }

  function faceSrc(kind, id, country) {
    return "faces/" + (country || "uk") + "/" + kind + "/" + encodeURIComponent(id) + ".svg";
  }
  function placeholderFace(id) {
    const lab = esc(String(id || "").slice(0, 10));
    return `<svg viewBox="-1 -1 2 2" width="160" height="160" role="img" aria-label="${lab} placeholder">
      <rect x="-0.55" y="-0.55" width="1.10" height="1.10" rx="0.04" fill="#D8D6CE" stroke="#6E6C66" stroke-width="0.03"/>
      <rect x="-0.46" y="-0.14" width="0.92" height="0.32" rx="0.03" fill="#D8D6CE"/>
      <text x="0" y="0.06" text-anchor="middle" font-size="0.18" fill="#3A3A38">${lab}</text>
    </svg>`;
  }
  // EPS-first: a sign whose face_source is "eps" loads the locally cooked GOV.UK EPS face
  // (site/faces-eps/, gitignored; built by tools/eps/build.py or tools/serve.sh). If it is missing
  // (offline, not built) the procedural face is the fallback, then the placeholder.
  function epsSrc(item, country) {
    return "faces-eps/" + (country || "uk") + "/signs/" + encodeURIComponent(item.id) + ".svg";
  }
  function faceHtml(kind, item) {
    const country = (window.__atlasCountry) || "uk";
    const baked = faceSrc(kind, item.id, country);
    const fs = item.face_source;
    const fallback = `(function(img){var t=img.nextElementSibling;img.replaceWith(t.content.cloneNode(true));})(this)`;
    if (kind === "signs" && fs && fs.source === "eps") {
      const toBaked = `(function(img){if(img.dataset.fb){${fallback.replace("(this)", "(img)")};return;}img.dataset.fb=1;img.src='${baked}';img.title='EPS face not built; showing the procedural fallback';})(this)`;
      return `<img class="face-img" src="${epsSrc(item, country)}" alt="${esc(item.id)}" width="160" height="160" onerror="${toBaked}"/>` +
        `<template>${placeholderFace(item.id)}</template>`;
    }
    return `<img class="face-img" src="${baked}" alt="${esc(item.id)}" width="160" height="160" onerror="${fallback}"/>` +
      `<template>${placeholderFace(item.id)}</template>`;
  }
  function sourcePill(item) {
    const fs = item.face_source;
    if (!fs) return "";
    const lab = fs.source === "eps" ? "GOV.UK EPS" : fs.source;
    return `<span class="pill source-${esc(fs.source)}" title="${esc((fs.why_not_eps || []).join("; "))}">${esc(lab)}</span>`;
  }
  function sourceRows(item) {
    const fs = item.face_source;
    if (!fs) return "";
    const why = (fs.why_not_eps || []).map(esc).join("<br>");
    return `<tr><th>Face source</th><td>${esc(fs.source)}${fs.source === "eps" ? " (fallback: " + esc(fs.fallback) + (fs.superseded ? "; hand-traced face superseded" : "") + ")" : ""}</td></tr>` +
      (fs.eps ? `<tr><th>GOV.UK EPS</th><td><code>${esc(fs.eps)}</code></td></tr>` : "") +
      (why ? `<tr><th>Why not EPS</th><td>${why}</td></tr>` : "");
  }
  function statusPill(item) {
    const st = item.status || "";
    if (!st || st === "current") return "";
    return `<span class="pill status-${esc(st)}">${esc(st)}</span>`;
  }
  function shortName(n) {
    // P1: cards show a short name; the article shows the full SI caption.
    const t = String(n || "");
    if (t.length <= 70) return t;
    const cut = t.slice(0, 70);
    return cut.slice(0, Math.max(cut.lastIndexOf(" "), 40)) + "…";
  }
  function cardSign(s) {
    return `<div class="card" data-href="${href("uk", "signs", s.id)}">
      <div class="face">${faceHtml("signs", s)}</div>
      <div class="k">${esc(s.id)}${s.renumbered_to ? " → " + esc(s.renumbered_to) : ""} ${statusPill(s)} ${sourcePill(s)}</div>
      <div class="n" title="${esc(s.name)}">${esc(shortName(s.name))}</div>
    </div>`;
  }
  function cardMark(m) {
    return `<div class="card" data-href="${href("uk", "markings", m.id)}">
      <div class="face">${faceHtml("markings", m)}</div>
      <div class="k">${esc(m.id)}</div>
      <div class="n">${esc(m.name)}</div>
    </div>`;
  }
  function cardFurn(f) {
    return `<div class="card" data-href="${href("uk", "furniture", f.id)}">
      <div class="face">${faceHtml("furniture", f)}</div>
      <div class="k">${esc(f.id)}</div>
      <div class="n">${esc(f.name)}</div>
    </div>`;
  }
  function bindCards() {
    main.querySelectorAll(".card[data-href]").forEach((el) => {
      el.addEventListener("click", () => { location.hash = el.getAttribute("data-href").slice(1); });
    });
  }

  function listSigns(atlas, familyFilter, query) {
    const q = (query || "").trim().toLowerCase();
    const params = new URL(location.href).searchParams;
    const statusFilter = params.get("status") || "";
    let rows = atlas.signs;
    if (familyFilter) rows = rows.filter((s) => s.family === familyFilter);
    if (statusFilter) rows = rows.filter((s) => (s.status || "current") === statusFilter);
    if (q) {
      rows = rows.filter((s) =>
        (s.id + " " + s.name + " " + s.what + " " + s.family + " " + s.mount).toLowerCase().includes(q));
    }
    const families = [...new Set(atlas.signs.map((s) => s.family))].sort();
    const statuses = [...new Set(atlas.signs.map((s) => s.status || "current"))].sort();
    main.innerHTML = `
      ${crumbs([{ href: href("uk", "", ""), label: "UK" }, { href: href("uk", "signs", ""), label: "Signs" }])}
      <h1>Traffic signs</h1>
      <p class="lede">${atlas.signs.length} catalogue rows (${(atlas.country.counts && atlas.country.counts.glyphs) || 0} dedicated glyphs). Fallbacks are a hatched placeholder, not a real plate.</p>
      <div class="filters" id="fam">
        <button data-f="" class="${!familyFilter ? "on" : ""}">All</button>
        ${families.map((f) => `<button data-f="${esc(f)}" class="${familyFilter === f ? "on" : ""}">${esc(f)}</button>`).join("")}
      </div>
      <div class="filters" id="st">
        <button data-s="" class="${!statusFilter ? "on" : ""}">Any status</button>
        ${statuses.map((st) => `<button data-s="${esc(st)}" class="${statusFilter === st ? "on" : ""}">${esc(st)}</button>`).join("")}
      </div>
      <div class="grid">${rows.map(cardSign).join("")}</div>
    `;
    bindCards();
    $("#fam").addEventListener("click", (e) => {
      const b = e.target.closest("button[data-f]");
      if (!b) return;
      const f = b.getAttribute("data-f");
      const u = new URL(location.href);
      if (f) u.searchParams.set("family", f); else u.searchParams.delete("family");
      history.replaceState(null, "", u.pathname + u.search + location.hash);
      render();
    });
    $("#st").addEventListener("click", (e) => {
      const b = e.target.closest("button[data-s]");
      if (!b) return;
      const st = b.getAttribute("data-s");
      const u = new URL(location.href);
      if (st) u.searchParams.set("status", st); else u.searchParams.delete("status");
      history.replaceState(null, "", u.pathname + u.search + location.hash);
      render();
    });
  }

  function signArticle(atlas, id) {
    const s = atlas.signs.find((x) => x.id === id);
    if (!s) { main.innerHTML = `<p class="note">Unknown sign ${esc(id)}</p>`; return; }
    const d = s.dimensions_m;
    main.innerHTML = `
      ${crumbs([
        { href: href("uk", "", ""), label: "UK" },
        { href: href("uk", "signs", ""), label: "Signs" },
        { href: href("uk", "signs", s.id), label: s.diagram },
      ])}
      <div class="article">
        <div class="hero">${faceHtml("signs", s)}</div>
        <div>
          <h1>${esc(s.diagram)} — ${esc(s.name)}</h1>
          <p>${esc(s.what)}</p>
          <p>
            <span class="pill ${s.glyph ? "glyph" : "fallback"}">${s.glyph ? "dedicated glyph" : "family fallback"}</span>
            ${statusPill(s)}
            ${sourcePill(s)}
            <span class="pill">${esc(s.family)}</span>
            <span class="pill">${esc(s.mount)}</span>
            <span class="pill">ch.${esc(s.chapter)}</span>
          </p>
          <h2>What it is</h2>
          <table class="meta">
            <tr><th>Diagram</th><td>${esc(s.diagram)}${s.status && s.status !== "current" ? " · " + esc(s.status) : ""}</td></tr>
            <tr><th>2016 index</th><td>${esc(s.index_id || s.id)}${s.renumbered_to ? " → " + esc(s.renumbered_to) : ""}${(s.renumbered_also || []).map((x) => " + " + esc(x)).join("")}</td></tr>
            ${s.si_caption ? `<tr><th>SI 2016 caption</th><td>${esc(s.si_caption)}${s.si_ref ? " (" + esc(s.si_ref) + ")" : ""}</td></tr>` : ""}
            ${s.name_alias ? `<tr><th>Also called</th><td>${esc(s.name_alias)}</td></tr>` : ""}
            ${(s.permitted_mm && s.permitted_mm.length) ? `<tr><th>Permitted sizes</th><td>${esc(s.permitted_mm.join(", "))} mm${s.permitted_dim ? " (" + esc(s.permitted_dim) + ")" : ""}</td></tr>` : ""}
            <tr><th>Family</th><td>${esc(s.family)}</td></tr>
            <tr><th>Renderer</th><td><code>${esc(s.renderer)}</code></td></tr>
            ${sourceRows(s)}
            <tr><th>OSM</th><td><code>${esc(s.osm)}</code></td></tr>
            <tr><th>Mount</th><td>${esc(s.mount)}</td></tr>
            <tr><th>Siting</th><td>${esc(s.siting)}</td></tr>
          </table>
          <h2>Dimensions</h2>
          ${dimTable(d)}
          <p class="lede">Working size in the cooker. Permitted sizes come from the SI 2016 table for this diagram (shown above when sourced).</p>
          <h2>Fonts</h2>
          <table class="meta">
            <tr><th>Official</th><td>${esc(s.font.official)}</td></tr>
            <tr><th>Procedural</th><td>${esc(s.font.procedural)}</td></tr>
          </table>
          <h2>Siting</h2>
          <p>${esc(s.siting_note)}</p>
          <p>Underside ${metres(d.underside)}. Post Ø ${metres(d.post_diameter)}. Verge offset ${metres(d.verge_offset)}.</p>
        </div>
      </div>
      <p class="licence">${s.kind === "non-tsrgd" || s.status === "not-2016"
        ? "Not a TSRGD 2016 diagram. Identification silhouette only."
        : (s.face_source && s.face_source.source === "eps"
          ? "Face: GOV.UK traffic sign image (EPS), Crown copyright, Department for Transport, Open Government Licence v3.0; converted locally from the GOV.UK EPS (attribution embedded in the SVG). Transport typeface is not shipped."
          : "Crown copyright. Open Government Licence v3.0. Redrawn identification silhouettes; hex colours are screen approximations. Transport typeface is not shipped.")}</p>
    `;
  }

  function listMarks(atlas, query) {
    const q = (query || "").trim().toLowerCase();
    let rows = atlas.markings;
    if (q) rows = rows.filter((m) => (m.id + " " + m.name + " " + m.what).toLowerCase().includes(q));
    main.innerHTML = `
      ${crumbs([{ href: href("uk", "", ""), label: "UK" }, { href: href("uk", "markings", ""), label: "Markings" }])}
      <h1>Road markings</h1>
      <p class="lede">Traffic Signs Manual Chapter 5 working sizes as cooked by <code>RoadMarkingRules</code>.</p>
      <div class="grid">${rows.map(cardMark).join("")}</div>
    `;
    bindCards();
  }

  function markArticle(atlas, id) {
    const m = atlas.markings.find((x) => x.id === id);
    if (!m) { main.innerHTML = `<p class="note">Unknown marking ${esc(id)}</p>`; return; }
    main.innerHTML = `
      ${crumbs([
        { href: href("uk", "", ""), label: "UK" },
        { href: href("uk", "markings", ""), label: "Markings" },
        { href: href("uk", "markings", m.id), label: m.id },
      ])}
      <div class="article">
        <div class="hero">${faceHtml("markings", m)}</div>
        <div>
          <h1>${esc(m.id)} — ${esc(m.name)}</h1>
          <p>${esc(m.what)}</p>
          <table class="meta">
            <tr><th>Renderer</th><td><code>${esc(m.renderer)}</code></td></tr>
            <tr><th>Pairs with</th><td>${m.pair ? `<a href="${href("uk", "signs", m.pair)}">${esc(m.pair)}</a>` : "—"}</td></tr>
          </table>
          <h2>Dimensions</h2>
          ${dimTable(m.dimensions_m)}
        </div>
      </div>
    `;
  }

  function listFurn(atlas) {
    main.innerHTML = `
      ${crumbs([{ href: href("uk", "", ""), label: "UK" }, { href: href("uk", "furniture", ""), label: "Furniture" }])}
      <h1>Street furniture</h1>
      <p class="lede">CHS posts, Belisha, telegraph (BS 1990), L12 D pylon, portal gantry. Spec 019.</p>
      <div class="grid">${atlas.furniture.map(cardFurn).join("")}</div>
    `;
    bindCards();
  }

  function furnArticle(atlas, id) {
    const f = atlas.furniture.find((x) => x.id === id);
    if (!f) { main.innerHTML = `<p class="note">Unknown furniture ${esc(id)}</p>`; return; }
    main.innerHTML = `
      ${crumbs([
        { href: href("uk", "", ""), label: "UK" },
        { href: href("uk", "furniture", ""), label: "Furniture" },
        { href: href("uk", "furniture", f.id), label: f.id },
      ])}
      <div class="article">
        <div class="hero">${faceHtml("furniture", f)}</div>
        <div>
          <h1>${esc(f.name)}</h1>
          <p>${esc(f.what)}</p>
          <table class="meta">
            <tr><th>Spec</th><td>${esc(f.spec)}</td></tr>
            <tr><th>Renderer</th><td><code>${esc(f.renderer)}</code></td></tr>
          </table>
          <h2>Dimensions</h2>
          ${dimTable(f.dimensions_m)}
        </div>
      </div>
    `;
  }

  function fontsPage(atlas) {
    const co = atlas.country;
    const cols = Object.entries(co.colours).map(([k, v]) =>
      `<tr><th>${esc(k)}</th><td><span style="display:inline-block;width:1.2rem;height:1.2rem;background:${esc(v)};vertical-align:middle;margin-right:.4rem;border:1px solid #3a3428"></span><code>${esc(v)}</code></td></tr>`).join("");
    main.innerHTML = `
      ${crumbs([{ href: href("uk", "", ""), label: "UK" }, { href: href("uk", "fonts", ""), label: "Fonts" }])}
      <h1>Fonts and colours</h1>
      <p class="note">The Transport typeface is the official TSRGD legend. It is not shipped. Static plates use Schedule 17 stand-in strokes (including lower case). Seven-bar numerals are Schedule 17 Part 5 VMS on MS4 only.</p>
      <h2>Type</h2>
      <table class="meta">${co.fonts.map((f) =>
        `<tr><th>${esc(f.name)}</th><td>${esc(f.role)} — ${f.shipped ? "shipped" : "not shipped"}. ${esc(f.reason)}</td></tr>`).join("")}</table>
      <h2>Screen approximations of BS EN 12899-1 classes</h2>
      <table class="meta">${cols}</table>
    `;
  }

  function sitingPage(atlas) {
    main.innerHTML = `
      ${crumbs([{ href: href("uk", "", ""), label: "UK" }, { href: href("uk", "siting", ""), label: "Siting" }])}
      <h1>Siting rules</h1>
      <p class="lede">${esc((atlas.siting.lede && atlas.siting.lede.text) || "Siting keys below. Every number has a source.")}</p>
      <table class="meta">${Object.entries(atlas.siting).filter(([k]) => k !== "lede").map(([k, v]) => {
        const text = v && typeof v === "object" ? v.text : v;
        const src = v && typeof v === "object" ? v.source : "";
        return `<tr><th>${esc(k)}</th><td>${esc(text)}${src ? `<div class="note">${esc(src)}</div>` : ""}</td></tr>`;
      }).join("")}</table>
    `;
  }

  function aboutPage(atlas) {
    const co = atlas.country;
    main.innerHTML = `
      ${crumbs([{ href: href(co.id, "", ""), label: co.name }, { href: href(co.id, "about", ""), label: "About" }])}
      <h1>About this catalogue</h1>
      <p>Redrawn identification silhouettes for GridForge. Not manufacturing drawings.</p>
      <h2>Sources</h2>
      <p class="note">Full list: <code>docs/SOURCES.md</code> and GridForge spec 015 §24. Highway Code pages are English captions. Diagram numbers stay as index. HC plate maps are not an id source.</p>
      <ul>
        <li><a href="https://www.highwaycodeuk.co.uk/signs-and-signals.html">Highway Code — Signs and signals</a> (OGL, 2026 edition)</li>
        <li><a href="https://www.highwaycodeuk.co.uk/warning-signs-on-the-road.html">Warning signs</a></li>
        <li><a href="https://www.highwaycodeuk.co.uk/road-signs-giving-orders.html">Signs giving orders</a></li>
        <li><a href="https://www.highwaycodeuk.co.uk/direction-signs-on-roads-motorways.html">Direction signs</a></li>
        <li><a href="https://www.highwaycodeuk.co.uk/information-signs.html">Information signs</a></li>
        <li><a href="https://www.highwaycodeuk.co.uk/light-signals-controlling-traffic.html">Light signals</a></li>
        <li><a href="https://www.highwaycodeuk.co.uk/road-markings.html">Road markings</a></li>
        <li><a href="https://www.highwaycodeuk.co.uk/road-works-signs.html">Road works signs</a></li>
        <li>TSRGD 2016 (SI 2016/362) — index in <code>countries/uk/tsrgd2016_index.json</code></li>
        <li>Know Your Traffic Signs 2023</li>
        <li>Traffic Signs Manual Chapter 5 (2018) — cited per marking; <strong>not OGL</strong></li>
        <li>Vendored dest catalogue <code>vendor/gridforge/UkTsrgdCatalogue.cs</code></li>
      </ul>
      <h2>Licence</h2>
      <p>${esc(co.licence.diagrams)}</p>
      <p>${esc(co.licence.typeface)}</p>
      <h2>Method</h2>
      <p>EPS first: fixed pictogram faces come from the GOV.UK traffic sign images (EPS, Crown copyright, OGL v3.0), fetched once and converted on this machine by <code>tools/eps/</code> into <code>site/faces-eps/</code> (not committed; the build generates them, and each carries the Crown copyright / OGL v3.0 notice). Everything else, and the offline fallback for every EPS face, is baked SVG from <code>tools/atlas/render.py</code>. Extract is the only JSON writer. Validator runs on every <code>rebuild.py --all</code>.</p>
      <h2>Limitations</h2>
      <p>TSM Chapters 1, 3, 4, 6, 7 unread. Spec 015/019 full text is not in this tree. Transport is not shipped. Highway Code caption maps are quarantined and are not an id source.</p>
    `;
  }

  function notFound(route) {
    main.innerHTML = `
      <h1>Not found</h1>
      <p class="note">No page for <code>#/${esc(route.country)}${route.kind ? "/" + esc(route.kind) : ""}${route.id ? "/" + esc(route.id) : ""}</code>.</p>
      <p><a href="${href("uk", "", "")}">UK home</a> · <a href="${href("uk", "about", "")}">About</a></p>
    `;
  }

  function searchPage(atlas, q) {
    const n = q.toLowerCase();
    const aliases = (atlas.country && atlas.country.renumber) || {};
    const aliasHit = Object.entries(aliases).filter(([a, b]) => a.toLowerCase() === n || String(b).toLowerCase() === n).flatMap(([a, b]) => [a, b]);
    const signs = atlas.signs.filter((s) =>
      (s.id + " " + s.diagram + " " + s.name + " " + s.what + " " + s.family).toLowerCase().includes(n)
      || aliasHit.includes(s.id) || aliasHit.includes(s.diagram)
    );
    const marks = atlas.markings.filter((m) => (m.id + " " + m.name + " " + m.what).toLowerCase().includes(n));
    const furn = atlas.furniture.filter((f) => (f.id + " " + f.name + " " + f.what).toLowerCase().includes(n));
    main.innerHTML = `
      <h1>Search “${esc(q)}”</h1>
      <h2>Signs (${signs.length})</h2>
      <p class="note">${signs.length} sign hits${signs.length > 48 ? " (showing 48)" : ""}.</p>
      <div class="grid">${signs.slice(0, 48).map(cardSign).join("") || "<p class='lede'>None</p>"}</div>
      <h2>Markings (${marks.length})</h2>
      <div class="grid">${marks.map(cardMark).join("") || "<p class='lede'>None</p>"}</div>
      <h2>Furniture (${furn.length})</h2>
      <div class="grid">${furn.map(cardFurn).join("") || "<p class='lede'>None</p>"}</div>
    `;
    bindCards();
  }

  function render() {
    const route = parseHash();
    window.__atlasCountry = route.country || "uk";
    nav(route);
    const atlas = ATLASES[route.country];
    if (!atlas) { notFound(route); return; }
    const q = qEl.value;
    const family = new URLSearchParams(location.search).get("family") || "";
    if (q.trim() && !route.id) { searchPage(atlas, q.trim()); return; }
    if (!route.kind) home(atlas);
    else if (route.kind === "signs" && route.id) signArticle(atlas, route.id);
    else if (route.kind === "signs") listSigns(atlas, family, "");
    else if (route.kind === "markings" && route.id) markArticle(atlas, route.id);
    else if (route.kind === "markings") listMarks(atlas, "");
    else if (route.kind === "furniture" && route.id) furnArticle(atlas, route.id);
    else if (route.kind === "furniture") listFurn(atlas);
    else if (route.kind === "fonts") fontsPage(atlas);
    else if (route.kind === "siting") sitingPage(atlas);
    else if (route.kind === "about") aboutPage(atlas);
    else notFound(route);
  }

  window.addEventListener("hashchange", render);
  qEl.addEventListener("input", () => render());
  if (!location.hash) location.hash = "#/uk";
  render();
})();
