# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MrCopywriteBot is an AI-powered copywriting platform (Phase 1: Telegram Bot MVP). It generates social media copy in 3 languages (UZ/RU/EN) with A/B variants, critic evaluation, and one-click improvement actions. The full PRD is in `docs/PROJECT OVERVIEW BRIEF.md`.

## Current Status

Pre-implementation / planning phase. No source code yet — only a project overview document and LICENSE (Apache 2.0).

## Planned Tech Stack

- **Python 3.11+** with **FastAPI**
- **PostgreSQL** (core data), **Redis** (cache + queue), **Celery/RQ** (async jobs)
- **OpenRouter** for LLM access (provider-agnostic routing with fallbacks)
- **Telegram Bot API** for Phase 1 client (aiogram or python-telegram-bot TBD)
- Payment adapters: Telegram Stars, Stripe, Payme, Crypto

## Architecture

Three logical modules (start monolithic, split into microservices later):

1. **api-gateway** — FastAPI app: auth, user/brand/audience profiles, history
2. **ai-orchestrator** — Writer model → Critic model → Suggestion mapping → Improve execution
3. **billing** — Entitlements, subscription plans, payment provider adapters

Backend is API-first; all clients (Telegram Bot, future Web/Mobile/Extension) are fully decoupled.

## Core LLM Pipeline

```
User input + settings + brand profile + audience profile
  → Writer model → Variant A + Variant B
  → Critic model → Issues[] + Suggestions[]
  → Suggestions become inline Telegram buttons
  → User taps button → Improve call → new GenerationVersion stored
```

## Key Domain Models

- **Generation** → produces 2 **Variants** (A: benefit-driven, B: story/curiosity hook)
- **Review** → critic evaluation producing **Suggestions** (typed actions with label + payload)
- **GenerationVersion** → result of applying a suggestion to a variant
- **BrandProfile** / **AudienceProfile** — saved user presets for tone, persona, constraints
- **Entitlement** — plan, daily limits, `relaxed_safety` flag

## Safety Modes

- `default`: moderation ON, adult/provocative content restricted
- `relaxed`: paid subscribers only (`entitlements.relaxed_safety = true`), allows adult marketing language
- Always blocked regardless of mode: illegal content, hate speech, violence, self-harm, extremism

## Languages

UZ (Uzbek, primary market), RU (Russian), EN (English) — equal quality target across all three.
