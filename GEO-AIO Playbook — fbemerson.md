# GEO/AIO Playbook — fbemerson.com

*Compiled by Murph (AI Chief of Staff) | February 2026*
*Project: fbemerson.com — F.B. Emerson Author Site*

---

## Executive Summary: What Actually Matters

**The BBC experiment that should wake you up:** On February 18, 2026, BBC journalist Thomas Germain spent 20 minutes writing a single fake blog post claiming he was the world's greatest hot-dog-eating tech journalist. Less than 24 hours later, ChatGPT, Google Gemini, and Google AI Overviews were all repeating it as fact. Claude (Anthropic) was the only AI that wasn't fooled.

**The core mechanism:** AI search engines don't verify — they synthesize. When they get a query, they pull live web content (via RAG — Retrieval-Augmented Generation), find pages that appear authoritative and well-structured, and quote them. A single, well-formatted page can become THE source on a topic if there's little competition.

**The strategic flip:** In traditional SEO, you fight for position 1-10 on a results page. In GEO, you fight to become the content AI synthesizes into its ONE answer. You're not competing for a ranking — you're competing to be the source of truth AI inherits and repeats.

**The three things that matter most (in order):**

1. **Authoritative, structured content that AI can extract** — answer-first format, listicles, tables, FAQ sections with proper schema
2. **Third-party mention velocity** — being cited/mentioned on Reddit, LinkedIn, press outlets, and other trusted sources
3. **Entity consistency** — F.B. Emerson showing up with the same name, attributes, and associations everywhere

**The counterintuitive truth:** 80% of sources cited by AI platforms do NOT appear in Google's top organic results. Only 12% of AI citations match Google's top rankings. AI search is a different game.

---

## Part 1: The Mechanics

### 1. How AI Search Systems Actually Work

#### The Two Modes: Training Data vs. RAG

**Training Data (Baked-In Knowledge):**
- What the model learned during training from massive web crawls, books, Wikipedia, Reddit, news sites
- Models like Claude, GPT-4, Gemini have knowledge cutoffs — you CANNOT influence existing training data directly
- BUT: By building a strong web presence now, you influence what future model versions learn

**RAG (Retrieval-Augmented Generation) — What you can influence right now:**
- When a user asks ChatGPT Browse, Google AI Overviews, or Perplexity a question, they run a live web search first, retrieve relevant pages, then synthesize an answer
- This real-time retrieval is where GEO tactics have immediate impact

**Practical implication:** RAG-based AI search is optimizable TODAY. fbemerson.com's content can appear in AI answers within 24-48 hours if it's indexed and formatted correctly.

#### The RAG Pipeline (How F.B. Emerson Gets Cited)

1. User asks: "Who is F.B. Emerson?" or "What are good books about [genre]?"
2. AI expands query into variations
3. Retrieves top pages for each variation
4. Runs reranking (rewards comprehensive, authoritative passages)
5. Synthesizes an answer from the highest-ranked content
6. Cites sources (sometimes)

---

### 2. Entity Building — Making F.B. Emerson a Recognized Author Entity

This is the MOST important section for fbemerson.com. For an author site, entity building IS the strategy. AI systems need to recognize F.B. Emerson as a distinct, identifiable author entity.

#### Entity Building Strategy for F.B. Emerson

**Core Steps:**

1. **Consistent Name:** "F.B. Emerson" — same name everywhere. Not "FB Emerson", not "F. B. Emerson" with spaces. Pick one format and use it consistently.
2. **Wikipedia/Wikidata:** If eligible (legitimate notability through published works, press coverage), pursue a Wikipedia page. At minimum, claim a Wikidata entry.
3. **Google Knowledge Panel:** Claim it via Google Search Console. Author Knowledge Panels are triggered by consistent signals across Amazon, Goodreads, LinkedIn, and the author's own site.
4. **Goodreads Author Profile:** Critical — Goodreads is a high-authority entity source for authors that AI systems trust.
5. **Amazon Author Central:** Complete your Author Central profile. Amazon is heavily crawled by AI systems.
6. **Person Schema on your site:** The foundation of everything — tells AI exactly who F.B. Emerson is.

#### Entity Attributes to Establish

