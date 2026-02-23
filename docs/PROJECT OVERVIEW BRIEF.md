# PROJECT OVERVIEW BRIEF — Copywriter AI Platform

Last edited time: February 23, 2026 9:38 PM

## 1) Product concept

**Copywriter AI** — ijtimoiy tarmoqlarda kontent joylashtiradigan barcha foydalanuvchilar uchun (marketolog, SMM, biznes egasi, bloger va h.k.) tezkor va sifatli matn tayyorlaydigan AI platforma.

Foydalanuvchi:

- nima yozmoqchi ekanini aytadi (Telegram post, banner copy, landing/offer copy),
- sozlamalarni tanlaydi (tone, emoji, platforma, CTA, brend ovozi, taqiqlar, hashtag, persona),
- natijani **A/B variant** ko‘rinishida oladi,
- “baholovchi model”dan **tavsiyalar** oladi,
- tavsiyalar **one-click** tugmalar ko‘rinishida qo‘llanadi (iteratsiya tezlashadi).

## 2) Value proposition (siz so‘ragan “va’da” — taklif qilinadigan variant)

**“3 tilda (UZ/RU/EN) brend uslubingizga mos, platformaga moslashgan A/B copy — 1 daqiqada.”**

Qo‘shimcha tagline variantlari:

- “Sizning brendingiz ohangida. Sizning auditoriyangiz tilida.”
- “Yozish emas — tanlash va klik qilish.”

## 3) Target audience

**Primary (MVP):** ijtimoiy tarmoqlarda kontent joylashtiradigan barcha foydalanuvchilar

**Use-cases (Top-3):**

1. Telegram post
2. Reklama banner matnlari
3. Landing/offer copy

## 4) MVP platform strategy

- **Phase 1:** Telegram Bot (MVP, birinchi bozor validatsiyasi)
- **Phase 2:** Web-App (Telegramdagi account bilan login + full dashboard)
- **Phase 3:** Web-Sayt (landing + pricing + auth + app entry)
- **Phase 4:** Chrome Extension
- **Phase 5:** Mobile App

> Asosiy prinsip: **backend universal**, clientlar (Telegram/Web/Extension/Mobile) to‘liq ajratilgan.
> 

---

# 5) User experience (Telegram MVP flow)

### Core flow

`/start → input → settings → generate → A/B variants → review → improve buttons → (save/copy/export)`

### Input (minimal)

- Matn maqsadi (post / banner / landing)
- Kontekst: mahsulot/xizmat, foyda (USP), auditoriya, CTA
- Cheklovlar: “forbidden words”, tone, emoji, length, hashtag, platform

### Settings (customizable + defaults)

- Tone
- Emoji usage
- Style (short/long, formal/casual, storytelling, etc.)
- Length
- CTA type + CTA text
- Target platform (Telegram/IG/TikTok/Ads/Landing…)
- Brand voice (Brand profile selection)
- Forbidden words
- Hashtags
- Audience persona (Audience profile selection)

### A/B variants

- **Variant A** va **Variant B** bir-biridan farqli strategiya bilan:
    - A: “benefit-driven” / “direct response”
    - B: “story/relatable” / “curiosity hook”
- Har bir variant uchun: Copy + optional “hooks/CTA” bloklari.

### Critic (baholovchi model)

- **Tavsiyalar** beradi (o‘zi rewrite qilmaydi).
- Output: “Issue list + suggestion list”
- Suggestion list tugmalarga aylanadi (one-click actions).

---

# 6) Core features (Scope)

## Must-have (MVP)

1. Telegram bot UX (inline buttons, wizard flow)
2. 3 til: **UZ/RU/EN** (bir xil sifat darajasiga yaqin)
3. A/B generation
4. Critic: tavsiyalar + one-click improve actions
5. User auth: Telegram auto-auth + universal auth (email/OAuth keyin)
6. Brand Profile + Audience Profile (bir nechta saqlash, tanlash)
7. History: 30 kun
8. Rate limit + queue (Redis + Celery/RQ)
9. Billing base: trial + subscription + free daily limit (2/day)

## Should-have (MVP+)

- Export formatlar: “Telegram post”, “Ad banner short/medium”, “Landing sections”
- Analytics: best-performing settings (A/B feedbackdan)
- Admin panel: template/settings, plans, limits, abuse monitoring

