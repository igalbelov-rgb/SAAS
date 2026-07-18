# 🚀 Automated Omni-Channel SaaS Platform

An enterprise-grade, AI-powered SaaS platform designed to automate e-commerce data extraction, creative content generation, and multi-channel marketing distribution. Built with a robust FastAPI backend, an interactive React/Vite frontend, and orchestrated via Docker & Nginx.

The entire production ecosystem is fully deployed and hosted on a cloud-based **AWS EC2 (Elastic Compute Cloud)** instance.

---

## 🏗️ System Architecture & Stack

┌─────────────────────────┐
│   Nginx Reverse Proxy   │ (Port 80/443)
└────────────┬────────────┘
             │
        ┌────┴────────────────────────┐
        ▼                             ▼
┌───────────────────────┐     ┌───────────────────────┐
│ React / Vite Frontend │     │    FastAPI Backend    │ (Port 8000)
└───────────────────────┘     └───────────┬───────────┘
                                          │
        ┌─────────────────────────────────┴───────────┐
        ▼                                             ▼
┌───────────────────────┐                     ┌───────────────────────┐
│     PostgreSQL DB     │                     │     n8n Automation    │
└───────────────────────┘                     └───────────────────────┘

### 🛰️ Infrastructure & Cloud DevOps
* **AWS EC2 Hosting:** The production infrastructure is entirely provisioned on an **AWS EC2** instance, handling real-time application traffic, automated workloads, and background tasks.
* **Nginx:** Acts as the reverse proxy on the EC2 host, handling SSL termination, CORS mitigation, and routing requests securely to the backend or frontend containers.
* **Docker & Docker Compose:** Containerizes all decoupled services to ensure configuration parity between local development (`localhost`) and the remote AWS production environment.
* **GitHub Actions (CI/CD):** Automatically triggers on code pushes to the main branch to run linters, execute unit tests, compile optimized multi-stage Docker builds, and deploy updates seamlessly to the **AWS EC2** instance.

### 🐍 Backend Service & Dependencies (Python 3.11)
The core architecture relies on an asynchronous, highly concurrent Python ecosystem with strict third-party pinning to guarantee runtime stability:

#### 1. Core Framework & Web Server
* `fastapi==0.111.0` - Modern, fast (high-performance) web framework for building APIs.
* `uvicorn==0.30.1` - Asynchronous ASGI server implementation used to run the FastAPI application.
* `python-multipart==0.0.9` - Enables native support for parsing form-data, file uploads, and multi-part payloads.

#### 2. Configuration & Data Validation
* `pydantic==2.7.2` - Data validation and settings management using Python type hinting.
* `pydantic-settings==2.3.3` - Advanced configuration management using `.env.production` files. 
* `python-dotenv==1.0.1` - Reads key-value pairs from `.env` files and sets them as environment variables.
* `email-validator>=2.0.0` - Robust syntactic validation for user registration and communication setups.

> 💡 *Note on Encoding:* Configuration is managed with an explicit `env_file_encoding = "utf-8"` within Pydantic-Settings to guarantee cross-platform support and native Hebrew/Unicode character parsing.

#### 3. Scraping, Networking & AI Engines
* `beautifulsoup4==4.12.3` - Screen-scraping library used to parse HTML structures and extract e-commerce data.
* `openai>=1.12.0` - Official SDK for orchestrating generative AI workflows (including OpenAI and `groq` platforms using `llama-3.1-8b-instant`).
* `httpx==0.26.0` - Next-generation, non-blocking HTTP client providing asynchronous pooling.
* `h2==4.1.0` - Pure-Python HTTP/2 state-machine to support rapid concurrent web transport pipelines.
* `requests==2.31.0` - Standard synchronous HTTP library utilized for resilient fallback connection blocks.

#### 4. Relational Database Stack
* `sqlmodel==0.0.22` - Object-Relational Mapping (ORM) framework designed by the creator of FastAPI, natively unifying `Pydantic` validation models and `SQLAlchemy` database operations.
* `psycopg2-binary==2.9.9` - Production-ready PostgreSQL database adapter for Python applications.

#### 5. Security & Authentication Stack
* `bcrypt==4.2.0` - High-security password hashing algorithm utilized to safely obfuscate user credentials.
* `pyjwt[crypto]==2.10.1` - JSON Web Token implementation with cryptographic binding to maintain secure, persistent user sessions.

### 💻 Frontend Service (React 19 & Vite 8)
* **Tech Stack:** Migrated to `React 19` and `Vite 8` for lightning-fast Hot Module Replacement (HMR) and optimal state management.
* **Styling Engine:** `Tailwind CSS v4` integrated natively via the `@tailwindcss/vite` pipeline, removing legacy configuration clutter (`tailwind.config.js`, `postcss.config.js`).
* **UI Layout:** Custom **"Ocean & Sand" theme** featuring a modern full-width split-screen workspace (Input deck on the left, live channel pipeline previews on the right) utilizing `Lucide-React` icon matrices.
* **Data Layer:** `Axios` HTTP client fitted with global request interceptors to dynamically dispatch bearer authentication headers.

---

## 🔄 End-to-End Core Pipeline (Data Flow)

When a user interacts with the system, data propagates through the decoupled architecture via a strict, high-performance lifecycle:

### Phase 1: Ingestion & Scraping (`POST /api/products/scrape`)
1. **Client Request:** The user drops an Amazon/E-commerce URL into the Frontend control deck. `Axios` dispatches a secure request through the `Nginx` reverse proxy to the `FastAPI` Extraction Engine running on **AWS EC2**.
2. **Extraction:** The backend utilizes `BeautifulSoup4` and custom headers to bypass anti-bot mechanisms, harvesting raw product titles, specification lists, prices, and media asset URLs.
3. **Database Persistence:** The parsed data is structured inside a `SQLModel` schema and safely committed to the `PostgreSQL` database, returning a unique product record ID (`pk_id`).

### Phase 2: AI Copywriting & Optimization
1. **Contextual Payload Preparation:** The backend retrieves the scraped data from PostgreSQL and constructs optimized prompts tailored to consumer-centric marketing frameworks.
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
Extracts unstructured web data using `BeautifulSoup4` and normalizes e-commerce vendor parameters into clean relational entities managed via `SQLModel`.

### 2. Image Transformer (Visual Refinement)
Normalizes raw seller images into professional, brand-aligned ad creatives, modifying pixel matrices or calling visual models to deliver production-ready assets.

### 3. AI Copywriting Engine
Translates analytical, flat technical specs into engaging, high-conversion copy optimized for channel-specific engagement benchmarks using `OpenAI` & `Groq` endpoints.

### 4. Omni-Channel Publisher
Publishes creative assets and localized affiliate links across multiple external social networks simultaneously using unified webhooks and API orchestration blocks.