- **What F.B. Emerson IS:** Author, fiction writer
- **What F.B. Emerson DOES:** Writes books (specify genre)
- **Who F.B. Emerson is ASSOCIATED WITH:** Book titles, genre, publishing world
- **WHERE F.B. Emerson is based:** Location if relevant
- **Key works:** List of published books

#### The sameAs Property Is Critical for Authors

```json
{
  "@type": "Person",
  "name": "F.B. Emerson",
  "url": "https://fbemerson.com",
  "sameAs": [
    "https://www.goodreads.com/author/show/[id]/F_B_Emerson",
    "https://www.amazon.com/author/fbemerson",
    "https://www.linkedin.com/in/cjemerson",
    "https://twitter.com/fbemerson"
  ]
}
```

This `sameAs` graph tells AI systems that all these profiles are the SAME person.

---

### 3. Structured Data / Schema Markup for fbemerson.com

#### Priority Schema Types

**Tier 1 — Foundation (Author Identity):**
- `Person` — F.B. Emerson as author (THE most important schema for this site)
- `WebSite` — establishes site entity
- `BreadcrumbList` — site structure signals

**Tier 2 — Content:**
- `Article` or `BlogPosting` — with proper author, datePublished, dateModified
- `FAQPage` — for FAQ sections

**Tier 3 — fbemerson.com-Specific:**
- `Book` — for EACH published book (with author, description, genre, offers)
- `ItemList` — for book series or collected works
- `CreativeWork` — for broader creative output
- `AggregateRating` — for book reviews

**Tier 4 — Advanced:**
- `SpeakableSpecification` — tells AI voice assistants which content to read aloud

#### Person Schema (The Most Important Schema for This Site)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "F.B. Emerson",
  "givenName": "F.B.",
  "familyName": "Emerson",
  "jobTitle": "Author",
  "description": "F.B. Emerson is a fiction author known for [genre/key themes]. [Additional credential].",
  "url": "https://fbemerson.com",
  "image": "https://fbemerson.com/images/fb-emerson.jpg",
  "sameAs": [
    "https://www.goodreads.com/author/show/[id]/F_B_Emerson",
    "https://www.amazon.com/author/fbemerson",
    "https://www.linkedin.com/in/cjemerson"
  ],
  "knowsAbout": ["fiction writing", "[genre]", "[themes]"]
}
```

#### Book Schema (Create One Per Book)

```json
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "[Book Title]",
  "author": {
    "@type": "Person",
    "name": "F.B. Emerson"
  },
  "description": "[Book description — 2-3 sentences]",
  "url": "https://fbemerson.com/books/[book-slug]",
  "genre": "[Genre]",
  "inLanguage": "en",
  "offers": {
    "@type": "Offer",
    "price": "[Price]",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[4.X]",
    "reviewCount": "[N]",
    "bestRating": "5"
  }
}
```

#### ItemList Schema (For Book Series)

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Books by F.B. Emerson",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "item": {
        "@type": "Book",
        "name": "[Book Title 1]",
        "url": "https://fbemerson.com/books/[slug]"
      }
    }
  ]
}
```

#### FAQPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Who is F.B. Emerson?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "F.B. Emerson is a fiction author known for [genre/key themes]. [Key accomplishment or unique attribute]. Find all of F.B. Emerson's published works at fbemerson.com."
      }
    },
    {
      "@type": "Question",
      "name": "What books has F.B. Emerson written?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[List of books with brief descriptions]."
      }
    }
  ]
}
```

---

### 4. Content Structure — How to Write So AI Cites F.B. Emerson

#### The 12 Proven Tactics Applied to an Author Site

**1. Listicles & Tables**
- Example: "Complete List of F.B. Emerson Books in Reading Order" with a table (title, genre, publication date, description)

**2. Answer-First Formatting**
- Bad: "F.B. Emerson's journey as an author began many years ago..."
- Good: "F.B. Emerson is a fiction author whose works explore [themes]. His published books include [title 1], [title 2], and [title 3]."

**3. Long-Form Content**
- Create detailed book pages (2,000+ words) with synopsis, themes, characters, reading guides
- Behind-the-scenes writing process posts

**4. Original Content**
- Author interviews, reading guides, world-building notes — content that only F.B. Emerson can create

**5. Quantitative Claims**
- "[X] readers on Goodreads", "[X]-star average rating", "[X] books published"

**6. Content Freshness**
- Update book pages when new reviews come in
- Blog about upcoming works, events

**7-12. Schema, E-E-A-T, Deep Pages, External Mentions, FAQ, Tracking**
- All apply as described in the general mechanics

#### Key Pages to Create

- `/books` — Complete bibliography with Book schema for each
- `/books/[title]` — Dedicated page per book (synopsis, themes, reviews, purchase links)
- `/about` — Author bio with Person schema
- `/faq` — "Who is F.B. Emerson?", "What genre does F.B. Emerson write?", etc.
- `/reading-order` — If applicable, recommended reading order
- `/blog` — Regular author updates for freshness signals

---

### 5. Citation Building for F.B. Emerson

#### Key Building Blocks

- **Goodreads profile** — Complete, with all books listed, author bio, profile photo
- **Amazon Author Central** — Complete profile, editorial reviews
- **Wikipedia** — If eligible based on press coverage and notability
- **LibraryThing** — Author profile
- **BookBub** — Author profile

#### Reddit Strategy

**Target Subreddits:**
- r/books
- r/[genre-specific] (e.g., r/Fantasy, r/scifi, r/romance depending on genre)
- r/writing
- r/selfpublish (if self-published)

**Tactics:**
- Participate in book discussions genuinely
- Do AMA threads: "I'm F.B. Emerson, author of [title], AMA"
- Share writing insights and process

#### LinkedIn Strategy

- Build CJ/F.B. Emerson's profile as a published author
- Publish articles about the writing process, book themes, or industry insights

#### Press & Media

- Book reviews in genre publications
- Author interviews on book blogs and podcasts
- HARO responses on writing/publishing topics

---

### 6. Topical Authority for an Author Site

#### Content Architecture

**Hub:** "About F.B. Emerson — Author" (comprehensive author page)

**Spokes:**
- Individual book pages with deep content
- Genre exploration posts (establish expertise in your genre)
- Writing process / behind-the-scenes content
- Reading guides and recommendations
- Book-related FAQ

**Topical Coverage:** Author entity, fiction writing, [book-specific topics], [genre]

---

### 7. Technical Site Signals

#### LLMs.txt for fbemerson.com

```markdown
# F.B. Emerson
## Key Resources
- [Books](/books): Complete bibliography of F.B. Emerson's published works
- [About the Author](/about): F.B. Emerson's background, influences, and writing career
- [FAQ](/faq): Common questions about F.B. Emerson and his books

## About This Site
fbemerson.com is the official website of F.B. Emerson, a fiction author known for [genre/themes]. The site features his complete bibliography, author background, and reading guides.
```

#### robots.txt

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /

Sitemap: https://fbemerson.com/sitemap.xml
```

---

## Part 2: fbemerson.com-Specific Strategy

- **Dominant entity:** F.B. Emerson as author
- **Key queries to own:** "F.B. Emerson", "F.B. Emerson books", "[specific book title]"
- **Quick win:** Person schema + Book schema for each title
- **Key building blocks:** Goodreads profile, Amazon Author Central, Wikipedia if eligible
- **Schema priorities:** Person, Book, ItemList (book series), CreativeWork

---

## Part 3: Action Plan

### Quick Wins (This Week)

1. **robots.txt audit** — Make sure you're NOT blocking GPTBot, PerplexityBot, ClaudeBot
2. **Add Person schema** for F.B. Emerson — THE most important schema for an author site
3. **Add Book schema** for each published title
4. **Add datePublished + dateModified** to all content
5. **Create /llms.txt** for fbemerson.com
6. **Manual AI audit** — ask ChatGPT, Perplexity, Google AI "Who is F.B. Emerson?"
7. **Complete Goodreads profile** — if not already done
8. **Complete Amazon Author Central** — if not already done

### 30-Day Wins

1. **Reddit presence** — Participate in genre-relevant subreddits, do an AMA
2. **LinkedIn articles** — Publish articles about writing, book themes, genre insights
3. **FAQ page** — Create dedicated /faq with 20+ questions (about the author, books, writing process)
4. **Update book pages** — Add reviews, reader feedback, deeper content
5. **Individual book pages** — Ensure each book has a dedicated page with full schema
6. **Internal linking** — Connect all book pages, about page, blog posts

