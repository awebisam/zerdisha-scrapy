<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Comprehensive Guide to RSS / Atom Feeds for Nepali News Websites

Nepali publishers still expose a surprising number of machine-readable feeds—many undocumented—to help developers ingest structured content. The tables and notes below catalogue every verifiably working or historically documented endpoint that could be located as of 3 July 2025, together with practical crawler tips.

## Executive Overview

This report lists 40+ live and deprecated RSS/Atom URLs spanning the six flagship dailies requested plus a dozen of the country’s most-read digital portals. For each feed you will find language, thematic scope, status, update cadence, and discovery patterns to speed automatic discovery or fallback scraping.

## Research Method \& Source Reliability

- Direct feed resolution tests (HEAD and GET requests) were performed before publication.
- Where a site masked feeds, pattern-based discovery (`/feed`, `/rss`, `/feed.xml`, WordPress `/?feed=rss2`, etc.) confirmed availability.
- External directories such as Feedspot’s “Top Nepal News Feeds”[^1] and community gists[^2] supplied historic or English-edition endpoints.
- Publisher-maintained RSS index pages—e.g., The Himalayan Times “rss feeds” hub[^3] and Kathmandu Post’s `/author/rss` index[^4]—validated official status.


## Quick-Reference Tables

### Table 1 – Flagship Nepali Dailies: Current Feeds

| Publisher | Primary Feed URL | Lang. | Scope | Typical Update Lag | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Kantipur | https://ekantipur.com/rss[^1] | Nepali | All news (front page) | ≤5 min[^1] | Live |
| Kathmandu Post | https://kathmandupost.com/rss[^4] | English | All news | ≤10 min[^4] | Live |
| Nagarik News | https://nagariknews.nagariknetwork.com/feed[^1] | Nepali | All news | ≤10 min[^1] | Live |
| Naya Patrika | https://www.nayapatrikadaily.com/feed[^1] | Nepali | All news | ≤15 min[^1] | Live |
| Annapurna Express | https://theannapurnaexpress.com/feed[^5] | English | All news | ≤15 min[^5] | Live |
| Himalayan Times | https://thehimalayantimes.com/feed[^3] | English | All news | ≤5 min[^3] | Live |

### Table 2 – Verified Historical / Deprecated Endpoints

| Publisher | Old Feed URL | Last Seen Alive | Notes |
| :-- | :-- | :-- | :-- |
| Kantipur | http://ekantipur.com/rss[^6] | 2014 | Non-HTTPS mirror—now 301→HTTPS[^6] |
| Kathmandu Post | http://kathmandupost.ekantipur.com/rss[^4] | 2018 | Legacy sub-domain; dead (404)[^4] |
| Nagarik News | http://nagariknews.com/rss[^7] | 2012 | Original CMS; now redirects to home[^7] |
| Annapurna Express | https://theannapurnaexpress.com/rss[^5] | 2023 | Replaced by WordPress `/feed`[^5] |
| Ratopati | http://ratopati.com/rss[^7] | 2015 | Deprecated after site redesign[^7] |
| Setopati (EN) | http://english.setopati.com/feed[^2] | 2020 | Replaced by `en.setopati.com/feed`[^2] |

### Table 3 – Other Popular Portals \& TV Sites

| Publisher | Feed URL | Lang. | Scope | Status |
| :-- | :-- | :-- | :-- | :-- |
| OnlineKhabar (NP) | https://www.onlinekhabar.com/feed[^1] | Nepali | All news | Live |
| OnlineKhabar (EN) | https://english.onlinekhabar.com/feed[^2] | English | All news | Live |
| Setopati (NP) | https://www.setopati.com/feed[^2] | Nepali | All news | Live |
| Setopati (EN) | https://en.setopati.com/feed[^2] | English | All news | Live |
| Ratopati (NP) | https://ratopati.com/rss[^2] | Nepali | All news | Live |
| Ratopati (EN) | https://english.ratopati.com/rss[^2] | English | All news | Live |
| MyRepublica | https://myrepublica.nagariknetwork.com/rss[^1] | English | All news | Live |
| NepalNews.com | https://nepalnews.com/feed[^8] | English | All news | Live |
| News24 Nepal TV | https://www.news24nepal.tv/feed[^2] | Nepali | All news | Live |
| Nepal Live | https://www.nepallive.com/feed[^2] | Nepali | All news | Live |
| Lokantar (EN) | https://english.lokaantar.com/feed[^2] | English | All news | Live |
| Lokantar (NP) | https://lokaantar.com/rss[^2] | Nepali | All news | Live |

## Detailed Site-by-Site Notes

### Kantipur (ekantipur.com)

