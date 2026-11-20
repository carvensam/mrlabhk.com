# Browser visual QA

Date: 2026-11-20

Checked the live site with a cache-busting query. All lazy-loaded images were forced to load before counting.

| Page | Images | Broken | Unwanted wording |
| --- | ---: | ---: | ---: |
| `/index.html` | 7 | 0 | 0 |
| `/plans.html` | 55 | 0 | 0 |
| `/plan-detail.html?id=e06` | 2 | 0 | 0 |
| `/centres.html` | 1 | 0 | 0 |
| `/about.html` | 1 | 0 | 0 |
| `/partner.html` | 1 | 0 | 0 |

Console errors: 0 on all six pages.

E06 detail and centre pages show the corrected E Plus phone `6661 8628` and full four-branch addresses.
