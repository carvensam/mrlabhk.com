# MR Lab 化驗所優惠站

靜態網站：<https://www.mrlabhk.com>。現有儲存庫：`carvensam/mrlabhk.com`，使用 GitHub Pages，沒有預約或付款系統。

## 結構

- `index.html`：首頁
- `plans.html`：全部體檢計劃（分類篩選及搜尋）
- `plan-detail.html?id=<plan-id>`：計劃詳情
- `centres.html`：體檢中心列表
- `about.html`：關於我們
- `partner.html`：加入我們
- `data/plans.js` / `data/plans.json`：48 個計劃
- `data/featured.js`：6 個精選優惠
- `assets/images/`：54 張計劃圖片、logo 及 favicon
- `assets/css/style.css`、`assets/js/app.js`：網站樣式及共用邏輯
- `tools/`：資料處理及驗證工具

## 本機驗證

```bash
node --check data/featured.js
node --check data/plans.js
node --check assets/js/app.js
python3 tools/validate_site.py
python3 -m http.server 8123
```

更新資料時須檢查每項計劃引用的實際圖片檔，確保圖片存在且沒有重複。

## 精選優惠

- **E01：79項身體檢查，HK$1,980。**
- **E02：78項女士核心檢查，HK$1,980。**
- **E03：性健康病毒篩查及全面體檢，HK$1,680。**
- **E04：74項上腹腔身體檢查，HK$2,380。**
- **E05：59項御守耆年重點身體檢查，HK$1,780。**
- **E06：醫家 EPH2.0 升級檢查計劃，HK$730。** 分店地址及電話已更新為醫家對外公布資料。

E06 四間分店：尖沙咀、佐敦、中環、荃灣；電話 6661 8628。

DR70 及其他腫瘤指標並非單獨確診或排除癌症的檢查，詳情頁已保留相關提醒。

## 查詢

WhatsApp：`https://wa.me/85246151993`，各計劃查詢連結自動帶入計劃名稱。需要由體檢中心自行預約的計劃，卡面及詳情頁均有提示。

## 部署

GoDaddy 根網域已改用 GitHub Pages 四個 A 記錄，`www` CNAME 為 `carvensam.github.io`。GitHub Pages DNS 檢查成功，Enforce HTTPS 已開啟，並已驗證 TLS 及 HTTP／根網域重定向至 <https://www.mrlabhk.com/>。

`main` 分支更新會由 GitHub Pages 部署。上線後可執行 `python3 tools/verify_live.py` 檢查網頁、圖片及 HTTPS。