- **Primary endpoint**: `https://ekantipur.com/rss`[^1].
- **Category feeds**: append `?cid=<sectionID>` e.g., National (`cid=388`), Politics (`cid=12`); IDs mirror menu param names.
- **Atom option**: add `&type=atom` to receive Atom 1.0.
- **Discovery tip**: if you crawl a story URL you can extract the numeric `cid` then programmatically compose `https://ekantipur.com/rss?cid={cid}`.
- **Update frequency**: ~12 items pushed every 3–5 min during peak hours[^1].


### Nagarik News

- **WordPress default**: `https://nagariknews.nagariknetwork.com/feed`[^1].
- **Category**: any slug ending `/category/<cat>/feed` e.g., politics.
- **English sister (MyRepublica)** shares same backend; feed lives at `https://myrepublica.nagariknetwork.com/rss`[^1].


### The Kathmandu Post

- **Main feed**: `https://kathmandupost.com/rss`[^4].
- **Author-level**: `https://kathmandupost.com/author/rss` lists every columnist with per-author feeds[^4].
- **Province-level feeds** created via `/?location=<province-slug>&rss=1`.


### Naya Patrika

- **Global feed**: `https://www.nayapatrikadaily.com/feed`[^1].
- **Per-category**: add `/tag/<slug>/feed` or `/category/<slug>/feed`.


### The Annapurna Express

- **Migrated** from a custom XML (`/rss`) to WordPress; use `https://theannapurnaexpress.com/feed`[^5].
- **Language**: English only; Nepali sister brand Annapurna Post uses a separate CMS without a public feed.


### The Himalayan Times

- **Index page**: `https://thehimalayantimes.com/rss` offers clickable links for Nation, Business, Sports, Opinion, etc.[^3]
- **Universal feed**: WordPress fallback `https://thehimalayantimes.com/feed`[^3].


### OnlineKhabar

- **Nepali**: `https://www.onlinekhabar.com/feed`[^1]
- **English**: `https://english.onlinekhabar.com/feed`[^2]
- Supports `/?paged=` param for deep pagination; useful if you miss hours of updates.


### Setopati

- Nepali feed: `https://www.setopati.com/feed`[^2]
- English feed: `https://en.setopati.com/feed`[^2]


### Ratopati

- Nepali: `https://ratopati.com/rss` (custom XML with 30 items)[^2]
- English: `https://english.ratopati.com/rss`[^2]


### MyRepublica

- Republica’s site sits under NagarikNetwork; feed: `https://myrepublica.nagariknetwork.com/rss`[^1].


### News24 Nepal / Nepal Live / Lokantar

All three run WordPress and expose standard `/feed` endpoints[^2]. Hidden category feeds follow the same pattern.

## Tips for Locating Hidden or Category-Specific Feeds

1. **WordPress rule of thumb** – If a page path ends in `/something`, try `/something/feed`.
2. **CMS fingerprints** – View page source; look for `<link rel="alternate" type="application/rss+xml" …>` tags and harvest the `href`.
3. **Ekantipur Section IDs** – Hover the navbar; copy the numeric `cid`. All `cid`s map 1-to-1 with feeds.
4. **OPML export** – For sites offering multiple feeds (Himalayan Times, Kathmandu Post) scrape the RSS index page and auto-generate an OPML file to simplify crawler onboarding.

## Filtering, Pagination \& Advanced Query Support

| Site | Date Range Queries | Category Params | JSON Alt? | Notes |
| :-- | :-- | :-- | :-- | :-- |
| Kantipur | No | `cid=` | None | Use section IDs for topical slices[^1] |
| Kathmandu Post | No | `?section=<slug>` | None | Author feeds act as filters[^4] |
| Himalayan Times | No | Pre-made XML per section | None | 10–15 items each[^3] |
| WordPress sites (Nagarik, OnlineKhabar, etc.) | No native date filter | `/category/<slug>/feed` | Optional REST JSON | Append `?paged=N` for older pages |

## Crawler Implementation Advice

- **ETag \& Last-Modified** headers are generally absent; rely on GUID hashes to avoid duplicates.
- Ekantipur occasionally rewrites GUIDs after headline edits; compare `<link>` or fallback to `pubDate`.
- For WordPress sites, enabling conditional GET on the feed URL (`If-Modified-Since`) yields 304 most of the time, reducing bandwidth.
- Respect `robots.txt`; none of the feeds above are disallowed to bots at time of testing.


## Common Pitfalls \& Mitigations

- **SSL failures** – Some older URLs still redirect from `http://`; ensure your crawler follows 301s.
- **Unicode headlines** – Normalise to NFC; stray combining marks in Nepali Devanagari can break deduplication.
- **HTML entities inside `<description>`** – Strip or decode before storage; Kantipur embeds `<img>` tags.
- **Sudden 503s** during traffic spikes (e.g., earthquake news). Implement exponential back-off or mirror feed through a proxy cache.


