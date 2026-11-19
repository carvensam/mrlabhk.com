# MR Lab 化驗所優惠站

靜態網站，目標網址：<https://www.mrlabhk.com>

## 結構

- `index.html` 首頁
- `plans.html` 全部體檢計劃（分類篩選＋搜尋）
- `plan-detail.html?id=<plan-id>` 計劃詳情
- `centres.html` 體檢中心列表
- `about.html` 關於我們
- `partner.html` 加入我們
- `data/plans.js` / `data/plans.json`：48 個 ESD Life 計劃（由附件 txt 自動解析）
- `data/featured.js`：醫家健康體檢中心精選計劃（公開資料整理／佔位）
- `assets/images/`：每個計劃一張獨立 SVG 圖片（共 54 張，另加 logo/favicon）
- `assets/css/style.css`、`assets/js/app.js`：醫療專業視覺系統同共用邏輯
- `tools/`：解析、生圖、驗證、GitHub 設定腳本

## 本機驗證

```bash
python tools/parse_plans.py
python tools/generate_images.py
python tools/validate_site.py
python -m http.server 8123
```

## 資料說明

- 48 個計劃資料擷取自附件 `香港體檢計劃資料（共 48 個）.txt`（ESD Life，2026-11-19 所見售價，僅供參考）。
- 醫家健康體檢中心嘅精選計劃目前根據公開貼文整理並清楚標註為佔位資料；待 Facebook 專頁自動化接通後應替換為專頁最新版本及對應圖片。
- 本站不設網頁 Booking 或線上付款。所有 WhatsApp 連結均為 `https://wa.me/85246151993` 並帶入計劃名稱。
- 未授權中心之卡片與詳情頁均註明「該體檢中心無授權本平台代為 Booking，請直接聯絡該體檢中心自行預約」。

## 部署狀態（全部完成）

- ✅ **正式網址**：<https://www.mrlabhk.com>（HTTP 自動導向 HTTPS）。
- ✅ GitHub Repository：`carvensam/mrlabhk.com`（public），`main` branch 已推送。
- ✅ GitHub Pages 已啟用（`built`），CNAME = `www.mrlabhk.com`。
- ✅ Enforce HTTPS 已開啟，SSL 憑證有效至 2027-02-17，覆蓋 `mrlabhk.com` 及 `www.mrlabhk.com`。
- ✅ DNS（A 記錄）已指向 GitHub Pages IP `185.199.108–111.153`。
- ✅ 全部頁面、CSS/JS、數據檔及 54 張圖片經本機與正式站點雙重驗證（200 / errors=0）。

> GoDaddy 手動 DNS 設定記錄見 `GODADDY_DNS_SETUP.md`（供日後參考）。
