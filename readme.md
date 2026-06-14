🚀 Automated Omni-Channel SaaS Platform
An enterprise-grade, AI-powered SaaS platform designed to automate e-commerce data extraction, creative content generation, and multi-channel marketing distribution. Built with a robust FastAPI backend, an interactive React/Vite frontend, and orchestrated via Docker & Nginx.

🏗️ System Architecture & Stack
                       ┌─────────────────────────┐
                       │   Nginx Reverse Proxy   │ (Port 80/443)
                       └────────────┬────────────┘
                                    │
            ┌───────────────────────┴───────────────────────┐
            ▼                                               ▼
┌───────────────────────┐                       ┌───────────────────────┐
│ React / Vite Frontend │                       │    FastAPI Backend    │ (Port 8000)
└───────────────────────┘                       └───────────┬───────────┘
                                                            │
                                    ┌───────────────────────┴───────────────────────┐
                                    ▼                                               ▼
                        ┌───────────────────────┐                       ┌───────────────────────┐
                        │     PostgreSQL DB     │                       │     n8n Automation    │
                        └───────────────────────┘                       └───────────────────────┘
🛰️ Infrastructure & DevOps
Nginx: Acts as the reverse proxy, handling SSL termination, CORS mitigation, and routing requests securely to the backend or frontend containers.

Docker & Docker Compose: Containerizes all decoupled services to ensure configuration parity between development environments and remote servers.

GitHub Actions (CI/CD): Automatically triggers on code pushes to the main branch to run linters, execute unit tests, compile optimized multi-stage Docker builds, and deploy updates to an AWS EC2 instance.

🐍 Backend Service (Python 3.11)
Core Framework: FastAPI + Uvicorn for asynchronous, highly concurrent API execution.

Database & ORM: PostgreSQL managed via SQLModel (unifying Pydantic data schemas and SQLAlchemy relational structures).

Security & Auth: Secure token-based user persistence utilizing PyJWT and Passlib (Bcrypt hashing algorithm).

💻 Frontend Service (JS/TS)
Framework: React + Vite utilizing single-page application (SPA) routing (react-router-dom).

Styling & UI: Tailwind CSS integrated with Lucide-React icon packs.

Data Layer: Axios HTTP clients fitted with request interceptors to automatically dispatch bearer authentication tags.

🎯 System Modules & Core Features
1. Scraper & Link Converter (Extraction Engine)
Functionality: Extracts unstructured web data when a user inputs a target vendor product URL.

Implementation: BeautifulSoup4 and custom Requests protocols pull live product titles, raw specifications, and media asset endpoints into localized structured tables.

2. Image Transformer (Visual Refinement)
Functionality: Normalizes raw seller images into professional, brand-aligned ad creatives.

Implementation: Specialized internal microservices modify pixel matrices or call downstream visual models to deliver production-ready marketing assets.

3. AI Copywriting Engine (Contextual Content Generation)
Functionality: Translates analytical, flat technical specs into engaging, consumer-centric ad copy.

Implementation: Integrates with OpenAI APIs using tailored prompt topologies optimized for channel-specific engagement benchmarks:

Telegram: Compact, punchy copy with prominent pricing indicators and immediate Call-to-Actions (CTAs).

Facebook: Hook-driven narrative copy focusing on target problem resolution and key benefits.

4. Omni-Channel Publisher (Distribution Orchestration)
Functionality: Publishes creative assets and affiliate links across a broad network with a single interaction.

Implementation: Utilizes an integrated asynchronous pipeline combined with n8n orchestration to trigger webhook relays:

Telegram Bot API: Dispatches updates instantly to moderated target channels and groups.

Meta Graph API: Programs automated posts straight to Facebook Pages or communities.

Pinterest API: Generates searchable visual boards that drive consistent affiliate referral funnels.

🗺️ Project Execution Roadmap
[x] Initial Repository Architecture Setup

[x] Containerized Multi-Service Docking Matrix (Local dev environments configured)

[x] Basic Route Matrix Configuration (react-router-dom and Nginx reverse mapping)

[ ] Database Schema Migration & Model Definition (SQLModel + PostgreSQL)

[ ] Authentication Stack Verification (Registration, Login, and Protected Route guards)

[ ] Scraper Pipeline & LLM API Integration

[ ] n8n Workflow Automation Engine Connection

[ ] GitHub Actions CI/CD deployment script testing on target cloud environments

saas/                  # תיקיית שורש (Root)
├── .github/
│   └── workflows/
│       └── deploy.yml              # 🚀 CI/CD Pipeline (GitHub Actions)
│
├── nginx/                          # 🌐 ה-Web Server והשומר בכניסה
│   ├── Dockerfile
│   └── nginx.conf                  # מנתב פניות ל-Frontend, ל-Backend ול-n8n
│
├── frontend/                       # 💻 ממשק המשתמש (למשל React / Vite
│   ├── node_modules
│      └── *
│   ├── public/
|      └── favico.svg
|      └── icons.svg
│   ├── src/
│   ├── package.json
│   ├── .env.production             # 🔑 משתני סביבה של 
│   ├── .env.development
|   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── readme.md
│   ├── vite.config.js
הפרודקשן עבור ה-Client
│   └── Dockerfile
│
├── backend/                 # 🐍 ה-Backend המרכזי (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # נקודת כניסה (FastAPI App)
│   │   ├── config.py               # קורא את ה-.env ומפיץ לקוד
│   │   ├── crypto.py               # 
│   │   ├── database.py             # חיבור ל-ORM (SQLAlchemy/SQLModel)
│   │   ├── models.py               # טבלאות הדאטאבייס (Users, Products, Subs)
│   │   ├── schemas.py              # אימות קלט/פלט (Pydantic)
│   │   │
│   │   ├── api/                    # 📂 חלוקת ה-API לנתיבים (Routers)
│   │   │   ├── auth.py             # רישום, התחברות (JWT) וניהול משתמשים
│   │   │   ├── products.py         # האוטומציה של הזרקת הלינקים וה-AI
│   │   │   └── billing.py          # סנכרון תשלומים (Stripe Webhooks)
│   │   │
│   │   ├── scrapers/               # מודול שליפת נתונים מהאינטרנט
│   │   └── ai_services/            # מודול חיבור ל-OpenAI / Stability
│   │
│   ├── .env.production             # 🔑 קובץ הסודות של ה-Backend בפרודקשן (לא עולה לגיט!)
│   ├── requirements.txt
│   └── Dockerfile
│
├── n8n-automation/                 # 🔄 מנוע האוטומציה וההפצה (מנוהל בדוקר)
│   └── workflows/
│       └── publish_pipeline.json
│
└── docker-compose.yml              # 🐳 מנצח התזמורת של הפרודקשן (מקים את כל השירותים)

### 🎨 UI/UX Overhaul & Modernization (Frontend)
- **Tech Stack Upgrade:** Migrated the frontend architecture to utilize **Vite 8**, **Tailwind CSS v4**, and **React 19** for maximum compilation speed and state efficiency.
- **Design Overhaul:** Replaced the default dark skeleton view with a punchy, highly dynamic **"Ocean & Sand" theme** tailored for modern SaaS products.
- **Structural Layout:** Implemented a full-width split-screen workspace featuring a seamless input control deck on the left and a live social media pipeline preview deck on the right.
- **Dependency Clean-up:** Resolved core PostCSS and Autoprefixer conflicts by aligning the system to use the native `@tailwindcss/vite` pipeline, wiping out redundant configuration clutter (`postcss.config.js`, `tailwind.config.js`).