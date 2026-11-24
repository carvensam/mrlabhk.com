# Browser visual QA

## 2026-11-25 — centre logo rebuild, local pre-deploy QA

Checked the local build at `http://127.0.0.1:8765` with a cache-busting query. All lazy-loaded images were forced to load before counting.

| Page | Images | Broken | Centre thumbnails | Unwanted wording | Console errors |
| --- | ---: | ---: | ---: | ---: | ---: |
| `/index.html` | 13 | 0 | 6/6 at 640×240 | 0 | 0 |
| `/plans.html` | 55 | 0 | 0 | 0 | 0 |
| `/plan-detail.html?id=e06` | 2 | 0 | 0 | 0 | 0 |
| `/centres.html` | 32 | 0 | 31/31 at 640×240 | 0 | 0 |
| `/items.html` | 1 | 0 | 0 | 0 | 0 |
| `/about.html` | 1 | 0 | 0 | 0 | 0 |
| `/partner.html` | 1 | 0 | 0 | 0 | 0 |

Additional checks:

- All 31 centre thumbnails are uniform 640×240 PNGs, fully inside the canvas with no clipping or edge contact.
- Logo sources were re-checked against official centre websites and recorded in `tools/logo_sources.json`; centres without a standalone centre-specific mark use an exact-name wordmark.
- Index 27 (`香港仁和體檢`) uses the darker official re:HEALTH asset so it remains legible on the light panel.
- Centre order is `香港生物醫學核心化驗所` → `醫家健康體檢中心` → `美邦醫學體檢中心`.
- Homepage slogan renders as `回饋社會．全民體檢`.
- Centre cards contain no authorisation / booking sentences; the required note remains on plan cards, plan detail and WhatsApp prefill.
- Every WhatsApp link uses `https://wa.me/85246151993` and renders in official green.
- Footer shows only `WhatsApp / 電話：4639 4019` and `電郵：info@welldonemarketinghk.com`; no old phone, Gmail or Facebook copy.
- E06 detail and centre pages retain phone `6661 8628`, all four addresses and the three opening-hour lines.
- Item glossary renders 102 `<details>` rows; clicking a row opens it, and category chips filter correctly.

## 2026-11-24 — previous live release

Checked the deployed site with a cache-busting query. All lazy-loaded images were forced to load before counting.

| Page | Images | Broken | Unwanted wording | Console errors |
| --- | ---: | ---: | ---: | ---: |
| `/index.html` | 13 | 0 | 0 | 0 |
| `/plans.html` | 55 | 0 | 0 | 0 |
| `/plan-detail.html?id=e06` | 2 | 0 | 0 | 0 |
| `/centres.html` | 32 | 0 | 0 | 0 |
| `/items.html` | 1 | 0 | 0 | 0 |
| `/about.html` | 1 | 0 | 0 | 0 |
| `/partner.html` | 1 | 0 | 0 | 0 |
