# 🚀 Automated Omni-Channel SaaS Platform

An enterprise-grade, AI-powered SaaS platform designed to automate e-commerce data extraction, creative content generation, and multi-channel marketing distribution. Built with a robust FastAPI backend, an interactive React/Vite frontend, and orchestrated via Docker & Nginx.

---

## 🏗️ System Architecture & Stack

┌─────────────────────────┐
                    │   Nginx Reverse Proxy   │ (Port 80/443)
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        ▼                                                 ▼
┌───────────────────────┐                         ┌───────────────────────┐
│ React / Vite Frontend │                         │    FastAPI Backend    │ (Port 8000)
└───────────────────────┘                         └───────────┬───────────┘
│
┌─────────────────────────┴────────────────────────┐
▼                                                  ▼
┌───────────────────────┐                          ┌───────────────────────┐
│     PostgreSQL DB     │                          │    n8n Automation     │
└───────────────────────┘                          └───────────────────────┘

### 🛰️ Infrastructure & DevOps
* **Nginx:** Acts as the reverse proxy, handling SSL termination, CORS mitigation, and routing requests securely to the backend or frontend containers.
* **Docker & Docker Compose:** Containerizes all decoupled services to ensure configuration parity between local development (`localhost`) and remote target environments.
* **GitHub Actions (CI/CD):** Automatically triggers on code pushes to the main branch to run linters, execute unit tests, compile optimized multi-stage Docker builds, and deploy updates to an AWS EC2 instance.

### 🐍 Backend Service (Python 3.11)
* **Core Framework:** `FastAPI` + `Uvicorn` for asynchronous, highly concurrent API execution.
* **Database & ORM:** `PostgreSQL` managed via `SQLModel` (unifying `Pydantic` data validation and `SQLAlchemy` relational structures).
* **Configuration Management:** `Pydantic-Settings` using `.env.production` with explicit `env_file_encoding = "utf-8"` to guarantee seamless cross-platform support and native Hebrew/Unicode character parsing.
* **Security & Auth:** Secure token-based user persistence utilizing `PyJWT` and `Passlib` (Bcrypt hashing algorithm).
* **External Integration Ecosystem:** * `openai` & `groq` (Utilizing `llama-3.1-8b-instant`) for ultra-fast, contextual copywriting generation.
    * `httpx` (Pinned to `v0.26.0`) to provide non-blocking HTTP pooling and resolve upstream dependency conflicts.

### 💻 Frontend Service (React 19 & Vite 8)
* **Tech Stack:** Migrated to `React 19` and `Vite 8` for lightning-fast Hot Module Replacement (HMR) and optimal state management.
* **Styling Engine:** `Tailwind CSS v4` integrated natively via the `@tailwindcss/vite` pipeline, removing legacy configuration clutter (`tailwind.config.js`, `postcss.config.js`).
* **UI Layout:** Custom **"Ocean & Sand" theme** featuring a modern full-width split-screen workspace (Input deck on the left, live channel pipeline previews on the right) utilizing `Lucide-React` icon matrices.
* **Data Layer:** `Axios` HTTP client fitted with global request interceptors to dynamically dispatch bearer authentication headers.

---

## 🔄 End-to-End Core Pipeline (Data Flow)

When a user interacts with the system, the data propagates through the decoupled architecture via a strict, high-performance lifecycle:

### Phase 1: Ingestion & Scraping (`POST /api/products/scrape`)
1. **Client Request:** The user drops an Amazon/E-commerce URL into the Frontend control deck. `Axios` dispatches a secure request through the `Nginx` reverse proxy to the `FastAPI` Extraction Engine.
2. **Extraction:** The backend utilizes `BeautifulSoup4` and custom headers to bypass anti-bot mechanisms, harvesting raw product titles, specification lists, prices, and media asset URLs.
3. **Database Persistence:** The parsed data is structured inside a `SQLModel` schema and safely committed to the `PostgreSQL` database, returning a unique product record ID (`pk_id`).

### Phase 2: AI Copywriting & Optimization
1. **Contextual Payload Preparation:** The backend retrieves the scraped data and constructs optimized prompts tailored to consumer-centric marketing frameworks.
2. **LLM Execution:** An asynchronous call is dispatched to the `Groq/OpenAI` API using the `llama-3.1-8b-instant` model.
    * *Resilience Layer:* If an upstream API timeout or authentication error occurs, the pipeline catches the exception and dynamically generates a structurally sound fallback mock to guarantee an uninterrupted user experience.
3. **Multi-Channel Customization:** The engine outputs three customized variations:
    * **Telegram:** Punchy, short copy with prominent pricing indicators, emojis, and immediate call-to-actions.
    * **Facebook:** Hook-driven narrative copy focusing on target problem resolution and key product benefits.
    * **Pinterest:** Optimized SEO description tags accompanied by dynamic setup ideas.

### Phase 3: Omni-Channel Publishing (`POST /api/products/publish/telegram`)
1. **Validation & State Update:** The user reviews the content on the React pipeline view and clicks "Publish". The database updates the product record state to `is_published = True`.
2. **Webhook Relay:** FastAPI triggers a webhook orchestration relay to `n8n Automation`.
3. **Target Distribution:**
    * **Telegram Bot API:** Dispatches the marketing asset bundle (Image + Generated Copy + Affiliate Link) instantly to moderated target channels.
    * **Meta Graph & Pinterest APIs:** Programmatically deliver tailored posts straight to target business pages and searchable visual boards.

---

## 🎯 System Modules & Core Features

### 1. Scraper & Link Converter (Extraction Engine)
Extracts unstructured web data and normalizes e-commerce vendor parameters into clean relational entities.

### 2. Image Transformer (Visual Refinement)
Normalizes raw seller images into professional, brand-aligned ad creatives, modifying pixel matrices or calling visual models to deliver production-ready assets.

### 3. AI Copywriting Engine
Translates analytical, flat technical specs into engaging, high-conversion copy optimized for channel-specific engagement benchmarks.

### 4. Omni-Channel Publisher
Publishes creative assets and localized affiliate links across multiple external social networks simultaneously with a single interaction.

---

## 🗺️ Project Execution Roadmap

- [x] Initial Repository Architecture Setup
- [x] Containerized Multi-Service Docking Matrix (Local dev environments configured)
- [x] Basic Route Matrix Configuration (`react-router-dom` and Nginx reverse mapping)
- [x] Frontend UI Overhaul (Vite 8 + Tailwind v4 + Ocean & Sand Layout)
- [x] Database Schema Definition & Model Persistence (`SQLModel` + `PostgreSQL`)
- [ ] Authentication Stack Verification (Registration, Login, and Protected Route guards)
- [ ] Live LLM Live Connection Tuning (Groq Client integration & Exception handler stabilization)
- [ ] n8n Workflow Automation Engine Connection
- [ ] GitHub Actions CI/CD deployment script testing on target cloud environments