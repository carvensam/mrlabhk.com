/* MR LAB 化驗所優惠站 — 共用前端邏輯 */
(function () {
  "use strict";

  var FEATURED = window.FEATURED_DATA || [];
  var PLANS = window.PLANS_DATA || [];
  var ALL = FEATURED.concat(PLANS);
  var WA_NUMBER = "85246151993";

  var CAT_LABEL = {
    featured: "精選",
    general: "一般／全身",
    abdominal: "腹腔相關",
    women: "女性",
    cancer: "癌症相關"
  };

  function esc(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function findPlan(id) {
    for (var i = 0; i < ALL.length; i++) if (ALL[i].id === id) return ALL[i];
    return null;
  }

  function waText(p) {
    if (p.authorised) {
      return "你好，我想查詢及預約【" + p.name + "】（" + p.code + "），請提供詳情及可用時段。";
    }
    return "你好，我想查詢【" + p.name + "】（" + p.code + "）。本人了解該體檢中心無授權本平台代為 Booking，會直接聯絡該體檢中心自行預約，請提供聯絡方式。";
  }

  function waLink(p) {
    return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(waText(p));
  }

  function money(p) {
    return p.price || "n.a.";
  }

  function icon(name) {
    var paths = {
      search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
      arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
      shield: '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 10-4.6-1.6-8-5-8-10V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
      heart: '<path d="M12 20s-7-4.6-7-9.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 7 3.5C19 15.4 12 20 12 20z"/><path d="M4 12h4l2-3 3 6 2-3h5"/>',
      scan: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
      female: '<circle cx="12" cy="8" r="5"/><path d="M12 13v8M8 17h8"/>',
      lab: '<path d="M9 3h6M10 3v7L5 20h14l-5-10V3"/><path d="M7 16h10"/>',
      check: '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
      info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
      whatsapp: '<path d="M20 12a8 8 0 0 1-11.7 7.1L4 20l1-4.2A8 8 0 1 1 20 12z"/><path d="M9 9c0 3 2 5 5 5l1.2-1.6 1.8.9c.3.2.4.5.2.8-.6 1.2-2 1.9-3.7 1.6-2.5-.5-4.4-2.6-4.7-5.2-.1-1.4.6-2.7 1.8-3.3.3-.2.6-.1.8.2l.8 1.6z"/>'
    };
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + (paths[name] || paths.info) + "</svg>";
  }

  function renderHeader() {
    var page = document.body.dataset.page || "";
    var items = [
      ["index", "首頁", "index.html"],
      ["plans", "全部體檢計劃", "plans.html"],
      ["centres", "體檢中心", "centres.html"],
      ["about", "關於我們", "about.html"],
      ["partner", "加入我們", "partner.html"]
    ];
    var nav = items.map(function (x) {
      return '<a href="' + x[2] + '"' + (page === x[0] ? ' class="active"' : "") + ">" + x[1] + "</a>";
    }).join("");
    document.getElementById("site-header").innerHTML =
      '<div class="container header-inner">' +
        '<a class="brand" href="index.html" aria-label="MR Lab 首頁">' +
          '<img src="assets/images/logo.svg" alt="MR Lab 標誌">' +
          '<span class="brand-text"><strong>MR LAB</strong><span>化驗所優惠站</span></span>' +
        "</a>" +
        '<button class="nav-toggle" id="navToggle" aria-label="開啟導覽">&#9776;</button>' +
        '<nav class="main-nav" id="mainNav">' + nav + "</nav>" +
        '<a class="header-cta" href="https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("你好，我想查詢化驗所優惠站嘅體檢計劃。") + '" target="_blank" rel="noopener">' + icon("whatsapp") + " WhatsApp 查詢</a>" +
      "</div>";
    var btn = document.getElementById("navToggle");
    if (btn) btn.addEventListener("click", function () {
      document.getElementById("mainNav").classList.toggle("open");
    });
  }

  function renderFooter() {
    document.getElementById("site-footer").innerHTML =
      '<div class="container">' +
        '<div class="footer-grid">' +
          '<div><h4>MR LAB 化驗所優惠站</h4><p>重質與收費透明，不比機構數量。整理香港體檢計劃資料，方便你客觀比較檢查內容、價格與分店資訊。</p>' +
            '<p class="disclaimer">所有價格及資料僅供參考，實際內容、可用時段及收費以體檢中心及出處頁面最新公布為準。</p></div>' +
          '<div><h4>網站導覽</h4><ul><li><a href="index.html">首頁</a></li><li><a href="plans.html">全部體檢計劃</a></li><li><a href="centres.html">體檢中心列表</a></li><li><a href="about.html">關於我們</a></li><li><a href="partner.html">加入我們</a></li></ul></div>' +
          '<div><h4>分類</h4><ul><li><a href="plans.html?cat=general">一般／全身</a></li><li><a href="plans.html?cat=abdominal">腹腔相關</a></li><li><a href="plans.html?cat=women">女性</a></li><li><a href="plans.html?cat=cancer">癌症相關</a></li></ul></div>' +
          '<div><h4>聯絡</h4><ul><li>WhatsApp / 電話：4615 1993</li><li>擁有者電郵：welldonemarketinghk@gmail.com</li><li><a href="https://www.facebook.com/" target="_blank" rel="noopener">Facebook 專頁</a></li></ul>' +
            '<a class="btn btn--primary btn--small" style="margin-top:10px" href="https://wa.me/' + WA_NUMBER + '" target="_blank" rel="noopener">WhatsApp 4615 1993</a></div>' +
        "</div>" +
        '<div class="footer-bottom"><span>© ' + new Date().getFullYear() + ' MR Lab 化驗所優惠站. All rights reserved.</span>' +
          '<span>免責聲明：本站為資訊整理平台，不提供診斷、治療或醫療建議。</span></div>' +
      "</div>";
  }

  function planCard(p) {
    var authBadge = p.authorised
      ? '<span class="badge badge--auth">可經本平台查詢預約</span>'
      : '<span class="badge badge--noauth">無授權本平台代訂</span>';
    var note = p.authorised
      ? ""
      : '<p class="note">此體檢中心無授權本平台代為 Booking，請直接聯絡該體檢中心自行預約。</p>';
    return '<article class="card">' +
      '<img class="card-img" src="' + esc(p.image) + '" alt="' + esc(p.name) + ' 專屬配圖" loading="lazy">' +
      '<div class="card-body">' +
        '<div class="card-top"><span class="badge badge--code">' + esc(p.code) + "</span>" +
          '<span class="badge badge--cat">' + esc(CAT_LABEL[p.category] || p.categoryLabel || "體檢計劃") + "</span>" + authBadge + "</div>" +
        "<h3>" + esc(p.name) + "</h3>" +
        '<p class="centre">' + esc(p.centre) + (p.itemCount ? " · " + esc(p.itemCount) : "") + "</p>" +
        '<p class="summary">' + esc(p.highlight || "請查看完整檢查內容") + "</p>" +
        '<div class="price-row"><span class="price-label">網上售價／參考價</span><span class="price-value">' + esc(money(p)) + "</span></div>" +
        '<div class="card-actions">' +
          '<a class="btn btn--outline btn--small" href="plan-detail.html?id=' + encodeURIComponent(p.id) + '">查看詳情 ' + icon("arrow") + "</a>" +
          '<a class="btn btn--whatsapp btn--small" href="' + waLink(p) + '" target="_blank" rel="noopener">' + icon("whatsapp") + " WhatsApp 查詢</a>" +
        "</div>" + note +
      "</div></article>";
  }

  function initHome() {
    var featured = FEATURED;
    document.getElementById("featured-grid").innerHTML = featured.map(planCard).join("");

    var cats = [
      ["general", "一般／全身檢查", "基本指標、三高、肝腎功能、超聲波及心電圖", "lab"],
      ["abdominal", "腹腔相關檢查", "腹部超聲波、CT／MRI、胃腸鏡、肝臟健康", "scan"],
      ["women", "女性體檢計劃", "婦科超聲波、柏氏抹片、HPV 及女性癌症指標", "female"],
      ["cancer", "癌症相關檢查", "癌症指標、低劑量 CT、糞便 DNA 及CTC 篩檢", "shield"]
    ];
    document.getElementById("category-grid").innerHTML = cats.map(function (c) {
      return '<a class="cat-card" href="plans.html?cat=' + c[0] + '">' +
        '<span class="cat-icon">' + icon(c[3]) + "</span><span><h3>" + c[1] + "</h3><span>" + c[2] + "</span></span></a>";
    }).join("");

    var centres = uniqueCentres();
    document.getElementById("centre-preview").innerHTML = centres.slice(0, 6).map(function (c, i) {
      return '<article class="card centre-card">' +
        '<div class="card-top"><span class="badge badge--code">' + String(i + 1).padStart(2, "0") + "</span>" +
          (c.name.indexOf("醫家") === 0 ? '<span class="badge badge--auth">可查詢預約</span>' : "") + "</div>" +
        "<h3>" + esc(c.name) + "</h3>" +
        '<p class="meta">' + c.locations.length + " 個地點 · " + c.plans.length + " 個計劃</p>" +
        '<ul>' + c.locations.slice(0, 2).map(function (l) {
          return "<li>" + esc(l.name) + '<div class="addr">' + esc(l.address || "地址請向中心查詢") + "</div></li>";
        }).join("") + "</ul>" +
        '<a class="text-link" href="centres.html">查看體檢中心列表 ' + icon("arrow") + "</a></article>";
    }).join("");
  }

  function uniqueCentres() {
    var map = {};
    ALL.forEach(function (p) {
      if (!map[p.centre]) map[p.centre] = { name: p.centre, plans: [], locations: [], index: Object.keys(map).length };
      map[p.centre].plans.push(p);
      (p.locations || []).forEach(function (l) {
        var key = (l.name || "") + "|" + (l.address || "");
        if (!map[p.centre]._seen) map[p.centre]._seen = {};
        if (!map[p.centre]._seen[key]) {
          map[p.centre]._seen[key] = true;
          map[p.centre].locations.push(l);
        }
      });
    });
    var list = Object.keys(map).map(function (k) { return map[k]; });
    list.sort(function (a, b) {
      var aa = a.name.indexOf("醫家") === 0 ? 0 : 1;
      var bb = b.name.indexOf("醫家") === 0 ? 0 : 1;
      return aa - bb || a.index - b.index;
    });
    return list;
  }

  function getParam(name) {
    var m = new RegExp("[?&]" + name + "=([^&#]*)").exec(window.location.search);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function initPlans() {
    var chips = document.querySelectorAll(".chip[data-cat]");
    var search = document.getElementById("planSearch");
    var cat = getParam("cat") || "all";

    function apply() {
      var q = (search.value || "").trim().toLowerCase();
      chips.forEach(function (c) { c.classList.toggle("active", c.dataset.cat === cat); });
      var list = ALL.filter(function (p) {
        if (cat !== "all" && p.category !== cat) return false;
        if (!q) return true;
        var hay = [p.name, p.centre, p.code, p.highlight, (p.locations || []).map(function (l) { return l.name; }).join(" ")].join(" ").toLowerCase();
        return hay.indexOf(q) !== -1;
      });
      document.getElementById("resultCount").textContent = "共 " + list.length + " 個計劃" + (cat === "all" ? "" : "（" + (CAT_LABEL[cat] || cat) + "）");
      document.getElementById("plans-grid").innerHTML = list.length
        ? list.map(planCard).join("")
        : '<div class="empty">搵唔到符合條件嘅計劃，請試吓其他關鍵字或分類。</div>';
    }

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        cat = c.dataset.cat;
        var url = cat === "all" ? "plans.html" : "plans.html?cat=" + cat;
        history.replaceState(null, "", url);
        apply();
      });
    });
    search.addEventListener("input", apply);
    apply();
  }

  function initDetail() {
    var id = getParam("id");
    var p = findPlan(id);
    var root = document.getElementById("detail-root");
    if (!p) {
      root.innerHTML = '<div class="empty">找不到此計劃。請返回 <a class="text-link" href="plans.html">全部體檢計劃</a>。</div>';
      return;
    }
    document.title = p.name + " | MR Lab 化驗所優惠站";
    var audience = (p.audience || []).map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("");
    var exams = (p.examSections || []).map(function (s) {
      return '<div class="exam-group"><h4>' + esc(s.title) + "</h4><ul>" +
        s.items.map(function (i) { return "<li>" + esc(i) + "</li>"; }).join("") + "</ul></div>";
    }).join("");
    var locs = (p.locations || []).map(function (l) {
      return '<div class="location"><h4>' + esc(l.name) + "</h4>" +
        (l.address ? '<p><span class="lbl">地址</span>' + esc(l.address) + "</p>" : "") +
        ((l.hours || []).length ? '<p><span class="lbl">辦公時間</span>' + esc(l.hours.join("；")) + "</p>" : "") +
        (l.phone ? '<p><span class="lbl">電話</span>' + esc(l.phone) + "</p>" : "") +
        (l.note ? '<p><span class="lbl">備註</span>' + esc(l.note) + "</p>" : "") +
        "</div>";
    }).join("");
    var authNote = p.authorised
      ? "此計劃由醫家健康體檢中心提供，可經本平台 WhatsApp 查詢及預約。"
      : "此體檢中心無授權本平台代為 Booking，請直接聯絡該體檢中心自行預約。";

    root.innerHTML =
      '<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">首頁</a> / <a href="plans.html">全部體檢計劃</a> / ' + esc(p.code) + "</div>" +
        '<span class="badge badge--code">' + esc(p.code) + "</span> " +
        '<span class="badge badge--cat">' + esc(CAT_LABEL[p.category] || p.categoryLabel) + "</span> " +
        (p.authorised ? '<span class="badge badge--auth">可經本平台查詢預約</span>' : '<span class="badge badge--noauth">無授權本平台代訂</span>') +
        "<h1>" + esc(p.name) + "</h1><p>" + esc(p.centre) + " · " + esc(p.itemCount) + " · " + esc(money(p)) + "</p></div></div>" +
      '<div class="container section"><div class="detail-layout"><div class="detail-main">' +
        '<img src="' + esc(p.image) + '" alt="' + esc(p.name) + ' 專屬配圖">' +
        '<div class="detail-content">' +
          "<h2>基本資料</h2><dl class=\"kv\">" +
            "<dt>計劃名稱</dt><dd>" + esc(p.name) + "</dd>" +
            "<dt>體檢中心</dt><dd>" + esc(p.centre) + "</dd>" +
            "<dt>標示項目數</dt><dd>" + esc(p.itemCount || "n.a.") + "</dd>" +
            "<dt>網上售價</dt><dd>" + esc(money(p)) + "</dd>" +
            "<dt>出處</dt><dd>" + esc(p.source || "n.a.") + "</dd>" +
            "<dt>出處網址</dt><dd>" + (p.sourceUrl ? '<a class="text-link" href="' + esc(p.sourceUrl) + '" target="_blank" rel="noopener">' + esc(p.sourceUrl) + "</a>" : "n.a.") + "</dd>" +
          "</dl>" +
          "<h2>適用對象及重點</h2><ul>" + audience + "</ul>" +
          "<h2>檢查內容</h2>" + (exams || "<p>n.a.</p>") +
          "<h2>分店資料</h2>" + (locs || "<p>n.a.</p>") +
          "<h2>預約及收費說明</h2><p>所有價格為出處頁面所見售價，僅供參考；實際收費、檢查項目及辦公時間可能隨時更改，預約前請向體檢中心核實。" + (p.dataNote ? " " + esc(p.dataNote) : "") + "</p>" +
          "<p><strong>" + esc(authNote) + "</strong></p>" +
        "</div></div>" +
        '<aside class="detail-side">' +
          '<div class="side-card"><span class="price-label">網上售價／參考價</span><span class="price-value">' + esc(money(p)) + "</span>" +
            '<label>WhatsApp 查詢（4615 1993）</label>' +
            '<a class="btn btn--whatsapp btn--block" href="' + waLink(p) + '" target="_blank" rel="noopener">' + icon("whatsapp") + " 帶計劃名稱查詢</a>" +
            '<p style="margin-top:12px">' + esc(authNote) + "</p></div>" +
          '<div class="side-card notice-card"><h4>收費透明聲明</h4><p>事前已列明之額外費用屬於清晰標示，並非隱藏收費。若有任何收費爭議，請以出處頁面及體檢中心單據為準。</p></div>' +
          '<div class="side-card"><h4>快速導覽</h4><p><a class="text-link" href="plans.html">返回全部計劃</a><br><a class="text-link" href="centres.html">體檢中心列表</a><br><a class="text-link" href="about.html">關於我們</a></p></div>' +
        "</aside></div></div>";
  }

  function initCentres() {
    var list = uniqueCentres();
    document.getElementById("centre-count").textContent = list.length + " 間體檢中心";
    document.getElementById("centres-grid").innerHTML = list.map(function (c) {
      var links = c.plans.map(function (p) {
        return '<a href="plan-detail.html?id=' + encodeURIComponent(p.id) + '">' + esc(p.code) + " " + esc(p.name) + "</a>";
      }).join("");
      return '<article class="card centre-card">' +
        '<div class="card-top"><span class="badge badge--code">' + esc(String(c.plans[0].code).toUpperCase().slice(0, 1)) + "</span>" +
          (c.name.indexOf("醫家") === 0 ? '<span class="badge badge--auth">可經本平台查詢預約</span>' : "") + "</div>" +
        "<h3>" + esc(c.name) + "</h3>" +
        '<p class="meta">' + c.locations.length + " 個地點 · " + c.plans.length + " 個計劃</p>" +
        "<ul>" + c.locations.map(function (l) {
          return "<li><strong>" + esc(l.name) + "</strong><div class=\"addr\">" + esc(l.address || "n.a.") +
            (l.hours && l.hours.length ? " · " + esc(l.hours.join("；")) : "") +
            (l.phone ? " · " + esc(l.phone) : "") + "</div></li>";
        }).join("") + "</ul>" +
        '<div class="plan-links">' + links + "</div></article>";
    }).join("");
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderHeader();
    renderFooter();
    var page = document.body.dataset.page;
    if (page === "home") initHome();
    else if (page === "plans") initPlans();
    else if (page === "detail") initDetail();
    else if (page === "centres") initCentres();
  });
})();