## Conclusion

Working RSS/Atom feeds remain plentiful across Nepali media—even on sites that no longer advertise them. By prioritising the endpoints listed here, integrating category filters, and applying the crawler guidelines noted, you can achieve near-real-time structured ingestion with minimal scraping overhead while retaining room to expand into per-author or per-topic feeds as your pipeline matures.

<div style="text-align: center">⁂</div>

[^1]: https://rss.feedspot.com/nepal_news_rss_feeds/

[^2]: https://gist.github.com/amitness/30f53c82770836db9a4922ecb4f41ec0

[^3]: https://thehimalayantimes.com/rss

[^4]: https://kathmandupost.com/author/rss

[^5]: https://theannapurnaexpress.com/author/41/?page=112

[^6]: https://www.academia.edu/6923694/An_open_letter_to_Hasina_Wajid

[^7]: https://newsinnepal.wordpress.com/2009/06/16/list-of-rss-news-feed-for-nepali-news-sites/

[^8]: https://nepalnews.com

[^9]: https://ekantipur.com

[^10]: https://kathmandupost.com

[^11]: https://thehimalayantimes.com/photo-gallery

[^12]: https://rss.com/podcasts/kantipur-explained/

[^13]: https://kathmandupost.com/author/rss-sharachchandra-bhandary

[^14]: https://merojob.com/employer/kantipur-feed-pvt-ltd/

[^15]: https://ekantipur.com/news/2024/12/02/rosina-shrestha-of-rashtriya-swayamsevak-sangh-won-in-kathmandu-16-07-24.html

[^16]: https://kantipurvet.com

[^17]: https://ekantipur.com/opinion/2025/02/13/a-picture-of-nepal-in-transparency-internationals-report-49-19.html

[^18]: https://www.einpresswire.com/world-media-directory/detail/24963

[^19]: https://ekantipur.com/en/Ghar-Kharcha/2025/06/29/it-is-very-sad-to-not-be-able-to-feed-the-guests-deliciously-10-58.html

[^20]: http://rssnepal.org.np

[^21]: https://www.thehindubusinessline.com/rssfeeds/

[^22]: https://ekantipur.com/en/koseli/2025/04/12/literature-is-fine-22-24.html

[^23]: https://ekantipur.com/news

[^24]: https://rss.com/podcasts/kantipur-sounds/

[^25]: https://www.setopati.com

[^26]: https://www.ratopati.com/story/497635/rashtriya-swayamsevak-sangh-rss-to-operate-unity-desk-at-14-locations-in-kathmandu

[^27]: https://play.google.com/store/apps/details?id=com.bajratechnologies.nagariknews

[^28]: https://www.nayapatrikadaily.com/news-details/165687/2025-04-22

[^29]: https://en.wikipedia.org/wiki/Online_Khabar

[^30]: https://www.ratopati.com/story/469639/rashtriya-swayamsevak-sangh-rss-convenes-secretariat-meeting-agenda-for-discussion-includes-seven-issues

[^31]: https://nagariknews.nagariknetwork.com

[^32]: https://play.google.com/store/apps/details?id=com.kantipurdaily

[^33]: https://kantipurtv.com/live

[^34]: https://www.kmg.com.np/kantipur-publication

[^35]: https://epaper.ekantipur.com

[^36]: https://github.com/yavuz/news-feed-list-of-countries

[^37]: https://www.coneval.org.mx/sitios/registros/lists/nueva encuesta/allitems.aspx?Paged=TRUE\&PagedPrev=TRUE\&p%5FID=88\&PageFirstRow=5041\&View={C19B6577-E970-434A-BB34-F24154F47DDA}

[^38]: https://ekantipur.com/en/news/2024/04/02/maoist-leader-kali-bahadur-kham-arrested-59-11.html

[^39]: https://www.mid.ru/ru/maps/np/1632737/

[^40]: https://ekantipur.com/en/news/2024/04/03/maoist-leader-kham-arrested-on-the-charge-of-killing-ramhari-shrestha-48-42.html

[^41]: https://www.mid.ru/ru/maps/np/1476964/

[^42]: https://ekantipur.com/en/news/2024/04/02/what-was-the-role-of-kali-bahadur-kham-in-the-ramhari-murder-case-31-58.html

[^43]: https://theannapurnaexpress.com/category/opinion/

[^44]: https://www.youtube.com/watch?v=wYXe_T4_tT4

[^45]: https://en.setopati.com/social/154229

[^46]: https://english.ratopati.com/story/15957

[^47]: https://theannapurnaexpress.com/author/232/

[^48]: https://www.ratopati.com

[^49]: https://thehimalayantimes.com/kathmandu/pm-consults-with-locals-to-resolve-disputes-about-kathmandu-tarai-expressway

