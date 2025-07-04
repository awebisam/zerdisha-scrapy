## How a Team of AI Bots Built This Thing (The Special Edition)

This whole thing started as a "what if?" idea during a chat with Gemini: could a team of AIs, managed by another AI, build a data scraping tool for Nepali news sites? We dove in headfirst to find out.

What followed was a masterclass in AI collaboration, with a surprisingly high success rate and a few tricky edge cases that showed where a human's touch is still key.

---

### The Crew: The Official Cast List

- **Gemini CLI (The Boss with a Megaphone):**  
  The project manager. Used the GitHub CLI (`gh`) to create issues, assign tasks, and even drop comments in Pull Requests to guide the developer bot. All issues, assignments, approvals, and even the "human" commits were orchestrated through Gemini prompts—never directly.
- **GitHub Copilot (The Coder in the Basement):**  
  The main developer. Once assigned an issue, it worked quietly in the background to write all the Python code and tests.
- **VSCode Copilot Agent (The Fixer):**  
  The specialist for quick, in-editor fixes, like tweaking type definitions, fixing lints, and handling stubborn edge cases on the fly.
- **Perplexity/Manus (The Research Intern):**  
  The scout sent to find RSS feeds and selectors for each Nepali news site. Mostly reliable, but sometimes missed local quirks or special URL rules.

---

### The Real Workflow: Smooth Sailing and... Hiccups

The AI team started strong. The initial project setup, the data cleaning pipelines, and even the first few spiders were built flawlessly. **Most of the news sites didn't require any human help at all.**

But then we hit the inevitable, real-world snags.

---

#### 🕷️ Part 1: When The Robots Got Confused (The Spider Quirks)

A few sites, namely **Naya Patrika, Annapurna Express,** and **The Himalayan Times**, had unique fingerprints that the initial AI research missed. For instance:
- Annapurna's RSS feed was `/rss` instead of `/feed`
- The Himalayan Times used a complex, category-based RSS structure.
- Naya Patrika had quirky content selectors that threw Copilot off.

For these cases, we ran a feedback loop:  
A human would spot the quirk, use Gemini to comment on the PR, and Copilot would read the comment and fix its own code.  
This loop was repeated for each tricky site until the spiders were robust.

- [Issue #8: Naya Patrika Spider](https://github.com/awebisam/zerdisha-scrapy/issues/8) | [PR #15](https://github.com/awebisam/zerdisha-scrapy/pull/15)
- [Issue #9: Annapurna Express Spider](https://github.com/awebisam/zerdisha-scrapy/issues/9) | [PR #14](https://github.com/awebisam/zerdisha-scrapy/pull/14)
- [Issue #10: The Himalayan Times Spider](https://github.com/awebisam/zerdisha-scrapy/issues/10) | [PR #13](https://github.com/awebisam/zerdisha-scrapy/pull/13)

---

#### ☁️ Part 2: The Real-World Bottleneck (A Zyte Cloud Story)

This was the big one. The whole plan hinged on hosting the project on **Zyte Scrapy Cloud**, for a very simple reason: it was free with the GitHub Student Developer Pack.

The "gotcha"? Zyte Cloud only supported Python 3.8.

The AI, by default, had written beautiful, modern Python 3.9+ code. All the simple, clean type hints like `list[str]` and `dict[str, int]` were suddenly invalid. The entire codebase was incompatible with our mandatory deployment environment.

This led to [Issue #11](https://github.com/awebisam/zerdisha-scrapy/issues/11):  
> Downgrade Python to 3.8 for Compatibility

Copilot was tasked with a full project refactor:  
Every single file in the project needed its type hints re-written—goodbye, modern Python, hello, `typing.List` and `typing.Dict`.  
This was a tedious, project-wide change, but Copilot executed it perfectly via [PR #12](https://github.com/awebisam/zerdisha-scrapy/pull/12).

It was a powerful reminder that real-world deployment can trump even the most elegant code.

---

### So, What's the Holdup?

If you're wondering why a PR is still open, we've hit a classic budget issue:  
I've completely burned through my monthly quota of GitHub Copilot requests.

Our star developer is on a mandatory, unpaid vacation until the credits reset.

---

### The Big Takeaways

- A highly effective **AI team** can handle most tasks autonomously, including complex multi-source scraping.  
- The **human role** is orchestration: navigating unique exceptions, platform-specific bottlenecks, and the occasional research miss.
- **Traceability:** Every issue and PR (even those with "human" authorship) was created via Gemini CLI automation and handled by Copilot, so the whole workflow is AI-driven and auditable.
- **Real-world constraints** (like hosting limitations and API quotas) are the ultimate equalizer.

---

_This PROCESS.md was drafted by Copilot based on the actual project history. For a full play-by-play, check the [issues](https://github.com/awebisam/zerdisha-scrapy/issues) and [pull requests](https://github.com/awebisam/zerdisha-scrapy/pulls)._
