# MR Lab 化驗所優惠站

靜態網站：<https://www.mrlabhk.com>。現有公開儲存庫為 `carvensam/mrlabhk.com`，沿用 GitHub Pages，沒有新增預約或付款系統。

## 結構

- `index.html`：首頁
- `plans.html`：全部體檢計劃（分類篩選及搜尋）
- `plan-detail.html?id=<plan-id>`：計劃詳情
- `centres.html`：體檢中心列表
- `about.html`：關於我們
- `partner.html`：加入我們
- `data/plans.js` / `data/plans.json`：48 個 來源平台 歷史資料計劃
- `data/featured.js`：五款 MrLab Facebook 貼文優惠，加上先前加入的醫家 EPH2.0 公開會員優惠
- `assets/images/mrlab-*.jpg`：從對應 MrLab 貼文保存的真實完整海報
- `assets/images/*.svg`：來源平台 計劃示意圖、原有會員優惠配圖及 logo/favicon
- `assets/css/style.css`、`assets/js/app.js`：網站視覺樣式及共用邏輯
- `tools/`：資料解析、示意圖生成及靜態驗證工具

## 本機驗證

```bash
node --check data/featured.js
node --check assets/js/app.js
python3 tools/validate_site.py
python3 -m http.server 8123
```

`tools/generate_images.py` 只生成 SVG 示意圖，不會覆蓋 `mrlab-*.jpg` 真實海報。更新精選資料時必須逐項檢查所引用的實際圖片檔，不應把 SVG 存在視為已核實精選海報。

## MrLab 精選來源

E01–E05 已替換原本佔位資料。以下名稱及價格依 2026-11-20 讀取的 MrLab 化驗所優惠站 Facebook 貼文及海報整理；這個日期是讀取日期，並非確認優惠有效或更新價格的日期。

- **E01：79項身體檢查，HK$1,980。** 腹腔超聲波、男女相關部位及 DR70。用戶指定必選來源：[原貼文](https://www.facebook.com/permalink.php?story_fbid=pfbid02bh5x3j5SbWkcDf5mSfmNm5ziPpXXRhEoXFLpvoGUZKyox7GzY5C7W7u9U4SZYC3El&id=61562009227913)，亦由用戶分享連結 <https://www.facebook.com/share/p/1QLJiWZ8Dj/> 指向。
- **E02：78項女士核心檢查，HK$1,980。** 貼文原價 HK$3,200。[原貼文](https://www.facebook.com/permalink.php?story_fbid=pfbid0oF6F2KGwaGKMEuBsueeBsRZDLYZgexfG4JYKsPN8w6Tx3yT6QMTyr7T7vTrqLrtfl&id=61562009227913)。
- **E03：性健康病毒篩查及全面體檢，HK$1,680。** 23種HPV、梅毒VDRL、HIV ag/ab及60多項體檢。[原貼文海報](https://www.facebook.com/photo/?fbid=122179884566400307&set=a.122101593080400307)。
- **E04：74項上腹腔身體檢查，HK$2,380。** 五項上腹腔超聲波；貼文列有期間限定二選一加送，適用狀況須另行確認。[原貼文海報](https://www.facebook.com/photo/?fbid=122178361640400307&set=a.122101593080400307)。
- **E05：59項御守耆年重點身體檢查，HK$1,780。** 頸動脈超聲波IMT、CK及肺部X光。[原貼文海報](https://www.facebook.com/photo/?fbid=122178283226400307&set=a.122101593080400307)。

上述五款貼文均列明服務由 **香港生物醫學核心化驗所** 提供，不應標成醫家。保留的 E06 仍依 [LUAHK 公開會員優惠頁](https://store.luahk.org/member_discount_items) 整理，並非 MrLab Facebook 貼文。

貼文沒有清楚列出優惠截止日期或完整服務地址。網站不捏造期限、地址、營業時間或平台代訂授權；以 `bookingMode: "source-enquiry"` 顯示中性查詢及最新條款確認提示。`authorised: false` 配合此模式代表沒有在本次更新核實代訂授權，前端不把它表述成已證實「無授權」。

DR70和其他腫瘤指標不是單獨確診或排除癌症的檢查。网站文字保留項目事實，不擴大海報的醫療成效宣傳。原海報完整保存；詳情頁提供檢查限制提示。

## 其他資料及查詢

48個來源計劃資料依原附件整理，為2026-11-19所見售價，今次沒有更改其內容、來源、分類或授權標示。

WhatsApp：`https://wa.me/85246151993`，各計劃查詢連結自動帶入計劃名稱。來源平台 原有未授權中心提示繼續保留。

## 部署

GoDaddy 的根網域已改為 GitHub Pages 四個 A 記錄，`www` CNAME 為 `carvensam.github.io`。GitHub Pages DNS 檢查成功，Enforce HTTPS 已開啟，並已驗證 TLS 及 HTTP／根網域重定向至 <https://www.mrlabhk.com/>。

本儲存庫 `main` 分支的更新會由 GitHub Pages 部署。檢查正式網站時，應核對最新 `data/featured.js`、共用前端及五張真實海報已上線，而不是只確認首頁回傳成功。
