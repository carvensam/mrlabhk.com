/* MR LAB 化驗所優惠站 — 共用前端邏輯 */
(function () {
  "use strict";

  var FEATURED = window.FEATURED_DATA || [];
  var PLANS = window.PLANS_DATA || [];
  var ITEMS = window.ITEMS_DATA || [];
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

  function isSourceEnquiry(p) {
    return p.bookingMode === "source-enquiry";
  }

  function isPoster(p) {
    return p.imageKind === "poster";
  }

  function bookingBadge(p) {
    if (isSourceEnquiry(p)) return '<span class="badge badge--enquiry">優惠查詢</span>';
    if (p.authorised === true) return '<span class="badge badge--auth">可經本平台查詢預約</span>';
    if (p.authorised === false) return '<span class="badge badge--noauth">無授權本平台代訂</span>';
    return '<span class="badge badge--enquiry">優惠查詢</span>';
  }

  function bookingNote(p) {
    if (isSourceEnquiry(p)) return "可向" + p.centre + "查詢收費、服務地點及預約安排。";
    if (p.authorised === true) return "此計劃由" + p.centre + "提供，可經本平台 WhatsApp 查詢及預約。";
    if (p.authorised === false) return "【" + p.name + "】此體檢中心無授權本平台代為 Booking，請直接聯絡該體檢中心自行預約。";
    return "請經 WhatsApp 查詢收費、服務地點及預約安排。";
  }

  function locationSummary(c) {
    return (c.locations.length ? c.locations.length + " 個地點" : "服務地點待查詢") + " · " + c.plans.length + " 個計劃";
  }

  function priceLabel() {
    return "優惠價";
  }

  function centreImage(name, index) {
    var src = "assets/images/centre-" + String(index).padStart(2, "0") + ".png";
    return '<img class="centre-img" src="' + esc(src) + '" alt="' + esc(name) + ' 識別圖" loading="lazy">';
  }

  function planImage(p, detail) {
    var poster = isPoster(p);
    var alt = p.name + " 優惠圖";
    var cls = detail ? (poster ? ' class="detail-img--poster"' : "") : ' class="card-img' + (poster ? " card-img--poster" : "") + '"';
    var img = "<img" + cls + ' src="' + esc(p.image) + '" alt="' + esc(alt) + '"' + (detail ? "" : ' loading="lazy"') + ">";
    return poster ? '<a class="poster-link" href="' + esc(p.image) + '" target="_blank" rel="noopener" aria-label="' + esc("查看優惠圖片：" + p.name) + '">' + img + "</a>" : img;
  }

  function waText(p) {
    if (isSourceEnquiry(p) || p.authorised == null) {
      return "你好，我想查詢【" + p.name + "】（" + p.code + "，" + p.centre + "）。請問收費、優惠是否仍適用、適用資格、檢查詳情、服務地點、可用時段及預約安排？";
    }
    if (p.authorised === true) {
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
      ["items", "體檢項目解說", "items.html"],
      ["about", "關於我們", "about.html"],
      ["partner", "加入我們", "partner.html"]
    ];
    var nav = items.map(function (x) {
      return '<a href="' + x[2] + '"' + (page === x[0] ? ' class="active"' : "") + ">" + x[1] + "</a>";
    }).join("");
    document.getElementById("site-header").innerHTML =
      '<div class="container header-inner">' +
        '<a class="brand" href="index.html" aria-label="MR Lab 首頁">' +
          '<img src="assets/images/logo-mrlab.png" alt="MR Lab 標誌">' +
          '<span class="brand-text"><strong>MR LAB</strong><span>化驗所優惠站</span></span>' +
        "</a>" +
        '<button class="nav-toggle" id="navToggle" aria-label="開啟導覽">&#9776;</button>' +
        '<nav class="main-nav" id="mainNav">' + nav + "</nav>" +
        '<a class="header-cta btn--whatsapp" aria-label="WhatsApp 查詢" href="https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("你好，我想查詢化驗所優惠站嘅體檢計劃。") + '" target="_blank" rel="noopener">' + icon("whatsapp") + '<span class="header-cta-label">WhatsApp 查詢</span></a>' +
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
          '<div><h4>MR LAB 化驗所優惠站</h4><p>香港體檢優惠一站搜尋，按檢查內容、價格及分店資料直接查詢。</p>' +
            '<p class="disclaimer">本站只提供優惠資料，不提供診斷、治療或醫療建議。</p></div>' +
          '<div><h4>網站導覽</h4><ul><li><a href="index.html">首頁</a></li><li><a href="plans.html">全部體檢計劃</a></li><li><a href="centres.html">體檢中心列表</a></li><li><a href="items.html">體檢項目解說</a></li><li><a href="about.html">關於我們</a></li><li><a href="partner.html">加入我們</a></li></ul></div>' +
          '<div><h4>分類</h4><ul><li><a href="plans.html?cat=general">一般／全身</a></li><li><a href="plans.html?cat=abdominal">腹腔相關</a></li><li><a href="plans.html?cat=women">女性</a></li><li><a href="plans.html?cat=cancer">癌症相關</a></li></ul></div>' +
          '<div><h4>聯絡</h4><ul><li>WhatsApp / 電話：4639 4019</li><li>電郵：info@welldonemarketinghk.com</li></ul>' +
            '<a class="btn btn--whatsapp btn--small" style="margin-top:10px" href="https://wa.me/' + WA_NUMBER + '" target="_blank" rel="noopener">WhatsApp 查詢</a></div>' +
        "</div>" +
        '<div class="footer-bottom"><span>© ' + new Date().getFullYear() + ' MR Lab 化驗所優惠站. All rights reserved.</span>' +
          '<span>本站只提供優惠資訊，不提供診斷、治療或醫療建議。</span></div>' +
      "</div>";
  }

  function planCard(p) {
    var authBadge = bookingBadge(p);
    var note = !isSourceEnquiry(p) && p.authorised === true ? "" : '<p class="note' + (isSourceEnquiry(p) ? " note--enquiry" : "") + '">' + esc(bookingNote(p)) + "</p>";
    return '<article class="card">' +
      planImage(p, false) +
      '<div class="card-body">' +
        '<div class="card-top"><span class="badge badge--code">' + esc(p.code) + "</span>" +
          '<span class="badge badge--cat">' + esc(CAT_LABEL[p.category] || p.categoryLabel || "體檢計劃") + "</span>" + authBadge + "</div>" +
        "<h3>" + esc(p.name) + "</h3>" +
        '<p class="centre">' + esc(p.centre) + (p.itemCount ? " · " + esc(p.itemCount) : "") + "</p>" +
        '<p class="summary">' + esc(p.highlight || "請查看完整檢查內容") + "</p>" +
        '<div class="price-row"><span class="price-label">' + priceLabel(p) + '</span><span class="price-value">' + esc(money(p)) + "</span></div>" +
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
        centreImage(c.name, i + 1) +
        '<div class="card-top"><span class="badge badge--code">' + String(i + 1).padStart(2, "0") + "</span>" +
          "</div>" +
        "<h3>" + esc(c.name) + "</h3>" +
        '<p class="meta">' + locationSummary(c) + "</p>" +
        (c.locations.length ? '<ul>' + c.locations.slice(0, 2).map(function (l) {
          return "<li>" + esc(l.name) + '<div class="addr">' + esc(l.address || "地址請向中心查詢") + "</div></li>";
        }).join("") + "</ul>" : '<p class="meta">請經 WhatsApp 查詢服務地點及時間</p>') +
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
    function rank(name) {
      if (name.indexOf("香港生物醫學核心化驗所") === 0) return 0;
      if (name.indexOf("醫家健康體檢中心") === 0) return 1;
      return 2;
    }
    list.sort(function (a, b) {
      return rank(a.name) - rank(b.name) || a.index - b.index;
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
    var authNote = bookingNote(p);

    root.innerHTML =
      '<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">首頁</a> / <a href="plans.html">全部體檢計劃</a> / ' + esc(p.code) + "</div>" +
        '<span class="badge badge--code">' + esc(p.code) + "</span> " +
        '<span class="badge badge--cat">' + esc(CAT_LABEL[p.category] || p.categoryLabel) + "</span> " +
        bookingBadge(p) +
        "<h1>" + esc(p.name) + "</h1><p>" + esc(p.centre) + (p.itemCount ? " · " + esc(p.itemCount) : "") + " · " + esc(money(p)) + "</p></div></div>" +
      '<div class="container section"><div class="detail-layout"><div class="detail-main">' +
        planImage(p, true) +
        '<div class="detail-content">' +
          (isPoster(p) ? '<p class="poster-view"><a class="text-link" href="' + esc(p.image) + '" target="_blank" rel="noopener">查看優惠圖片（亦可點擊上方圖片）</a></p>' : "") +
          "<h2>基本資料</h2><dl class=\"kv\">" +
            "<dt>計劃名稱</dt><dd>" + esc(p.name) + "</dd>" +
            "<dt>體檢中心</dt><dd>" + esc(p.centre) + "</dd>" +
            "<dt>項目數</dt><dd>" + esc(p.itemCount || "n.a.") + "</dd>" +
            "<dt>" + priceLabel(p) + "</dt><dd>" + esc(money(p)) + "</dd>" +
          "</dl>" +
          "<h2>適用對象及重點</h2><ul>" + audience + "</ul>" +
          "<h2>檢查內容</h2>" + (exams || "<p>n.a.</p>") +
          (p.medicalNote ? "<h2>醫療提醒</h2><p>" + esc(p.medicalNote) + "</p>" : "") +
          "<h2>服務地點及時間</h2>" + (locs || "<p>請經 WhatsApp 查詢服務地點及時間</p>") +
          "<h2>查詢說明</h2><p>收費、檢查項目及服務時間可向體檢中心查詢。</p>" +
          "<p><strong>" + esc(authNote) + "</strong></p>" +
        "</div></div>" +
        '<aside class="detail-side">' +
          '<div class="side-card"><span class="price-label">' + priceLabel(p) + '</span><span class="price-value">' + esc(money(p)) + "</span>" +
            '<label>WhatsApp 查詢</label>' +
            '<a class="btn btn--whatsapp btn--block" href="' + waLink(p) + '" target="_blank" rel="noopener">' + icon("whatsapp") + " 帶計劃名稱查詢</a>" +
            '<p style="margin-top:12px">' + esc(authNote) + "</p></div>" +
          '<div class="side-card notice-card"><h4>查詢提示</h4><p>可按 WhatsApp 查詢收費、服務地點及預約安排。</p></div>' +
          '<div class="side-card"><h4>快速導覽</h4><p><a class="text-link" href="plans.html">返回全部計劃</a><br><a class="text-link" href="centres.html">體檢中心列表</a><br><a class="text-link" href="about.html">關於我們</a></p></div>' +
        "</aside></div></div>";
  }

  function initCentres() {
    var list = uniqueCentres();
    document.getElementById("centre-count").textContent = list.length + " 間體檢中心";
    document.getElementById("centres-grid").innerHTML = list.map(function (c, i) {
      var links = c.plans.map(function (p) {
        return '<a href="plan-detail.html?id=' + encodeURIComponent(p.id) + '">' + esc(p.code) + " " + esc(p.name) + "</a>";
      }).join("");
      return '<article class="card centre-card">' +
        centreImage(c.name, i + 1) +
        '<div class="card-top"><span class="badge badge--code">' + String(i + 1).padStart(2, "0") + "</span>" +
          "</div>" +
        "<h3>" + esc(c.name) + "</h3>" +
        '<p class="meta">' + locationSummary(c) + "</p>" +
        (c.locations.length ? "<ul>" + c.locations.map(function (l) {
          return "<li><strong>" + esc(l.name) + "</strong><div class=\"addr\">" + esc(l.address || "地址請向中心查詢") +
            (l.hours && l.hours.length ? " · " + esc(l.hours.join("；")) : "") +
            (l.phone ? " · " + esc(l.phone) : "") + "</div></li>";
        }).join("") + "</ul>" : '<p class="meta">請經 WhatsApp 查詢服務地點及時間</p>') +
        '<div class="plan-links">' + links + "</div></article>";
    }).join("");
  }

  function initItems() {
    var root = document.getElementById("items-root");
    var chips = document.getElementById("item-chips");
    var search = document.getElementById("itemSearch");
    var active = "all";

    chips.innerHTML = '<button class="chip active" data-item-cat="all">全部 ' + ITEMS.reduce(function (n, g) { return n + g.items.length; }, 0) + " 項</button>" +
      ITEMS.map(function (g) {
        return '<button class="chip" data-item-cat="' + esc(g.id) + '">' + esc(g.name) + " " + g.items.length + "</button>";
      }).join("");

    function apply() {
      var q = (search.value || "").trim().toLowerCase();
      chips.querySelectorAll(".chip").forEach(function (c) { c.classList.toggle("active", c.dataset.itemCat === active); });
      var total = 0;
      var html = ITEMS.map(function (g) {
        if (active !== "all" && active !== g.id) return "";
        var rows = g.items.filter(function (it) {
          if (!q) return true;
          return (it.name + " " + it.en + " " + it.desc).toLowerCase().indexOf(q) !== -1;
        }).map(function (it) {
          total++;
          return '<details class="item-row"><summary><span class="item-name">' + esc(it.name) +
            '</span><span class="item-en">' + esc(it.en) + '</span><span class="item-plus" aria-hidden="true">＋</span></summary>' +
            '<div class="item-desc">' + esc(it.desc) + "</div></details>";
        }).join("");
        if (!rows) return "";
        return '<section class="item-group"><div class="item-group-head"><span class="cat-icon">' + icon(g.icon) +
          '</span><div><h2>' + esc(g.name) + '</h2><p>' + esc(g.intro) + "</p></div></div>" +
          '<div class="item-list">' + rows + "</div></section>";
      }).join("");
      document.getElementById("item-count").textContent = "共 " + total + " 個項目" + (q || active !== "all" ? "符合目前篩選" : "");
      root.innerHTML = html || '<div class="empty">搵唔到符合條件嘅項目，請試吓其他關鍵字或分類。</div>';
    }

    chips.addEventListener("click", function (e) {
      var btn = e.target.closest(".chip[data-item-cat]");
      if (!btn) return;
      active = btn.dataset.itemCat;
      apply();
    });
    search.addEventListener("input", apply);
    apply();
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderHeader();
    renderFooter();
    var page = document.body.dataset.page;
    if (page === "home") initHome();
    else if (page === "plans") initPlans();
    else if (page === "detail") initDetail();
    else if (page === "centres") initCentres();
    else if (page === "items") initItems();
  });
})();