### Long-Term Plays (3-6 Months)

1. **Author entity building** — Wikidata entry, consistent sameAs across all platforms
2. **Press/reviews** — Get books reviewed on genre blogs, podcasts, publications
3. **Reddit community** — Become a valued contributor in book/genre subreddits
4. **YouTube/podcast** — Author interviews, writing process content
5. **Genre authority content** — Blog posts establishing expertise in your genre space
6. **Co-citation network** — Get included in "best [genre] books" lists and reading recommendations
7. **Wikipedia** — If notability criteria are met, pursue a Wikipedia page

---

## Part 4: Claude Code Master Prompt (Pre-Filled for fbemerson.com)

Copy-paste this into any Claude Code session building the fbemerson.com website:

```
# GEO/AIO OPTIMIZATION MASTER PROMPT — fbemerson.com

## CONTEXT
This website is fbemerson.com, the official author site for F.B. Emerson. Every implementation
decision should maximize the site's visibility in AI search engines.

The core principle: AI search engines retrieve and synthesize web content in real-time (RAG).
They favor structured, authoritative, factually dense content. Your job is to make F.B.
Emerson's author presence as extractable, authoritative, and entity-clear as possible.

## PROJECT DETAILS
- Site: fbemerson.com
- Brand entity: F.B. Emerson is a fiction author known for [genre/themes/key works]
- Core topic cluster: Author entity, fiction writing, [genre], [book-specific themes]
- Author/Expert entity: F.B. Emerson (pen name of CJ Emerson)
- Target audience: Readers of [genre], book discovery audiences, fiction enthusiasts

## MANDATORY TECHNICAL IMPLEMENTATIONS

### 1. robots.txt
```
User-agent: GPTBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: *
Allow: /
Sitemap: https://fbemerson.com/sitemap.xml
```

### 2. Create /llms.txt
```markdown
# F.B. Emerson
## Core Resources
- [Books](/books): Complete bibliography of F.B. Emerson's works
- [About the Author](/about): Background, influences, and writing career
- [FAQ](/faq): Common questions about F.B. Emerson and his books

## About This Site
fbemerson.com is the official website of F.B. Emerson, a fiction author. The site features his complete bibliography, author information, and reading guides.

## Key Facts
- Author: F.B. Emerson
- Genre: [Genre]
- Published works: [Number of books]
```

### 3. Sitewide JSON-LD Schema

#### Person Schema (THE Critical Schema):
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "F.B. Emerson",
  "givenName": "F.B.",
  "familyName": "Emerson",
  "jobTitle": "Author",
  "description": "F.B. Emerson is a fiction author known for [genre/themes].",
  "url": "https://fbemerson.com",
  "image": "https://fbemerson.com/images/fb-emerson.jpg",
  "sameAs": [
    "https://www.goodreads.com/author/show/[id]/F_B_Emerson",
    "https://www.amazon.com/author/fbemerson",
    "https://www.linkedin.com/in/cjemerson"
  ],
  "knowsAbout": ["fiction writing", "[genre]", "[themes]"]
}
```

#### Book Schema (one per book):
```json
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "[Book Title]",
  "author": {
    "@type": "Person",
    "name": "F.B. Emerson"
  },
  "description": "[Book description]",
  "url": "https://fbemerson.com/books/[slug]",
  "genre": "[Genre]",
  "inLanguage": "en",
  "offers": {
    "@type": "Offer",
    "price": "[Price]",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[4.X]",
    "reviewCount": "[N]",
    "bestRating": "5"
  }
}
```

#### FAQPage Schema:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Who is F.B. Emerson?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "F.B. Emerson is a fiction author known for [genre/themes]. His published works include [titles]."
      }
    },
    {
      "@type": "Question",
      "name": "What books has F.B. Emerson written?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Complete list with brief descriptions]."
      }
    }
  ]
}
```

### 4. Content Structure Requirements

```
[H1 — Author name or book title, clear and direct]

[DIRECT ANSWER — Who F.B. Emerson is and what he writes, in 40-60 words]