## Could-have (coming soon)

- Template marketplace (siz aytgandek: 1-versiyada yo‘q, “coming soon”)
- Team/agency workspace (sizda bor: multi-tenant)
- Chrome extension rewriting
- Mobile app

---

# 7) Monetization & plans

## Free trial + subscription

- **Free limit:** kuniga 2 generation
- **Trial:** (taklif) 3–7 kun Pro access yoki 20 credit (aniqlash mumkin)

## Payments priority

- Telegram users: **Telegram Stars** (primary)
- Others: **Stripe**
- Local: **Payme**
- Optional: **Crypto**

> Billing arxitekturasi provider-agnostic bo‘lishi kerak (Stripe/Payme/Stars/Crypto alohida adapterlar).
> 

---

# 8) Safety & policy layer (Sensitive content)

### 1) Default mode (hamma uchun)

- Moderation **ON**
- Quyidagilar bloklanadi:
    - noqonuniy faoliyat / firibgarlik
    - nafrat, zo‘ravonlikka undash
    - o‘ziga zarar (self-harm)
    - tahdid/harassment
    - ekstremizm
- “Adult / sensual / provocative marketing” — **cheklangan** (yumshoq formatda, explicit bo‘lmagan).

### 2) Relaxed mode (faqat aktiv subscription)

- Moderation **Relaxed**
- Ruxsat kengayadi:
    - “adult marketing language” (18+ kontekst) — **allowed**
    - “sensual/romantic/provocative” copy — **allowed**
    - “edgy humor / stronger slang” — **allowed**
- Baribir **doim blok**:
    - noqonuniy instruktsiyalar (drug making, hacking, weapons, scam)
    - hate/violent extremism
    - self-harm kontent
    - doxxing/PII abuse

### 3) Implementatsiya (backend)

- `entitlements.relaxed_safety = true/false`
- Har requestda:
    - `policy_mode = default | relaxed`
    - Moderation service policy setini shunga qarab tanlaydi
- Loglarda `policy_mode` alohida saqlanadi (audit uchun), prompt esa **masked**.

---

# 9) Data & learning policy

- User promptlari **training** uchun ishlatilmaydi.
- Lekin:
    - A/B test natijalari
    - user rating/feedback
    - “high-rated settings + output meta”
        
        kabi **anonim agregat** ma’lumotlar model/prompt strategiyani optimizatsiya qilish uchun ishlatiladi.
        

Logging:

- prompts **masked** (PII va sensitive qismlar mask)
- request_id tracing (debug uchun)

---

# 10) Technical architecture (API-first, microservices)

## High-level components

**Clients**

- Telegram Bot
- Web-App
- Web-Site
- Chrome Extension
- Mobile App

**Backend (universal)**

1. **API Gateway / BFF** (FastAPI)
2. **Auth Service** (Telegram auto + email/OAuth future)
3. **User Profile Service**
    - Brand Profiles
    - Audience Profiles
4. **Generation Orchestrator Service**
    - Writer → Critic → Suggestion mapping → Improvement execution
5. **LLM Provider Service**
    - OpenRouter integration (provider-agnostic layer)
    - model routing, fallbacks, cost tracking
6. **Billing Service**
    - Plans, subscription, entitlements
    - Payment adapters: Stars, Stripe, Payme, Crypto
7. **Moderation/Safety Service**
    - policy checks, sensitive gating
8. **History & Storage Service**
    - generations, reviews, suggestions, versions
9. **Analytics Service** (MVP minimal)
    - A/B stats, best settings, conversion metrics

**Infra**

- Postgres (core)
- Redis (cache + queue)
- Celery/RQ (async jobs)
- Object Storage (optional: exports/assets)
- Observability: logs + metrics + error tracking

## Microservice boundaries (pragmatic MVP)

MVPda servislarni “logical modules” qilib boshlab, infra jihatdan 2–3 deployment bilan ham chiqsa bo‘ladi:

- `api-gateway` (auth + profiles + history endpoints)
- `ai-orchestrator` (writer/critic/provider routing)
- `billing` (entitlements + payments)

Keyin scale bo‘lsa alohida microservice’larga ajratiladi.

---

# 11) LLM pipeline design

## Writer model

Input:

- user input (context)
- settings
- chosen brand profile
- chosen audience profile
- language + platform constraints

