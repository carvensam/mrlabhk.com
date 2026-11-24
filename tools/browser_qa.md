# Browser visual QA

Date: 2026-11-24

Checked the local build of the deployment repo with a threaded static server. All lazy-loaded images were forced to load before counting.

| Page | Images | Broken | Unwanted wording | Console errors |
| --- | ---: | ---: | ---: | ---: |
| `/index.html` | 13 | 0 | 0 | 0 |
| `/plans.html` | 55 | 0 | 0 | 0 |
| `/plan-detail.html?id=e06` | 2 | 0 | 0 | 0 |
| `/centres.html` | 32 | 0 | 0 | 0 |
| `/items.html` | 1 | 0 | 0 | 0 |
| `/about.html` | 1 | 0 | 0 | 0 |
| `/partner.html` | 1 | 0 | 0 | 0 |

Additional checks:

- Homepage slogan renders as `回饋社會．全民體檢`.
- Centre order is `香港生物醫學核心化驗所` → `醫家健康體檢中心` → `美邦醫學體檢中心`.
- Centre cards contain no authorisation / booking sentences; the required note remains on plan cards, plan detail and WhatsApp prefill.
- Every WhatsApp link uses `https://wa.me/85246151993` and renders in official green `rgb(37, 211, 102)`.
- Footer shows only `WhatsApp / 電話：4639 4019` and `電郵：info@welldonemarketinghk.com`; no old phone, Gmail or Facebook copy.
- E06 detail and centre pages retain phone `6661 8628`, all four addresses and the three opening-hour lines.
- Item glossary renders 102 `<details>` rows; clicking a row opens it, and category chips filter correctly.
