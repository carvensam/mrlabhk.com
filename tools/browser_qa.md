# Browser visual QA

## 2026-11-25 — E06 plan removed

Removed `e06` / 醫家 EPH2.0 升級檢查計劃（58項）from `data/featured.js`, together with `assets/images/e06.webp` and its build-tool references. Featured plans are now `e01`–`e05`; image references total 53. Validators no longer check E06 phone or addresses. With no remaining plan, 醫家健康體檢中心 no longer appears in the centre list.

- `tools/validate_site.py`: `pages=7 plans=48 featured=5 images=53`, `errors=0 warnings=0`.

## 2026-11-25 — wording update

Replaced all second-person singular and plural wording in site copy with `大家`, including WhatsApp prefill text and the DNS setup note. A full repository search now returns 0 matches for the old second-person forms.

## 2026-11-25 — mobile header WhatsApp alignment

The top-right WhatsApp button was overflowing on narrow screens because the inline SVG had no fixed size and the header kept desktop gaps while showing the full label.

- `assets/js/app.js`: the header CTA label is wrapped in `.header-cta-label` and the link has `aria-label="WhatsApp 查詢"`.
- `assets/css/style.css`: header SVG is fixed at 18×18 with `line-height: 1`; at `max-width: 760px` the header gap is 10px, the label is hidden and the CTA becomes a 36×36 green circle pinned to the right edge.
- All 7 pages now load `style.css?v=20261125b` and `app.js?v=20261125c` so cached copies cannot keep the old header layout.
- Simulated 375px and 320px layout: brand, menu toggle and WhatsApp circle all stay inside the header container; WhatsApp sits at the far right with no horizontal overflow.
- `tools/validate_site.py`: `pages=7 plans=48 featured=6 images=54`, `errors=0 warnings=0`; 0 console errors.

## 2026-11-25 — browser/meta icon replacement

Deployed in `bce1853` with a follow-up root `favicon.ico` fallback. The browser/meta icon was rebuilt from `assets/images/logo-mrlab.png`. All 7 pages now link to versioned `favicon.ico?v=20261125`, `favicon.svg?v=20261125`, `favicon.png?v=20261125` and `apple-touch-icon`.

- Local QA: 7/7 pages returned all four icon links with status 200, matching MIME types and valid ICO/PNG headers; 0 console errors.
- `tools/validate_site.py`: `pages=7 plans=48 featured=6 images=54`, `errors=0 warnings=0`.
- Live QA used `fetch` with `cache: 'no-store'` to bypass the CDN HTML cache: 7/7 pages returned the new versioned icon links and all icon assets returned status 200.
- Live `favicon.svg` contains the embedded MR Lab logo data and no longer contains the previous heartbeat mark; live `favicon.png` is 17,170 bytes with valid PNG header bytes.
- Live root `favicon.ico` now returns `image/x-icon` at 12,045 bytes; before this follow-up it returned 404.
- `tools/verify_live.py` now recognises ICO magic bytes; final run: `errors=0 image_failures=0 ssl_ok=True`; 88 live images checked, no failures.
- The host sends `Cache-Control: max-age=600` for HTML. A hard refresh or a fresh tab may be needed once before an old cached tab shows the new browser icon.

## 2026-11-25 — centre logo rebuild, live verification

Deployed commit `9f99665` (includes the `00aea66` logo rebuild). Checked the live site with a cache-busting query. All lazy-loaded images were forced to load before counting.

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

- `tools/verify_live.py`: `errors=0 image_failures=0 ssl_ok=True`; 85 live images checked, no failures.
- All 31 centre thumbnails are uniform 640×240 PNGs, fully inside the canvas with no clipping or edge contact.
- Logo identity was re-checked against each centre’s official website and recorded in `tools/logo_sources.json`; centres without a standalone centre-specific mark use an exact-name wordmark.
- Index 27 (`香港仁和體檢`) uses the darker official re:HEALTH asset so it remains legible on the light panel.
- Index 20 (`明德醫療中心`) uses an exact-name wordmark because no centre-specific mark is published; index 22 (`聯合醫務`) uses the corporate site’s transparent UMP logo.
- Final automated audit: 30 manifest entries, 31 valid PNGs, 31 mapping refs, 0 banned wording, and WhatsApp numbers limited to `85246151993`.
- Centre order is `香港生物醫學核心化驗所` → `醫家健康體檢中心` → `美邦醫學體檢中心`.
- Homepage slogan renders as `回饋社會．全民體檢`.
- Centre cards contain no authorisation / booking sentences; the required note remains on plan cards, plan detail and WhatsApp prefill.
- Every WhatsApp link uses `https://wa.me/85246151993` and renders in official green.
- Footer shows only `WhatsApp / 電話：4639 4019` and `電郵：info@welldonemarketinghk.com`; no old phone, Gmail or Facebook copy.
- E06 detail and centre pages retain phone `6661 8628`, all four addresses and the three opening-hour lines.
- Item glossary renders 102 `<details>` rows; clicking a row opens it, and category chips filter correctly.

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