[H2 — "Who Is F.B. Emerson?"]
[Direct author bio with credentials]

[H2 — "What Books Has F.B. Emerson Written?"]
[Complete bibliography table]

[H2 — "Frequently Asked Questions"]
[FAQ with schema]
```

### 5. Technical Checklist
- [ ] robots.txt allows all AI crawlers
- [ ] /llms.txt created
- [ ] XML sitemap submitted
- [ ] HTTPS on all pages
- [ ] Person schema for F.B. Emerson
- [ ] Book schema for each published work
- [ ] ItemList schema for complete bibliography
- [ ] FAQPage schema on key pages
- [ ] Goodreads sameAs link
- [ ] Amazon Author Central sameAs link
- [ ] datePublished/dateModified on all content
- [ ] Author bio on every page
- [ ] Internal linking complete
- [ ] Canonical tags on all pages
- [ ] AggregateRating on book pages with reviews

## IMPLEMENTATION PRIORITY ORDER

### Phase 1 (Launch Blockers):
1. robots.txt with AI crawler permissions
2. HTTPS
3. Person schema for F.B. Emerson
4. /llms.txt

### Phase 2 (First Week):
5. Book schema for each title
6. FAQPage schema on key pages
7. /faq dedicated page
8. Author bio optimized answer-first
9. Goodreads + Amazon Author Central profiles complete

### Phase 3 (First Month):
10. Full FAQ expansion (20+ questions)
11. Individual book pages with deep content
12. ItemList schema for bibliography
13. AggregateRating schema on book pages
14. Content freshness protocol

### Phase 4 (Ongoing):
15. Blog posts for freshness
16. Genre authority content
17. Monthly page updates
18. Track AI visibility
```

---

## Appendix: AI Search Quick Reference

### Key Statistics to Know

| Metric | Data |
|--------|------|
| LLM traffic growth | 800% YoY (Semrush, 2025) |
| Listicle citation rate | 50% of top AI citations |
| Table citation boost | 2.5x vs. unstructured |
| Long-form citation rate | 3x more than short posts |
| Original research citation share | 67% of ChatGPT's top 1,000 |
| Quantitative claim advantage | 40% higher citation rate |
| Content freshness window | 76.4% updated in last 30 days |
| Schema markup boost | 3-5x more AI recommendations |
| External citation multiplier | 6.5x more likely with third-party mentions |
| AI citation vs Google rankings | 80% of AI sources NOT in Google top results |

### The Platforms and What They Prioritize

| Platform | Mechanism | Key Signal |
|----------|-----------|------------|
| Google AI Overviews | RAG from index | E-E-A-T, schema, freshness |
| ChatGPT Browse | RAG from live web | Extractability, authority |
| Perplexity | RAG from live web | Sources, recency, structure |
| Gemini | RAG + training | YouTube, Google ecosystem |
| Claude (claude.ai) | Training data only | Training corpus (Common Crawl, books) |
| Bing Copilot | RAG from Bing index | Traditional SEO + schema |

### Most Cited Platforms by LLMs

1. LinkedIn (rising fast — real human authors)
2. Reddit (huge training data source, frequently cited in RAG)
3. Wikipedia (entity validation, fact-checking)
4. YouTube (especially Gemini)
5. Quora (Q&A format ideal)
6. Reuters, AP News (for factual claims)
7. Government sites (.gov, .edu)

### Monitoring Tools

| Tool | Best For | Cost |
|------|----------|------|
| Manual AI testing | Quick spot checks | Free |
| Otterly.ai | Automated brand monitoring | Paid |
| Semrush AI Visibility Toolkit | Enterprise-grade tracking | Paid |
| Profound | Deep citation analysis | Paid |
| Rankability | Built-in AI Analyzer | Paid |
| Google Search Console | AI Overview tracking | Free |
| Server logs | GPTBot/ClaudeBot crawl activity | Free |

---

*Document compiled by Murph | AI Chief of Staff to CJ Emerson*
*Based on research from: Backlinko, GoFishDigital, Amsive, Onely, GeoStar, SEMrush, Ahrefs, BBC Future, Search Engine Land, and primary research from multiple GEO practitioners*
*February 2026 — Review quarterly as this field evolves rapidly*
