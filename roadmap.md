# 📝 Project Status & Future Roadmap

## 📌 1. What We Have Done So Far (Completed)
* **Project Architecture:** Structured a decoupled Full-Stack architecture (`frontend/`, `backend/`, `nginx/`, `n8n-automation/`).
* **Containerization:** Configured a unified environment using Docker & Docker Compose with persistent data volumes for PostgreSQL.
* **Reverse Proxy:** Implemented Nginx to orchestrate clean internal routing and eliminate CORS issues between services.
* **Modern Authentication Stack:** Rewrote the auth mechanics to use pure, modern `bcrypt` directly, eliminating legacy library issues.
* **Token-Based Security:** Created an asynchronous JWT generation mechanism in FastAPI and synchronized the React client to capture tokens and securely auto-navigate to the `/dashboard`.

---

## 🛠️ 2. Upcoming Milestones & Required Files (To-Do)

### 📺 Milestone A: Building the Advanced AI Dashboard
To transform the current dashboard into a high-converting, beautiful, and interactive application containing product URL inputs, AI review sections, and social media toggle controls, we will modify/create the following files:

* **`frontend/src/pages/Dashboard.jsx` (Modify/Build):**
  * Create a clean grid-based split layout (Input Form vs. Live Preview Panel).
  * Add a URL input field with loading states for the scraper.
  * Add tabs/sections to show the generated AI Copywriting (Telegram vs. Facebook tabs).
* **`frontend/src/components/ProductPreview.jsx` (New Component):**
  * Displays the extracted product title, technical specs, and a gallery of images fetched by the backend.
* **`frontend/src/components/PublishControl.jsx` (New Component):**
  * Contains the action buttons with icons (`Lucide-React`) for one-click publishing to Telegram, Facebook, and Pinterest. A button for each, 3 in total.
* **`frontend/src/services/api.js` (Modify):**
  * Add Axios functions to dispatch the product URL to the backend (`api.post('/products/scrape')`) and to trigger the publishing pipeline.

### 🧠 Milestone B: AI Integration & Sourcing Automation (OpenAI & Scraping)
To enable the system to automatically analyze URLs, extract technical data, and generate tailored marketing copy, we will build the core functional services on the backend:

* **`backend/app/scrapers/product_scraper.py` (New Module):**
  * Uses `BeautifulSoup4` and custom headers to parse target URLs, pull titles, descriptions, and extract image links.
* **`backend/app/ai_services/openai_client.py` (New Module):**
  * Initializes the `OpenAI` client using configuration environment variables.
  * Contains the custom system and user prompt engineering functions to translate raw tech specs into structured channel-specific copy.
* **`backend/app/api/products.py` (New Router):**
  * Exposes endpoints like `@router.post("/scrape")` and `@router.post("/generate-copy")` to orchestrate the internal scraper and OpenAI service.
* **`backend/app/models.py` & `schemas.py` (Modify):**
  * Add the `Product` model to the database to log past scraped products, descriptions, and tracking details per user.

### 🔄 Milestone C: Multi-Channel Distribution & Automation Architecture
To push content out dynamically without blocking the main FastAPI server, we hook into specialized distribution environments:

* **`backend/app/api/billing.py` (Flesh Out):**
  * Integration of payment processors (like Stripe webhooks) to secure and gate user access levels.
* **`n8n-automation/workflows/publish_pipeline.json` (Build Workflow):**
  * Construct visual webhooks in n8n that catch parsed payload data sent by the FastAPI backend, parse it, and route it dynamically through official publisher APIs.

---

## 🔑 3. External API Integration Checklists
To complete the system, we will need to register developer accounts and extract access tokens from the following platforms:

| Platform / Service | Required Credentials | Purpose in the SaaS |
| :--- | :--- | :--- |
| **OpenAI Developer Platform** | `OPENAI_API_KEY` | Powers the core AI Copywriting Engine (GPT-4o-mini). |
| **Telegram (via @BotFather)** | `TELEGRAM_BOT_TOKEN`, `CHAT_ID` | Delivers instant automated image/text posts to client channels. |
| **Meta for Developers** | `FACEBOOK_APP_ID`, `PAGE_ACCESS_TOKEN` | Authorizes the backend to write to Facebook groups and pages via the Graph API. |
| **Pinterest Developer Portal** | `PINTEREST_ACCESS_TOKEN`, `BOARD_ID` | Creates optimized marketing boards and redirect pins. |
| **Stripe Dashboard** (Optional / Future) | `STRIPE_API_KEY`, `WEBHOOK_SECRET` | Manages subscription tiers, premium access, and monetization. |