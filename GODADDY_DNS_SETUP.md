# GoDaddy DNS 設定指南 — www.mrlabhk.com

## 現況（全部完成 ✅）

| 項目 | 狀態 |
|---|---|
| GitHub Repository | ✅ 已建立 `carvensam/mrlabhk.com`（public） |
| 網站檔案 | ✅ 已推送到 `main`（54 個計劃 = 6 個精選 + 48 個計劃，每張獨立圖片） |
| GitHub Pages | ✅ 已啟用，build 狀態 `built`，source = `main` / root |
| CNAME（GitHub 端） | ✅ 已設為 `www.mrlabhk.com`（repo 內亦有 `CNAME` 檔） |
| Enforce HTTPS | ✅ 已開啟，SSL 憑證有效至 2027-02-17 |
| GoDaddy DNS | ✅ `www` 及 `@` 的 A 記錄已指向 `185.199.108–111.153` |
| 正式站點 | ✅ <https://www.mrlabhk.com> 全部網頁／資產回傳 200，HTTP 自動導 HTTPS |

> 以下手動步驟為當初设定的記錄，供日後 DNS 需重新設定時使用。

---

## 手動設定步驟（GoDaddy）

1. 登入 <https://sso.godaddy.com/>（帳號 `welldonemarketinghk@gmail.com`）。
2. **My Products** → 搵到 `mrlabhk.com` → **DNS** → **Manage DNS**。
3. 喺 **Records** 頁：
   - 如果見到 `www` 嘅 **CNAME** 記錄（指向 `sites...godaddy.com` 或停車頁），先**刪除**佢。
   - 修改／刪除現有 `www` 嘅 **A** 記錄（應該係 `15.197.148.33` 或 `3.33.130.190`）。
4. 加入以下 **A 記錄**（Type = `A`，TTL 用預設 1 小時或 600 秒）：

   | Type | Name | Value |
   |---|---|---|
   | A | `www` | `185.199.108.153` |
   | A | `www` | `185.199.109.153` |
   | A | `www` | `185.199.110.153` |
   | A | `www` | `185.199.111.153` |
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |

   - `www` 嘅 4 條 A 記錄係必須（直接服務 `www.mrlabhk.com`）。
   - `@` 嘅 4 條 A 記錄讓 naked domain `mrlabhk.com` 自動 redirect 去 `www`（GitHub Pages 會處理）。
5. **Save**。DNS 生效需時幾分鐘至 24–48 小時。

---

## DNS 生效後 — 開啟 Enforce HTTPS

DNS 生效並經 GitHub 偵測到後，SSL 憑證會自動簽發（通常幾分鐘至數小時）。完成後執行：

```powershell
cd "C:\Users\user\Documents\Default Project"
python tools/github_pages_status.py
```

或者喺 GitHub 手動開啟：
- Repo `carvensam/mrlabhk.com` → **Settings** → **Pages** → 剔「**Enforce HTTPS**」。

## 驗證

```powershell
# 應回傳 200 同網站內容
python -c "import urllib.request; r=urllib.request.urlopen('https://www.mrlabhk.com',timeout=30); print(r.status, len(r.read()), r.geturl())"
```

成功嘅話 `https://www.mrlabhk.com` 會顯示網站，而且 `https://` 強制生效。

---

## 若 GoDaddy 想用 CNAME（替代方案）

如果 GoDaddy 介面唔俾你加 `www` 嘅 A 記錄，可以改用：
- `www` → **CNAME** → `carvensam.github.io`

但 A 記錄（4 個 IP）係 GitHub 官方推薦做法，兼容性較好，建議優先使用。