Output:

- Variant A
- Variant B
- meta: style tags, token usage, language, version

## Critic model

Input:

- variant A/B
- expected constraints (tone, length, forbidden, CTA, platform)

Output:

- issues (list)
- suggestions (list)
    - each suggestion has: `type`, `label`, `action_payload`

## One-click improve execution

When user taps a button:

- Orchestrator calls Writer again with:
    - original content + explicit “apply suggestion X” instruction
    - keeps constraints fixed
- Stores new version linked to original generation.

---

# 12) Key API endpoints (draft contract)

## Auth

- `POST /auth/telegram` (telegram_id + signature verification)
- `POST /auth/login` (future: email/OAuth)

## Profiles

- `POST /profiles/brand`
- `GET /profiles/brand`
- `POST /profiles/audience`
- `GET /profiles/audience`

## Generation

- `POST /generate`
    
    body: `{language, use_case, input, settings, brand_profile_id?, audience_profile_id?, ab=true}`
    
- `POST /review`
    
    body: `{generation_id}` or `{textA,textB,constraints}`
    
- `POST /improve`
    
    body: `{generation_id, suggestion_id, target_variant: A|B}`
    

## History

- `GET /history?range=30d`
- `GET /generation/{id}` (versions + suggestions + rating)

## Billing

- `GET /plans`
- `POST /subscribe`
- `POST /payment/webhook/*` (stripe/payme/crypto)
- `POST /stars/confirm` (telegram stars)

## Admin (MVP minimal)

- `GET /admin/usage`
- `POST /admin/settings/defaults`

---

# 13) Data model (high-level)

- **User**: id, telegram_id, email?, locale, created_at
- **Entitlement**: user_id, plan_id, active_until, daily_limit, relaxed_safety_flag
- **BrandProfile**: user_id, name, tone, vocab, forbidden, examples
- **AudienceProfile**: user_id, name, persona, pains, desires, style prefs
- **Generation**: user_id, use_case, language, settings_snapshot, input_snapshot, created_at
- **Variant**: generation_id, key(A/B), text, meta
- **Review**: generation_id, score(optional), issues[], created_at
- **Suggestion**: review_id, type, label, payload
- **GenerationVersion**: parent_generation_id, applied_suggestion_id, result_text, created_at

Retention:

- History 30 kun (keyin auto purge)

---

# 14) Multi-tenant (team/agency)

Sizning talab: “Ha bo‘ladi”.

Shuning uchun data modelga:

- **Workspace** (team)
- **Member roles** (owner/admin/editor/viewer)
- **Shared Brand Profiles** (workspace-level)
- Billing workspace-level yoki user-level (2 modeldan birini tanlaymiz)

MVPda minimal: workspace skeleton + future flags.

---

# 15) Performance & scalability

- Redis rate limit (per user, per minute/day)
- Celery/RQ queue:
    - generate jobs
    - review jobs
    - improve jobs
- Timeout handling + retries
- Provider routing:
    - model fallback (OpenRouter models list)
    - cost guardrail (max tokens / max cost per request)

---

# 16) Success metrics (MVP)

- Activation: /start → 1st generation completion %
- A/B usage: A vs B copy/click ratio
- Improve click rate: suggestions applied %
- Repeat usage: 7-day retention
- Conversion: free → trial → paid
- Cost: average cost per successful generation

---

# 17) Risks & mitigation

1. **3 til sifatida farq** → har til uchun prompt tuning + eval set
2. **Cost spike** → daily limit + token cap + queue + caching
3. **Safety policy clash** → “relaxed mode” (to‘liq off emas) + audit logs
4. **Telegram UX friction** → minimal steps + presets + last-used settings
5. **Provider instability** → OpenRouter fallback routing + circuit breaker

---

# 18) Open questions (key decisions to finalize)

Quyidagilarni men siz tasdiqlamasangiz ham “default” qilib ketaverdim, lekin final PRDga yaqinlashish uchun kerak bo‘ladi:

1. Trial: 3 kunmi, 7 kunmi? (yoki credit)
2. A/B variantlar farqi: “strategy presets”ni aniq belgilaymizmi?
3. Rating: user 1–5 baho beradimi? (A/B training signal uchun foydali)
4. Workspace billing: user-levelmi yoki team-level?